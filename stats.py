from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication

uiloader = QUiLoader()


class Stats:
    def __init__(self):
        self.ui = uiloader.load("ui/stats.ui")
        self.ui.button.clicked.connect(self.handleCalc)

    @staticmethod
    def handleCalc():
        print("统计按钮被点击了")


if __name__ == '__main__':
    app = QApplication([])
    stats = Stats()
    stats.ui.show()
    app.exec()
