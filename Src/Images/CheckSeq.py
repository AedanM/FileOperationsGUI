import itertools
from pathlib import Path


def DigitizeStr(inString: str) -> int:
    outChars = []
    for char in inString:
        if char.isnumeric():
            outChars.append(char)
    return int("".join(outChars))


def MakeNumList(filePath):
    fileNums: set[int] = set()
    for file in Path(filePath).glob("**/*"):
        if isinstance(file, Path):
            fileNums.add(DigitizeStr(inString=file.stem))
    return sorted(list(fileNums))


def Ranges(i):
    for _a, b in itertools.groupby(enumerate(i), lambda pair: pair[1] - pair[0]):
        b = list(b)
        yield b[0][1], b[-1][1]


def CheckSequence(filePath) -> list:
    numList = MakeNumList(filePath=filePath)
    prevVal = None
    missingVals: list[int] = []
    for num in numList:
        if prevVal is not None and prevVal != num - 1:
            missingVals += range(prevVal + 1, num)
        prevVal = num

    return list(Ranges(missingVals))


def CheckSeq(fp):
    missing = CheckSequence(fp)
    if missing:
        missingList = [f"{x[0]} to {x[1]}" if x[0] != x[1] else str(x[0]) for x in missing]
        outStr = f"Missing {', '.join(missingList)}"
    else:
        numList = MakeNumList(fp)
        outStr = f"Complete Sequence from {numList[0]}-{numList[-1]}"
    return outStr
