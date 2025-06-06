from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTabWidget, QLabel, QLineEdit, QTextEdit, QHBoxLayout, QFormLayout, QMessageBox
from theoritical import calculate_queue_metrics
from plot import PlotWidget


class QueueSimulatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Queue Simulator")
        self.setGeometry(100, 100, 600, 800)
        
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

    def run_calculation(self):
        lamda = float(self.lamda_field.text())
        mu = float(self.mu_field.text())
        results, data = calculate_queue_metrics(lamda, mu)
        self.result_area.setPlainText(results)

        # Remove any previous plot
        for i in reversed(range(self.plot_layout.count())):
            self.plot_layout.itemAt(i).widget().setParent(None)

        dummy_sim_data = {                          #TODO: Replace dummy data with real simulation data
            "rho_sim": [
                0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75,
                0.8, 0.85, 0.9, 0.92, 0.94, 0.95, 0.96, 0.97, 0.98, 0.99
            ],
            "Wq_sim": [
                0.05, 0.11, 0.18, 0.28, 0.5, 0.85, 1.3, 2.3, 4.8, 7.5,
                12.0, 20.5, 38.0, 55.0, 85.0, 120.0, 160.0, 220.0, 350.0, 600.0
            ]  # in minutes, sharply rising near 1
        }

        # Add the new plot
        plot_widget = PlotWidget(data, dummy_sim_data)
        self.plot_layout.addWidget(plot_widget)

