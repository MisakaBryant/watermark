import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

class WatermarkMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Watermark 批量水印工具")
        self.setGeometry(200, 200, 900, 600)
        label = QLabel("Hello, Watermark GUI!", self)
        label.move(50, 50)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = WatermarkMainWindow()
    win.show()
    sys.exit(app.exec_())
