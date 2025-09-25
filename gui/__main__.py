from .main_window import WatermarkMainWindow
import sys
from PyQt5.QtWidgets import QApplication

def main():
    app = QApplication(sys.argv)
    win = WatermarkMainWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
