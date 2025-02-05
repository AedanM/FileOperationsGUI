from pathlib import Path


def MakeStringSystemSafe(
    inputPath: str | Path,
    removeSpaces: bool = True,
) -> str:
    objPath: Path = Path(inputPath)
    stringPath = objPath.stem
    bannedChars = '<>:"/\\|?*'
    if removeSpaces:
        bannedChars += " "
    for bannedChar in bannedChars:
        stringPath = stringPath.replace(bannedChar, "_")

    return str(objPath.parent / (stringPath + objPath.suffix))
