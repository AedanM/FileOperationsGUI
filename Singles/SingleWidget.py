from pathlib import Path

from BaseWidget import BaseWidget
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit
from Singles.DecompilePDF import DecompilePDF
from Singles.SplitIMG import SplitIMG
from Singles.TranslateIMG import TranslateIMG
from Singles.TrimEdges import TrimAllEdges


class SingleOperationsWidget(BaseWidget):

    def __init__(self, parent):
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

        self.BuildSplitFrame(2)
        self.BuildTranslateFrame(4)
        self.BuildTrimFrame(6)
        self.BuildDecompileFrame(2)

    def BuildSplitFrame(self, idx):
        frame, layout = self.BuildBaseFrame(
            title="Split Image",
            caption="Split Up an Image into Composites",
        )

        gridSize = QLineEdit(frame)
        gridSize.setPlaceholderText("Grid Size")
        layout.addWidget(gridSize)

        makeDir = self.AddButtonFrame(frame, layout, "SubDir")

        def RunAction():
            yield SplitIMG(
                Path(self.ActiveField),
                [int(x) for x in gridSize.text().split("x")],
                makeSubDir=makeDir.isChecked(),
            )

        self.BuildRunButton(frame, layout, RunAction)

        self.Layout.addWidget(frame, 3, idx, 3, 1)

    def BuildTrimFrame(self, idx):
        frame, layout = self.BuildBaseFrame(
            title="Trim Image",
            caption="Cut away colored edge",
        )

        trimColor = QLineEdit(frame)
        trimColor.setPlaceholderText("Color Array")
        layout.addWidget(trimColor)

        def RunAction():
            yield TrimAllEdges(
                Path(self.ActiveField),
                trimColor.text().split(",") if trimColor.text() != "" else None,
            )

        self.BuildRunButton(frame, layout, RunAction)

        self.Layout.addWidget(frame, 3, idx, 3, 1)

    def BuildDecompileFrame(self, idx):
        frame, layout = self.BuildBaseFrame(
            title="Decompile PDF File",
            caption="Turn a PDF file into a image sequence",
        )

        def RunAction():
            yield DecompilePDF(
                Path(self.ActiveField),
            )

        self.BuildRunButton(frame, layout, RunAction)

        self.Layout.addWidget(frame, 6, idx, 3, 1)

    def BuildTranslateFrame(self, idx):
        frame, layout = self.BuildBaseFrame(
            title="Translate Image",
            caption="Reformat Metadata based on File Name",
        )

        lang = QLineEdit(frame)
        lang.setPlaceholderText("Source Language")
        layout.addWidget(lang)

        def RunAction():
            yield TranslateIMG(lang.text(), self.ActiveField)

        self.BuildRunButton(frame, layout, RunAction)

        self.Layout.addWidget(frame, 3, idx, 3, 1)
