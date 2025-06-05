from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from gui import QueueSimulatorGUI
import sys

if __name__ == "__main__":
    app = QApplication([])

    window = QueueSimulatorGUI()
    window.show()

    sys.exit(app.exec())
