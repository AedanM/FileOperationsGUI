import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QStyleFactory, QTabWidget
from tendo import singleton

from Src.Widgets import ImageWidget, MediaWidget, SingleWidget

INSTANCE = singleton.SingleInstance()


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.TabView = QTabWidget()
        self.TabView.addTab(ImageWidget.ImageWidget(self.TabView), "Image Operations")
        self.TabView.addTab(MediaWidget.MediaWidget(self.TabView), "Media Operations")
        self.TabView.addTab(SingleWidget.SingleWidget(self.TabView), "Single Operations")
        self.setCentralWidget(self.TabView)

        self.setWindowTitle("Media GUI")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    window = MainWindow()
    window.show()
    app.exec()
