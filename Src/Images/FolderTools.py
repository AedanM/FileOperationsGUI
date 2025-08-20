"""Module to flatten and simplify directories."""

import re
import shutil
from collections.abc import Generator
from pathlib import Path

from Src.Utilities.UtilityTools import ComputeHash, DeleteFolder, GenerateUniqueName


def SortToFolders(p: Path, simplifyFirst: bool, minCount: int = 1) -> Generator[str]:
    """Sort files by file name into folders (file 1, file 2, file 3 -> /file).

    Parameters
    ----------
    p : Path
        _description_
    minCount : int, optional
        _description_, by default 1

    Yields
    ------
    Generator[str]
        _description_
    """
    if simplifyFirst:
        yield from Simplify(p)

    files: list[Path] = list(p.glob("*.*"))
    seqs: set[str] = set()
    for file in files:
        if file.stem.strip()[-1].isnumeric():
            seqs.add(" ".join(file.stem.split(" ")[:-1]))
    for seq in seqs:
        folder = p / seq
        sequenceFiles = [x for x in files if re.search(rf"{seq}\s?\d+", x.name)]
        if len(sequenceFiles) > minCount or folder.exists():
            folder.mkdir(parents=True, exist_ok=True)
            for file in sequenceFiles:
                file.replace(folder / file.name)
            yield f"{seq} -> {len(sequenceFiles)} Files"


def Flatten(
    p: Path,
    rename: bool = False,
    delete: bool = False,
    globPattern: str = "**/*.*",
) -> Generator[str]:
    """Flatten a nested pattern of folders.

    Parameters
    ----------
    p : Path
        parent path
    rename : bool, optional
        true if folder name is to be prefixed, by default False
    delete : bool, optional
        true if files are to be deleted, by default False
    globPattern : str, optional
        glob matching pattern, by default "**/*.*"

    Yields
    ------
    Generator[str]
        status strings
    """
    for folder in p.glob(globPattern):
        if folder.parent != p:
            dst: Path = p / f"{folder.parent.stem + ' ' if rename else ''}{folder.name}"
            if delete:
                folder.rename(dst)
            else:
                shutil.copyfile(str(folder), str(dst))
    if delete and globPattern in ["**/*.*"]:
        for folder in p.glob("**/*/"):
            DeleteFolder(folder)
    yield f"{len(list(p.glob(globPattern)))} Files moved to {p.name}" + (
        f"\n{len(list(p.glob('**/*/')))} Folders Removed" if delete else ""
    )


def AllEqualFiles(folder: Path) -> bool:
    """Determine if all files in a folder are the same."""
    if not folder:
        return False
    files = [p for p in folder.iterdir() if p.is_file()]

    if len(files) <= 1:
        return True

    firstHash = ComputeHash(files[0])
    return all(ComputeHash(other) == firstHash for other in files[1:])


def Simplify(inputPath: Path) -> Generator[str]:
    """Reduce folder structure in directory."""
    folderList: list[Path] = [x for x in inputPath.glob("*") if x.is_dir() and x.stem[0] != "_"]
    for dirPath in folderList:
        files: list[Path] = list(dirPath.glob("*.*"))
        if files and AllEqualFiles(dirPath):
            masterFile: Path = files[0]
            dst: Path = dirPath.parent / f"{dirPath.name}{masterFile.suffix}"
            if dst.exists() and ComputeHash(masterFile) == ComputeHash(dst):
                pass
            elif not dst.exists():
                masterFile.rename(dst)
            else:
                dst: Path = GenerateUniqueName(
                    dirPath.parent / f"{dirPath.name}{masterFile.suffix}",
                )
                masterFile.rename(dst)
                raise FileExistsError(masterFile, dst)
            if not DeleteFolder(dirPath):
                yield (f"Could not delete -> {dirPath}")
