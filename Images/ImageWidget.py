from pathlib import Path

from BaseWidget import BaseWidget
from Images.CheckSeq import CheckSeq
from Images.FixNames import FixNames
from Images.Flatten import Flatten
from Images.IMGtoPDF import CompileFolderToPDFs
from Images.MergePDF import MergePDFFolders
from Images.SortToFolders import SortToFolders
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QDoubleSpinBox, QLabel, QLineEdit, QTextEdit


class ImageOperationsWidget(BaseWidget):

    def __init__(self, parent):
        super().__init__(parent)

        self.OutputText = QTextEdit(self)

        masterFolderLabel = QLabel(self)
        masterFolderLabel.setText("<h1>Master Folder</h1>")
        masterFolderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.MainFolderInput = QLineEdit(self)
        inputFrame = self.BuildInputFrame(self.MainFolderInput)

        self.Layout.addWidget(masterFolderLabel, 0, 0, 1, 7)
        self.Layout.addWidget(self.OutputText, 10, 0, 1, 7)
        self.Layout.addWidget(inputFrame, 1, 0, 1, 7)

        self.BuildCheckSeqFrame(2)
        self.BuildFixNamesFrame(2)

        self.BuildSortFolderFrame(4)
        self.BuildFlattenFrame(4)

        self.BuildPDFFrame(6)
        self.BuildIMG2PDFFrame(6)

    def BuildCheckSeqFrame(self, idx):
        frame, layout = self.BuildBaseFrame(
            title="Check Seq",
            caption="Check that a sequence of files is complete",
        )

        def RunAction():
            yield CheckSeq(self.ActiveField)

        self.BuildRunButton(frame, layout, RunAction)
        self.Layout.addWidget(frame, 6, idx, 3, 1)

    def BuildSortFolderFrame(self, idx):
        frame, layout = self.BuildBaseFrame(
            title="Sort To Folders",
            caption="Sort Img sequences to Folders",
        )

        def RunAction():
            yield SortToFolders(Path(self.ActiveField))

        self.BuildRunButton(frame, layout, RunAction)
        self.Layout.addWidget(frame, 3, idx, 3, 1)

    def BuildFlattenFrame(self, idx):
        frame, layout = self.BuildBaseFrame(
            title="Flatten",
            caption="Flatten a file directory",
        )

        rename = self.AddButtonFrame(frame, layout, "Rename")
        delete = self.AddButtonFrame(frame, layout, "Delete")

        globPattern = QLineEdit(frame)
        globPattern.setPlaceholderText("Glob Pattern")
        layout.addWidget(globPattern)

        def RunAction():
            if globPattern.text() != "":
                yield Flatten(
                    Path(self.ActiveField),
                    rename.isChecked(),
                    delete.isChecked(),
                    globPattern=globPattern.text(),
                )
            else:
                yield Flatten(
                    Path(self.ActiveField),
                    rename.isChecked(),
                    delete.isChecked(),
                )

        self.BuildRunButton(frame, layout, RunAction)
        self.Layout.addWidget(frame, 6, idx, 3, 1)

    def BuildPDFFrame(self, idx):
        frame, layout = self.BuildBaseFrame(
            title="Compile To PDF",
            caption="Convert Img Sequence to PDF</p><p>At % resolution",
        )

        resolutionBox = QDoubleSpinBox(frame)
        resolutionBox.setMaximum(100.01)
        resolutionBox.setValue(100.0)
        layout.addWidget(resolutionBox)

        def RunAction():
            yield CompileFolderToPDFs(
                Path(self.ActiveField),
                resolutionBox.value(),
            )

        self.BuildRunButton(frame, layout, RunAction)
        self.Layout.addWidget(frame, 3, idx, 3, 1)

    def BuildIMG2PDFFrame(self, idx):
        frame, layout = self.BuildBaseFrame(
            title="Merge PDFs",
            caption="Merge PDFs in folders",
        )

        def RunAction():
            yield MergePDFFolders(Path(self.ActiveField))

        self.BuildRunButton(frame, layout, RunAction)

        self.Layout.addWidget(frame, 6, idx, 3, 1)

    def BuildFixNamesFrame(self, idx):
        frame, layout = self.BuildBaseFrame(
            title="Fix Names",
            caption="Apply Naming Rules",
        )

        globFilter = QLineEdit(frame)
        globFilter.setPlaceholderText("Glob Pattern")
        layout.addWidget(globFilter)

        def RunAction():
            yield FixNames(
                Path(self.ActiveField),
                globFilter.text() if globFilter.text() != "" else "*.*",
            )

        self.BuildRunButton(frame, layout, RunAction)
        self.Layout.addWidget(frame, 3, idx, 3, 1)
