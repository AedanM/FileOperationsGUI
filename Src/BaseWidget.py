from typing import Callable

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


class BaseWidget(QWidget):
    MainFolderInput: QLineEdit

    def __init__(self, parent) -> None:
        QWidget.__init__(self, parent=parent)
        self.setObjectName(self.CleanName)
        layout = QGridLayout(self)
        self.setLayout(layout)

    @property
    def ActiveField(self) -> str:
        return self.MainFolderInput.text().replace('"', "")

    def Setup(self, **kwargs) -> None:
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

    def BuildInputFrame(self, lineEdit: QLineEdit, selectFolder: bool = True):
        inputFrame = QFrame(self)
        browseButton = QPushButton(inputFrame)
        browseButton.setText("Browse")
        browseButton.clicked.connect(
            lambda: (
                self.SelectFolder(lineEdit=lineEdit) if selectFolder else self.SelectFile(lineEdit)
            )
        )

        inputFrameLayout = QHBoxLayout(inputFrame)

        inputFrameLayout.addWidget(lineEdit)
        inputFrameLayout.addWidget(browseButton)
        return inputFrame

    def SelectFolder(self, lineEdit: QLineEdit):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        lineEdit.setText(folder)
        return folder

    def SelectFile(self, lineEdit: QLineEdit):
        folder = QFileDialog.getOpenFileName(self, "Select File")
        lineEdit.setText(folder[0])
        return folder

    def BuildBaseFrame(self, title: str, caption: str):
        funcFrame = QFrame(self)
        inputFrameLayout = QVBoxLayout(funcFrame)

        titleLabel = QLabel(funcFrame)
        titleLabel.setStyleSheet("border:0px; border-bottom:5px solid white")
        titleLabel.setFixedHeight(100)
        titleLabel.setText(f"<h1>{title}</h1>")

        descLabel = QLabel(funcFrame)
        descLabel.setText(f"<p>{caption}<p>")
        descLabel.setWordWrap(True)

        inputFrameLayout.addWidget(titleLabel)
        inputFrameLayout.addWidget(descLabel)

        return funcFrame, inputFrameLayout

    def BuildRunButton(self, masterFrame: QFrame, masterLayout, connection: Callable):
        runButton = QPushButton(masterFrame)
        runButton.setText("Run")

        def Connection():
            for result in connection():
                try:
                    currentText = self.OutputText.toPlainText()  # type: ignore
                    self.OutputText.setText(f"{currentText}\n{result}")  # type: ignore
                    self.OutputText.verticalScrollBar().setValue(  # type:ignore
                        self.OutputText.verticalScrollBar().maximum()  # type:ignore
                    )
                except Exception as e:
                    print(e)

        runButton.clicked.connect(Connection)

        masterLayout.addWidget(runButton)

    def AddButtonFrame(self, masterFrame: QFrame, masterLayout, labelStr: str):
        btnFrame = QFrame(masterFrame)
        btnLayout = QHBoxLayout(btnFrame)
        btnLabel = QLabel(btnFrame)
        btnLabel.setText(labelStr)

        btn = QRadioButton(masterFrame)
        btnLayout.addWidget(btnLabel)
        btnLayout.addWidget(btn)
        masterLayout.addWidget(btnFrame)
        return btn
