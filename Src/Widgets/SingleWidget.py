"""Widget page for single operations."""

from collections.abc import Generator

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QWidget

from Src.Utilities.TranslateInPlace import TranslateV2
from Src.Widgets.BaseWidget import BaseWidget


class SingleWidget(BaseWidget):
    """Operation tools for ideally single operations."""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.OutputText = QTextEdit(self)
        masterFolderLabel = QLabel(self)
        masterFolderLabel.setText("<h1>Active Image</h1>")
        masterFolderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.MainFolderInput = QLineEdit(self)
        inputFrame = self.BuildInputFrame(self.MainFolderInput, False)

        self.Layout.addWidget(masterFolderLabel, 0, 0, 1, 7)
        self.Layout.addWidget(self.OutputText, 10, 0, 1, 7)
        self.Layout.addWidget(inputFrame, 1, 0, 1, 7)

        self.BuildTranslateFrame(4)

    # region Constructors

    def BuildTranslateFrame(self, columnIdx: int) -> None:
        """Build frame for translating image.

        Parameters
        ----------
        columnIdx : int
            column to place the frame inside

        """
        frame, layout = self.BuildBaseFrame(
            title="Translate Image",
            caption="Detect and translate text on page",
        )

        lang = QLineEdit(frame)
        lang.setPlaceholderText("Source Language")
        layout.addWidget(lang)

        def RunAction() -> Generator[str]:
            return TranslateV2(lang.text(), self.ActiveField)

        self.BuildRunButton(frame, layout, RunAction)

        self.Layout.addWidget(frame, 3, columnIdx, 3, 1)

    # endregion
