import csv
import re
from pathlib import Path

import Src.Utilities.FileExplorerTools as fe


def AppendTitles(mediaFolder, title, episodeFolder):
    episodeTitles = LoadTitles(title, episodeFolder)
    if episodeTitles:
        renameCount = 0
        filesToChange = list(Path(mediaFolder).glob("**/*.*"))
        for file in filesToChange:
            # Expected Format is (Title SXXEXX.XX)
            file = Path(file) if not isinstance(file, Path) else file
            if epAndSeason := re.search(pattern=r"S\d\dE\d\d", string=file.stem):
                try:
                    start = epAndSeason.regs[0][0]
                    end = epAndSeason.regs[0][1]
                    epAndSeason = file.stem[start:end]
                    if episodeTitles[epAndSeason] not in file.stem:
                        newName = file.stem.replace(
                            epAndSeason, f"{epAndSeason} {episodeTitles[epAndSeason]}"
                        )
                        file.rename(Path(file.parent) / (newName + file.suffix))
                        renameCount += 1

                # pylint: disable=W0718
                except Exception as e:
                    print(f"{file.stem} not modified because of {e}")

        return f"{renameCount}/{len(filesToChange)} files renamed"
    return "Episode Titles Not Found"


def LoadTitles(title, episodeFolder) -> dict[str, str]:
    try:
        episodeTitlesCSV = f"{fe.MakeStringSystemSafe(inputPath=title)}_Episodes.csv"
        episodeCSVPath = Path(episodeFolder) / episodeTitlesCSV
        with episodeCSVPath.open(mode="r") as fp:
            episodeTitles = dict(csv.reader(fp))
    except FileNotFoundError:
        episodeTitlesCSV = f"{fe.MakeStringSystemSafe(inputPath=title)}_TV_Series_Episodes.csv"
        episodeCSVPath = Path(episodeFolder) / episodeTitlesCSV
        with episodeCSVPath.open(mode="r") as fp:
            episodeTitles = dict(csv.reader(fp))
    return episodeTitles


if __name__ == "__main__":
    FOLDER = r"H:\DownloadBuffer\Season 01"
    TITLE = r"Adventures_of_Superman"
    EP_FOLDER = r".\Temp\Episodes"
    AppendTitles(mediaFolder=FOLDER, title=TITLE, episodeFolder=EP_FOLDER)
