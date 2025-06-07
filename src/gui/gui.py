import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logic')))

from PyQt6.QtWidgets import QMainWindow, QPushButton, QVBoxLayout, QWidget, QTabWidget, QLineEdit, QTextEdit
from plot import PlotWidget


from theoritical import calculate_queue_metrics
from simulation import QueueSimulator

class QueueSimulatorGUI(QMainWindow):


    DEFAULT_SIZE = (600, 800)
    DEFAULT_POSITION = (100, 100)
    DEFAULT_TITLE = "Queue Simulator"

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

        # Add input fields and buttons for calculations
        self.lamda_field = QLineEdit()
        self.lamda_field.setPlaceholderText("Enter λ (arrival rate)")
        calculations_layout.addWidget(self.lamda_field)

        self.mu_field = QLineEdit()
        self.mu_field.setPlaceholderText("Enter μ (service rate)")
        calculations_layout.addWidget(self.mu_field)

        self.calculate_button = QPushButton("Run Calculation")
        self.calculate_button.clicked.connect(self.run_calculation)
        calculations_layout.addWidget(self.calculate_button)

        self.result_area = QTextEdit()
        self.result_area.setReadOnly(True)
        calculations_layout.addWidget(self.result_area)

        calculations_tab.setLayout(calculations_layout)
        self.tabs.addTab(calculations_tab, "Calculations")

    def init_plot(self):
        self.plot_tab = QWidget()
        self.plot_layout = QVBoxLayout()
        self.plot_tab.setLayout(self.plot_layout)
        self.tabs.addTab(self.plot_tab, "Plot")


    def generate_simulation_data(self, mu):
        """
        Generate ploting data for simulation.
        """
        # rho_points = [i*4.9 / 100 for i in range(1, 20)]
        rho_points =  [
                0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75,
                0.8, 0.85, 0.9, 0.92, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99
            ]

        wq_points = []
        lamda_values = [rho * mu for rho in rho_points]

        simulator = QueueSimulator()

        for lamda in lamda_values:
            simulator.run_simulation(lamda, mu)
            wq_points.append(simulator.Wq* 60)


        return {
            "rho_sim": rho_points,
            "Wq_sim": wq_points
        }



    def run_calculation(self):
        lamda = float(self.lamda_field.text())
        mu = float(self.mu_field.text())
        results, data = calculate_queue_metrics(lamda, mu)
        self.result_area.setPlainText(results)

        # Remove any previous plot
        for i in reversed(range(self.plot_layout.count())):
            self.plot_layout.itemAt(i).widget().setParent(None)

        # Generates simulation data points
        sim_data = self.generate_simulation_data(mu)

        # Add the new plot
        plot_widget = PlotWidget(data, sim_data)
        self.plot_layout.addWidget(plot_widget)

