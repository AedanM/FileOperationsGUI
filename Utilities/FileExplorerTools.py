from pathlib import Path


def MakeStringSystemSafe(
    inputPath: str,
    isFullPath: bool = False,
    removeSpaces: bool = True,
) -> str:
    stringPath = inputPath
    objPath: Path = Path(stringPath)
    keepCharacters = (".", "_", "\\", "/", ":", " ", "-") if isFullPath else (".", "_", " ", "-")

    if str(Path.stem).count(".") > 0:
        ext = objPath.suffix
        stringPath = (str(objPath) if not ext else str(objPath).replace(ext, "")).replace(
            ".", ""
        ) + ext

    if removeSpaces:
        stringPath = stringPath.replace(" ", "_") if removeSpaces else ""

    return "".join(c for c in stringPath if c.isalnum() or c in keepCharacters).rstrip()
