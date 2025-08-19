"""Utility tools for file gui."""

import hashlib
from collections.abc import Callable, Generator
from functools import wraps
from pathlib import Path
from time import time
from typing import Any

VIDEO_EXTS: list[str] = ["mkv", "mp4", "avi", "webm"]
IMG_EXTS: list[str] = ["png", "bmp", "webp", "ico", "jpeg", "jpg", "tiff", "heic"]


def DeleteFolder(path: Path) -> bool:
    if not path.is_dir():
        return False
    for file in path.iterdir():
        if file.is_dir():
            DeleteFolder(file)
        else:
            file.unlink()
    path.rmdir()
    return True


def ComputeHash(path: Path) -> bytes:
    h = hashlib.new("sha256")
    with path.open("rb") as f:
        while chunk := f.read(8196):
            h.update(chunk)
    return h.digest()


def TimeUtility(repetitions: int = 10000, returnResults: bool = False) -> Callable:
    def TimeMethod(func: Callable) -> Callable:
        @wraps(func)
        def Wrap(*args: Any, **kw: Any) -> list[float] | None:
            totalTime = 0
            results = []
            for iteration in range(repetitions):
                ts = time()
                runResult = func(*args, **kw)
                te = time()
                results.append(runResult)
                totalTime += float(te - ts)
                if iteration % (repetitions // 10) == 0:
                    print(f"{iteration}/{repetitions} - {iteration / repetitions * 100}%")
                return results if returnResults else None
            print(
                f"Method {func.__name__} took {totalTime:0.3f}s over {repetitions} reps"  # type:ignore[unresolvedAttribute]
                f" with an average time of {(totalTime / repetitions) * 1000:2.4f} ms",
            )

        return Wrap

    return TimeMethod


def GenerateMessage(message: str) -> Generator[str]:
    yield message


def CheckAgainstList(item: Any, tags: list[str]) -> bool:
    return any(tag in str(item) for tag in tags)


def MakeStringSystemSafe(
    inputPath: str | Path,
    removeSpaces: bool = False,
) -> str:
    objPath: Path = Path(inputPath)
    stringPath = objPath.stem
    bannedChars = '<>:"/\\|?*'
    if removeSpaces:
        bannedChars += " "
    for bannedChar in bannedChars:
        stringPath = stringPath.replace(bannedChar, "_")

    return str(objPath.parent / (stringPath + objPath.suffix))


def GetAllVideos(inputPath: Path) -> list[Path]:
    """Get all video files across multiple extensions.

    Parameters
    ----------
    inputPath : Path
        path to directory

    Returns
    -------
    list[Path]
        list of video files in directory
    """
    outList = []
    if inputPath.is_file():
        outList = [inputPath]
    else:
        for ext in VIDEO_EXTS:
            outList += list(inputPath.glob(f"*.{ext}"))
    return outList


def GenerateUniqueName(filePath: Path) -> Path:
    """Generate a unique filename for a file if it already exists.

    Parameters
    ----------
    filePath : Path
        file path to test

    Returns
    -------
    Path
        unique file path
    """
    count = 1
    outPath: Path = filePath
    while outPath.exists():
        outPath = outPath.parent / f"{outPath.stem} {count:03d}{outPath.suffix}"
        count += 1
    return outPath


def DigitizeStr(inString: str) -> int:
    return int("".join([char for char in inString if char.isnumeric()]))
