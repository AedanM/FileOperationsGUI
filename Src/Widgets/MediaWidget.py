"""Media alteration widget."""

from collections.abc import Generator

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QLineEdit, QRadioButton, QTextEdit, QWidget

from Src.Media.GetEpisodeTitles import LoadEpisodes
from Src.Media.Titles import AppendTitles, RunTitleEdit
from Src.Widgets.BaseWidget import BaseWidget


class MediaWidget(BaseWidget):
    """Widget for media altering, movies etc."""

    def __init__(self, parent: QWidget) -> None:
        super().__init__(parent)
        self.OutputText = QTextEdit(self)
        masterFolderLabel = QLabel(self)
        masterFolderLabel.setText("<h1>Master Folder</h1>")
        self.MainFolderInput = QLineEdit(self)
        masterFolderLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        inputFrame = self.BuildInputFrame(self.MainFolderInput)
        self.Layout.addWidget(masterFolderLabel, 0, 0, 1, 7)
        self.Layout.addWidget(self.OutputText, 10, 0, 1, 7)
        self.Layout.addWidget(inputFrame, 1, 0, 1, 7)
        self.BuildAppendFrame(0)
        self.BuildLoadEpisodes(2)
        self.BuildTitleEditFrame(6)

    # region Constructors

    def BuildAppendFrame(self, columnIdx: int) -> None:
        frame, layout = self.BuildBaseFrame(
            title="Append Titles",
            caption="Use Scraped Titles to Append Filenames",
        )

        self.AppendTitle = QLineEdit(frame)
        self.AppendTitle.setPlaceholderText("Show Title")

        self.EpisodeFolder = QLineEdit(frame)
        self.EpisodeFolder.setText(r".\Episode Listings")

        episodeFrame = self.BuildInputFrame(self.EpisodeFolder)
        layout.addWidget(self.AppendTitle)
        layout.addWidget(episodeFrame)

        def RunAction() -> Generator[str]:
            yield AppendTitles(
                self.ActiveField,
                self.AppendTitle.text(),
                self.EpisodeFolder.text(),
            )

        self.BuildRunButton(frame, layout, RunAction)
        self.Layout.addWidget(frame, 3, columnIdx, 6, 1)  #

    def BuildLoadEpisodes(self, columnIdx: int) -> None:
        frame, layout = self.BuildBaseFrame(
            title="Load Episodes",
            caption="Scrape wikipedia to load episode titles",
        )

        showFrame = QFrame(self)
        showLayout = QHBoxLayout(showFrame)
        isShowLabel = QLabel(frame)
        isShowLabel.setText("Use exact page (List of... etc)")
        self.IsShow = QRadioButton(frame)
        showLayout.addWidget(isShowLabel)
        showLayout.addWidget(self.IsShow)

        self.ContentTitle = QLineEdit(frame)
        self.ContentTitle.setPlaceholderText("Show Title")
        layout.addWidget(self.ContentTitle)
        layout.addWidget(showFrame)

        def RunAction() -> Generator[str]:
            yield LoadEpisodes(topic=self.ContentTitle.text(), _isShow=self.IsShow.isChecked())

        self.BuildRunButton(frame, layout, RunAction)

        self.Layout.addWidget(frame, 3, columnIdx, 6, 1)

    def BuildTitleEditFrame(self, columnIdx: int) -> None:
        frame, layout = self.BuildBaseFrame(
            title="Title Edit",
            caption="Reformat Metadata based on File Name",
        )

        def RunAction() -> Generator[str]:
            yield RunTitleEdit(self.ActiveField)

        self.BuildRunButton(frame, layout, RunAction)

        self.Layout.addWidget(frame, 3, columnIdx, 3, 1)

    # endregion
