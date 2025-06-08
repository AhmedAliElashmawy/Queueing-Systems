import sys
import os
import random
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logic')))

from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QTabWidget, QLineEdit, QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout, QDialog, QLabel, QDialogButtonBox
from PyQt6.QtCore import Qt


from plot import PlotWidget
from theoritical import calculate_queue_metrics
from simulation import QueueSimulator

class QueueSimulatorGUI(QMainWindow):


    DEFAULT_SIZE = (600, 426)
    DEFAULT_POSITION = (100, 100)
    DEFAULT_TITLE = "Queue Simulator"

    scenarios =[
        {"mu": 12, "lamda": 4},
        {"mu": 12, "lamda": 6},
        {"mu": 12, "lamda": 10}
    ]

    def __init__(self):
        super().__init__()
        self.setWindowTitle(QueueSimulatorGUI.DEFAULT_TITLE)
        self.setGeometry(*self.DEFAULT_POSITION, *self.DEFAULT_SIZE)

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.layout = QVBoxLayout(central_widget)

        self.tabs = QTabWidget()
        self.layout.addWidget(self.tabs)

        self.init_calculations()
        self.init_plot()

    def init_calculations(self):
        calculations_tab = QWidget()
        calculations_layout = QVBoxLayout()

        # Parameter input section
        params_layout = QVBoxLayout()

        # First Row
        scenarios_layout1 = QHBoxLayout()
        self.scenario_button0 = QPushButton("Scenario 0: λ=4, μ=12")
        self.scenario_button0.clicked.connect(lambda: self.load_scenario(0))
        scenarios_layout1.addWidget(self.scenario_button0)

        self.scenario_button1 = QPushButton("Scenario 1: λ=6, μ=12")
        self.scenario_button1.clicked.connect(lambda: self.load_scenario(1))
        scenarios_layout1.addWidget(self.scenario_button1)
        
        # Second row
        scenarios_layout2 = QHBoxLayout()
        self.scenario_button2 = QPushButton("Scenario 2: λ=10, μ=12")
        self.scenario_button2.clicked.connect(lambda: self.load_scenario(2))
        scenarios_layout2.addWidget(self.scenario_button2)
        
        self.custom_scenario_button = QPushButton("Custom Scenario")
        self.custom_scenario_button.clicked.connect(self.open_custom_scenario)
        scenarios_layout2.addWidget(self.custom_scenario_button)
        
        # Add both rows to the params layout
        params_layout.addLayout(scenarios_layout1)
        params_layout.addLayout(scenarios_layout2)

        calculations_layout.addLayout(params_layout)

        # Create a table for comparison
        self.table = QTableWidget(9, 2)  # 9 rows (rho, Wq, Ws, L, Lq), 2 columns (Theoretical, Simulation)
        self.table.setHorizontalHeaderLabels(["Theoretical", "Simulation"])
        self.table.setVerticalHeaderLabels(["Server Utilization (ρ)",
                                            "Avg Wait Time in Queue in minutes (Wq)",
                                            "Avg Time in System in minutes (Ws)",
                                            "Avg Customers in System (L)",
                                            "Avg Customers in Queue (Lq)",
                                            "P(System has 0 customers) (P₀)",
                                            "P(System has 1 customer) (P₁)",
                                            "P(System has 2 customers) (P₂)",
                                            "P(System has 3 customers) (P₃)"
                                            ])

        # Set the first column with metrics names
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        calculations_layout.addWidget(self.table)

        calculations_tab.setLayout(calculations_layout)
        self.tabs.addTab(calculations_tab, "Comparison")

    def load_scenario(self, scenario_index):
        """Load a predefined scenario"""
        scenario = self.scenarios[scenario_index]
        self.run_calculation(scenario["lamda"], scenario["mu"])

    def open_custom_scenario(self):
        """Open dialog to input custom scenario parameters"""
        dialog = QDialog(self)
        dialog.setWindowTitle("Custom Scenario")
        
        layout = QVBoxLayout()
        
        mu_layout = QHBoxLayout()
        mu_label = QLabel("Service Rate (μ):")
        mu_field = QLineEdit()
        mu_layout.addWidget(mu_label)
        mu_layout.addWidget(mu_field)
        layout.addLayout(mu_layout)
        
        lamda_layout = QHBoxLayout()
        lamda_label = QLabel("Arrival Rate (λ):")
        lamda_field = QLineEdit()
        lamda_layout.addWidget(lamda_label)
        lamda_layout.addWidget(lamda_field)
        layout.addLayout(lamda_layout)
        
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(dialog.accept)
        buttons.rejected.connect(dialog.reject)
        layout.addWidget(buttons)
        
        dialog.setLayout(layout)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            try:
                if mu_field.text() == "" or lamda_field.text() == "":
                    raise ValueError("Rates cannot be empty.")
                mu = float(mu_field.text())
                lamda = float(lamda_field.text())
                if mu <= 0 or lamda <= 0:
                    raise ValueError("Rates must be positive.")
                if lamda >= mu:
                    raise ValueError("Arrival rate (λ) must be less than service rate (μ).")
                self.run_calculation(lamda, mu)
            except ValueError as e:
                error_dialog = QDialog(self)
                error_dialog.setWindowTitle("Error")
                error_layout = QVBoxLayout()
                error_label = QLabel(str(e))
                error_layout.addWidget(error_label)
                ok_button = QPushButton("OK")
                ok_button.clicked.connect(error_dialog.accept)
                error_layout.addWidget(ok_button)
                error_dialog.setLayout(error_layout)
                error_dialog.exec()

    def init_plot(self):
        self.plot_tab = QWidget()
        self.plot_layout = QVBoxLayout()
        self.plot_tab.setLayout(self.plot_layout)
        self.tabs.addTab(self.plot_tab, "Plot")

    def generate_sorted_spread_points(self,n=20):
        step = 1.0 / (n + 1)
        points = [(i + 1) * step + random.uniform(-0.4, 0.4) * step for i in range(n)]

        points = [min(max(p, 0.0001), 0.9999) for p in points]
        return sorted(points)

    def generate_simulation_data(self, mu):
        """
        Generate ploting data for simulation.
        """

        rho_points = self.generate_sorted_spread_points()

        wq_points = []
        lamda_values = [rho * mu for rho in rho_points]

        simulator = QueueSimulator()

        for lamda in lamda_values:
            simulator.run_simulation(lamda, mu)
            wq_points.append(simulator.Wq)


        return {
            "rho_sim": rho_points,
            "Wq_sim": wq_points
        }



    def run_calculation(self, lamda, mu):
        # Get theoretical results
        results, theory_data = calculate_queue_metrics(lamda, mu)

        # Run simulation
        simulator = QueueSimulator()
        simulator.run_simulation(lamda, mu)

        # Fill table with theoretical values
        self.table.setItem(0, 0, QTableWidgetItem(f"{results['rho']:.4f}"))
        self.table.setItem(1, 0, QTableWidgetItem(f"{results['Wq']*60:.4f}"))
        self.table.setItem(2, 0, QTableWidgetItem(f"{results['Ws']*60:.4f}"))
        self.table.setItem(3, 0, QTableWidgetItem(f"{results['L']:.4f}"))
        self.table.setItem(4, 0, QTableWidgetItem(f"{results['Lq']:.4f}"))
        self.table.setItem(5, 0, QTableWidgetItem(f"{results['P'][0]:.4f}"))
        self.table.setItem(6, 0, QTableWidgetItem(f"{results['P'][1]:.4f}"))
        self.table.setItem(7, 0, QTableWidgetItem(f"{results['P'][2]:.4f}"))
        self.table.setItem(8, 0, QTableWidgetItem(f"{results['P'][3]:.4f}"))

        # Fill table with simulation values
        self.table.setItem(0, 1, QTableWidgetItem(f"{simulator.rho:.4f}"))
        self.table.setItem(1, 1, QTableWidgetItem(f"{simulator.Wq:.4f}"))
        self.table.setItem(2, 1, QTableWidgetItem(f"{simulator.Ws:.4f}"))
        self.table.setItem(3, 1, QTableWidgetItem(f"{simulator.L:.4f}"))
        self.table.setItem(4, 1, QTableWidgetItem(f"{simulator.Lq:.4f}"))
        self.table.setItem(5, 1, QTableWidgetItem(f"{simulator.P[0]:.4f}"))
        self.table.setItem(6, 1, QTableWidgetItem(f"{simulator.P[1]:.4f}"))
        self.table.setItem(7, 1, QTableWidgetItem(f"{simulator.P[2]:.4f}"))
        self.table.setItem(8, 1, QTableWidgetItem(f"{simulator.P[3]:.4f}"))

        # Make all cells read-only
        for row in range(9):
            for col in range(2):
                if item := self.table.item(row, col):
                    item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)

        # Remove any previous plot
        for i in reversed(range(self.plot_layout.count())):
            self.plot_layout.itemAt(i).widget().setParent(None)

        # Generate simulation data points for plot
        sim_data = self.generate_simulation_data(mu)

        # Add the new plot
        plot_widget = PlotWidget(theory_data, sim_data)
        self.plot_layout.addWidget(plot_widget)


