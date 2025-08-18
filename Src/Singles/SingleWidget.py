"""Widget page for single operations."""

from collections.abc import Generator
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QLineEdit, QTextEdit, QWidget

from Src.BaseWidget import BaseWidget
from Src.Singles.ImageSequences import DecompileGIF, DecompilePDF, DecompileVideo, SplitIMG
from Src.Singles.TranslateInPlace import TranslateV2
from Src.Singles.TrimEdges import TrimAllEdges


class SingleOperationsWidget(BaseWidget):
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

        self.BuildSplitFrame(2)
        self.BuildTranslateFrame(4)
        self.BuildTrimFrame(6)
        self.BuildPDFDecompileFrame(2)
        self.BuildGifDecompileFrame(4)
        self.BuildVideoDecompileFrame(6)

    def BuildSplitFrame(self, columnIdx: int) -> None:
        """Build frame for splitting image.

        Parameters
        ----------
        columnIdx : int
            column to place the frame inside

        """
        frame, layout = self.BuildBaseFrame(
            title="Split Image",
            caption="Split an image into a sequence",
        )

        gridSize = QLineEdit(frame)
        gridSize.setPlaceholderText("Grid Size")
        layout.addWidget(gridSize)

        makeDir = self.AddButtonFrame(frame, layout, "SubDir")

        def RunAction() -> Generator[str]:
            return SplitIMG(
                Path(self.ActiveField),
                [int(x) for x in gridSize.text().split("x")],
                makeSubDir=makeDir.isChecked(),
            )

        self.BuildRunButton(frame, layout, RunAction)

        self.Layout.addWidget(frame, 3, columnIdx, 3, 1)

    def BuildTrimFrame(self, columnIdx: int) -> None:
        """Build frame for trimming image.

        Parameters
        ----------
        columnIdx : int
            column to place the frame inside

        """
        frame, layout = self.BuildBaseFrame(
            title="Trim Image",
            caption="Cut away colored edge",
        )

        trimColor = QLineEdit(frame)
        trimColor.setPlaceholderText("Color Array")
        layout.addWidget(trimColor)

        def RunAction() -> Generator[str]:
            return TrimAllEdges(
                Path(self.ActiveField),
                trimColor.text().split(",") if trimColor.text() != "" else None,
            )

        self.BuildRunButton(frame, layout, RunAction)

        self.Layout.addWidget(frame, 3, columnIdx, 3, 1)

    def BuildPDFDecompileFrame(self, columnIdx: int) -> None:
        """Build frame to decompile pdf.

        Parameters
        ----------
        columnIdx : int
            column to place the frame inside

        """
        frame, layout = self.BuildBaseFrame(
            title="Decomp PDF File",
            caption="Turn a PDF file into a image sequence",
        )

        makeDir = self.AddButtonFrame(frame, layout, "SubDir")

        def RunAction() -> Generator[str]:
            return DecompilePDF(Path(self.ActiveField), makeDir)

        self.BuildRunButton(frame, layout, RunAction)

        self.Layout.addWidget(frame, 6, columnIdx, 3, 1)

    def BuildGifDecompileFrame(self, columnIdx: int) -> None:
        """Build frame to decompile gif.

        Parameters
        ----------
        columnIdx : int
            column to place the frame inside

        """
        frame, layout = self.BuildBaseFrame(
            title="Decomp GIF File",
            caption="Turn a GIF file into a image sequence",
        )
        makeDir = self.AddButtonFrame(frame, layout, "SubDir")

        def RunAction() -> Generator[str]:
            return DecompileGIF(Path(self.ActiveField), makeDir.isChecked())

        self.BuildRunButton(frame, layout, RunAction)

        self.Layout.addWidget(frame, 6, columnIdx, 3, 1)

    def BuildVideoDecompileFrame(self, columnIdx: int) -> None:
        """Build frame to decompile videos.

        Parameters
        ----------
        columnIdx : int
            column to place the frame inside

        """
        frame, layout = self.BuildBaseFrame(
            title="Decomp Video File",
            caption="Turn a Video file into a image sequence",
        )
        makeDir = self.AddButtonFrame(frame, layout, "SubDir")

        def RunAction() -> Generator[str]:
            return DecompileVideo(Path(self.ActiveField), makeSubDir=makeDir)

        self.BuildRunButton(frame, layout, RunAction)

        self.Layout.addWidget(frame, 6, columnIdx, 3, 1)

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
