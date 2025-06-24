import sys

from PyQt6.QtWidgets import QApplication, QMainWindow, QStyleFactory, QTabWidget
from Src.Images.ImageWidget import ImageOperationsWidget
from Src.Media.MediaWidget import MediaOperationsWidget
from Src.Singles.SingleWidget import SingleOperationsWidget


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.TabView = QTabWidget()
        self.TabView.addTab(ImageOperationsWidget(self.TabView), "Image Operations")
        self.TabView.addTab(MediaOperationsWidget(self.TabView), "Media Operations")
        self.TabView.addTab(SingleOperationsWidget(self.TabView), "Single Operations")
        self.setCentralWidget(self.TabView)

        self.setWindowTitle("Media GUI")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("Fusion"))
    window = MainWindow()
    window.show()
    app.exec()
