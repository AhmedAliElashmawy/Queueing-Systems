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
        plot_tab = QWidget()
        plot_layout = QVBoxLayout()
        plot_tab.setLayout(plot_layout)
        self.tabs.addTab(plot_tab, "Plot")

    def run_calculation(self):
        lamda = float(self.lamda_field.text())
        mu = float(self.mu_field.text())
        results, data = calculate_queue_metrics(lamda, mu)
        self.result_area.setPlainText(results)
        PlotWidget(data)
