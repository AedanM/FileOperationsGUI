"""Module to check if a series of files are missing entries."""
import itertools
from collections.abc import Generator
from pathlib import Path


def DigitizeStr(inString: str) -> int:
    return int("".join([char for char in inString if char.isnumeric()]))


def MakeNumList(filePath: Path) -> list[int]:
    fileNums: set[int] = set()
    for file in [x for x in filePath.glob("**/*") if isinstance(x, Path)]:
        fileNums.add(DigitizeStr(inString=file.stem))
    return sorted(fileNums)


def Ranges(i: list[int]) -> Generator[tuple[int, int]]:
    for _a, b in itertools.groupby(enumerate(i), lambda pair: pair[1] - pair[0]):
        b = list(b)
        yield b[0][1], b[-1][1]


def CheckSequence(filePath: Path) -> list:
    numList: list[int] = MakeNumList(filePath=filePath)
    prevVal: int = numList[0]
    missingVals: list[int] = []
    for num in numList[1:]:
        if prevVal != num - 1:
            missingVals += range(prevVal + 1, num)
        prevVal = num
    return list(Ranges(missingVals))


def CheckSeq(path: Path) -> Generator[str]:
    missing = CheckSequence(path)
    if missing:
        missingList = [f"{x[0]} to {x[1]}" if x[0] != x[1] else str(x[0]) for x in missing]
        outStr = f"Missing {', '.join(missingList)}"
    else:
        numList = MakeNumList(path)
        outStr = f"Complete Sequence from {numList[0]}-{numList[-1]}"
    yield outStr
