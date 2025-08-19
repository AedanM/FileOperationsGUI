"""Base widget which gui in built on."""

from collections.abc import Callable
from typing import Any

from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtWidgets import (
    QFileDialog,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QRadioButton,
    QVBoxLayout,
    QWidget,
)


class WorkerThread(QThread):
    """Ability to do things away from gui thread."""

    resultReady = pyqtSignal(str)

    def __init__(self, connection: Callable) -> None:
        super().__init__()
        self.connection = connection

    def run(self) -> None:
        try:
            for result in self.connection():
                self.resultReady.emit(result)
        except Exception as e:
            self.resultReady.emit(f"Error Occurred {e}")


class BaseWidget(QWidget):
    """Base widget for FileOpsGui."""

    MainFolderInput: QLineEdit

    def __init__(self, parent: QWidget) -> None:
        QWidget.__init__(self, parent=parent)
        self.setObjectName(self.CleanName)
        layout = QGridLayout(self)
        self.setLayout(layout)

    @property
    def ActiveField(self) -> str:
        return self.MainFolderInput.text().replace('"', "")

    def Setup(self, **_kwargs: Any) -> None:
        pass

    @property
    def CleanName(self) -> str:
        return str(self.__class__).rsplit(".", 1)[-1][:-2].replace("Screen", "").strip()

    @property
    def Layout(self) -> QGridLayout:
        layout = self.layout()
        if not isinstance(layout, QGridLayout):
            layout = QGridLayout(self)
        return layout

    def BuildInputFrame(self, lineEdit: QLineEdit, selectFolder: bool = True) -> QFrame:
        inputFrame = QFrame(self)
        browseButton = QPushButton(inputFrame)
        browseButton.setText("Browse")
        browseButton.clicked.connect(
            lambda: (
                self.SelectFolder(lineEdit=lineEdit) if selectFolder else self.SelectFile(lineEdit)
            ),
        )

        inputFrameLayout = QHBoxLayout(inputFrame)

        inputFrameLayout.addWidget(lineEdit)
        inputFrameLayout.addWidget(browseButton)
        return inputFrame

    def SelectFolder(self, lineEdit: QLineEdit) -> str:
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        lineEdit.setText(folder)
        return folder

    def SelectFile(self, lineEdit: QLineEdit) -> str:
        folder = QFileDialog.getOpenFileName(self, "Select File")
        lineEdit.setText(folder[0])
        return folder

    def BuildBaseFrame(self, title: str, caption: str) -> tuple[QFrame, QVBoxLayout]:
        funcFrame = QFrame(self)
        inputFrameLayout = QVBoxLayout(funcFrame)

        titleLabel = QLabel(funcFrame)
        titleLabel.setStyleSheet("border:0px; border-bottom:5px solid white")
        titleLabel.setFixedHeight(75)
        titleLabel.setText(f"<h1>{title}</h1>")

        descLabel = QLabel(funcFrame)
        descLabel.setText(f"<p>{caption}<p>")
        descLabel.setWordWrap(True)

        inputFrameLayout.addWidget(titleLabel)
        inputFrameLayout.addWidget(descLabel)

        return funcFrame, inputFrameLayout

    def BuildRunButton(
        self,
        masterFrame: QFrame,
        masterLayout: QHBoxLayout | QVBoxLayout,
        connection: Callable,
    ) -> None:
        """Build a run button hooked to a command.

        Parameters
        ----------
        masterFrame : QFrame
            Parent frame for control
        masterLayout : QHBoxLayout | QVBoxLayout
            parent layout for control
        connection : Callable
            linked method for control, ideally returns a generator
        """
        runButton = QPushButton("Run", masterFrame)

        def displayResult(result: str) -> None:
            currentText = self.OutputText.toPlainText()
            self.OutputText.setText(f"{currentText}\n{result}")
            self.OutputText.verticalScrollBar().setValue(
                self.OutputText.verticalScrollBar().maximum(),
            )

        def startWorker() -> None:
            self.worker = WorkerThread(connection)
            self.worker.resultReady.connect(displayResult)
            self.worker.start()

        runButton.clicked.connect(startWorker)
        masterLayout.addWidget(runButton)

    def AddButtonFrame(
        self,
        masterFrame: QFrame,
        masterLayout: QHBoxLayout | QVBoxLayout,
        labelStr: str,
    ) -> QRadioButton:
        """Add a button frame to layout control.

        Parameters
        ----------
        masterFrame : QFrame
            Parent frame for control
        masterLayout : QHBoxLayout | QVBoxLayout
            parent layout for control
        labelStr : str
            description of control

        Returns
        -------
        QRadioButton
            returns the added button control
        """
        btnFrame = QFrame(masterFrame)
        btnLayout = QHBoxLayout(btnFrame)
        btnLabel = QLabel(btnFrame)
        btnLabel.setText(labelStr)

        btn = QRadioButton(masterFrame)
        btnLayout.addWidget(btnLabel)
        btnLayout.addWidget(btn)
        masterLayout.addWidget(btnFrame)
        return btn
