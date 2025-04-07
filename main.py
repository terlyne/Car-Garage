from ui.main_window import MainWindow
from models.garage import CGarage
from PyQt6.QtWidgets import QApplication
import sys


def main():
    garage = CGarage(max_auto=10)

    app = QApplication(sys.argv)
    window = MainWindow(garage)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
