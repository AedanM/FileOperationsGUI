"""Widget for image manipulation, essentially the homepage."""

from collections.abc import Generator
from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QComboBox, QDoubleSpinBox, QLabel, QLineEdit, QTextEdit, QWidget

from Src.Images.FixNames import FixNames
from Src.Images.FolderTools import Flatten, SortToFolders
from Src.Images.ImageSequences import DecompileGIF, DecompilePDF, DecompileVideo
from Src.Images.PDFTools import CompileFolders
from Src.Images.TrimEdges import TrimAllEdges
from Src.Utilities.UtilityTools import GenerateMessage
from Src.Widgets.BaseWidget import BaseWidget


class ImageWidget(BaseWidget):
    """Image operations page of the widget."""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)

        self.OutputText = QTextEdit(self)
        self.OutputText.setMinimumHeight(200)

        masterFolderLabel = QLabel(self)
        masterFolderLabel.setText("<h1>Master Folder</h1>")
        masterFolderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.MainFolderInput = QLineEdit(self)
        inputFrame = self.BuildInputFrame(self.MainFolderInput)

        self.Layout.addWidget(masterFolderLabel, 0, 0, 1, 7)
        self.Layout.addWidget(self.OutputText, 10, 0, 1, 7)
        self.Layout.addWidget(inputFrame, 1, 0, 1, 7)

        self.BuildFixNamesFrame(2, 3)
        self.BuildTrimFrame(2, 6)

        self.BuildSortFolderFrame(4, 3)
        self.BuildFlattenFrame(4, 6)

        self.BuildCompilePDFFrame(6, 3)
        self.BuildDecompileFrame(6, 6)

    # region Constructors
    def BuildSortFolderFrame(self, columnIdx: int, rowIdx: int) -> None:
        frame, layout = self.BuildBaseFrame(
            title="Sort To Folders",
            caption="Sort Img sequences to Folders",
        )
        simplify = self.AddButtonFrame(frame, layout, "Simplify First")

        def RunAction() -> Generator[str]:
            return SortToFolders(Path(self.ActiveField), simplify.isChecked())

        self.BuildRunButton(frame, layout, RunAction)
        self.Layout.addWidget(frame, rowIdx, columnIdx, 3, 1)

    def BuildFlattenFrame(self, columnIdx: int, rowIdx: int) -> None:
        frame, layout = self.BuildBaseFrame(
            title="Flatten",
            caption="Flatten a file directory",
        )

        rename = self.AddButtonFrame(frame, layout, "Rename")
        delete = self.AddButtonFrame(frame, layout, "Delete")

        globPattern = QLineEdit(frame)
        globPattern.setPlaceholderText("Glob Pattern")
        layout.addWidget(globPattern)

        def RunAction() -> Generator[str]:
            return Flatten(
                Path(self.ActiveField),
                rename.isChecked(),
                delete.isChecked(),
                globPattern=globPattern.text() if globPattern.text() else "**/*.*",
            )

        self.BuildRunButton(frame, layout, RunAction)
        self.Layout.addWidget(frame, rowIdx, columnIdx, 3, 1)

    def BuildCompilePDFFrame(self, columnIdx: int, rowIdx: int) -> None:
        frame, layout = self.BuildBaseFrame(
            title="Compile To PDF",
            caption="Convert Img Sequence to PDF</p><p>At % resolution",
        )

        resolutionBox = QDoubleSpinBox(frame)
        resolutionBox.setMaximum(100.00)
        resolutionBox.setValue(100.0)
        layout.addWidget(resolutionBox)

        def RunAction() -> Generator[str]:
            return CompileFolders(
                Path(self.ActiveField),
                resolutionBox.value(),
            )

        self.BuildRunButton(frame, layout, RunAction)
        self.Layout.addWidget(frame, rowIdx, columnIdx, 3, 1)

    def BuildFixNamesFrame(self, columnIdx: int, rowIdx: int) -> None:
        frame, layout = self.BuildBaseFrame(
            title="Fix Names",
            caption="Apply Naming Rules",
        )

        globFilter = QLineEdit(frame)
        globFilter.setPlaceholderText("Glob Pattern")
        layout.addWidget(globFilter)

        def RunAction() -> Generator[str]:
            return FixNames(
                Path(self.ActiveField),
                globFilter.text() if globFilter.text() != "" else "*.*",
            )

        self.BuildRunButton(frame, layout, RunAction)
        self.Layout.addWidget(frame, rowIdx, columnIdx, 3, 1)

    def BuildDecompileFrame(self, columnIdx: int, rowIdx: int) -> None:
        """Build frame to decompile files.

        Parameters
        ----------
        columnIdx : int
            column to place the frame inside
        rowIdx : int
            row to place frame on

        """
        frame, layout = self.BuildBaseFrame(
            title="Decomp Files",
            caption="Turn a file type into a image sequence",
        )

        decompileOptions: QComboBox = QComboBox()
        decompileOptions.addItems(["GIF", "PDF", "VIDEO"])
        layout.addWidget(decompileOptions)

        makeDir = self.AddButtonFrame(frame, layout, "Create SubDir")

        def RunAction() -> Generator[str]:
            match decompileOptions.currentText():
                case "GIF":
                    return DecompileGIF(Path(self.ActiveField), makeDir.isChecked())
                case "PDF":
                    return DecompilePDF(Path(self.ActiveField), makeDir.isChecked())
                case "VIDEO":
                    return DecompileVideo(Path(self.ActiveField), makeDir.isChecked())
                case _others:
                    return GenerateMessage(
                        f"Invalid selection {decompileOptions.currentText()}",
                    )

        self.BuildRunButton(frame, layout, RunAction)

        self.Layout.addWidget(frame, rowIdx, columnIdx, 3, 1)

    def BuildTrimFrame(self, columnIdx: int, rowIdx: int) -> None:
        """Build frame for trimming image.

        Parameters
        ----------
        columnIdx : int
            column to place the frame inside
        rowIdx : int
            row to place frame on

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
                trimColor.text() if trimColor.text() != "" else None,
            )

        self.BuildRunButton(frame, layout, RunAction)

        self.Layout.addWidget(frame, rowIdx, columnIdx, 3, 1)

    # endregion
