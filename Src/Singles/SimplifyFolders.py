"""Simplify a directory by removing folders with single files, or multiple duplicates."""

import sys
from collections.abc import Generator
from pathlib import Path

from Src.Utilities.UtilityTools import ComputeHash, DeleteFolder, GenerateUniqueName


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
        if AllEqualFiles(dirPath):
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
            if DeleteFolder(dirPath):
                yield str(files[0])
            else:
                yield (f"Could not delete -> {dirPath}")


if __name__ == "__main__":
    for r in Simplify(Path(sys.argv[1])):
        print(r)
