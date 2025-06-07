import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.', 'gui')))

from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from gui import QueueSimulatorGUI

if __name__ == "__main__":
    app = QApplication([])

    window = QueueSimulatorGUI()
    window.show()

    sys.exit(app.exec())