"""Module to apply naming rules."""

import contextlib
import re
import sys
from collections.abc import Generator
from pathlib import Path

from Src.Utilities.UtilityTools import GenerateUniqueName


def PadFinalNum(name: str) -> str:
    """Format names to have a final number padded if applicable.

    Parameters
    ----------
    name : str
        input name (format Name1)

    Returns
    -------
    str
        Formatted name (format Name 001)
    """
    if match := re.search(r"(\d+)$", name):
        num = int(match.group(1))
        prefix = name[: match.start()].strip()
        return f"{prefix} {num:03d}"
    return name


def CamelToSentence(text: str) -> str:
    """Convert a CamelCase string to Camel Case.

    Parameters
    ----------
    text : str
        input CamelCase string

    Returns
    -------
    str
        spaced string
    """
    matches = re.finditer(".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)", text)
    return " ".join([m.group(0) for m in matches])


def FixSpaceSubs(name: str) -> str:
    """Fix common space replacements used on the internet.

    Parameters
    ----------
    name : str
        unformatted name

    Returns
    -------
    str
        formatted name
    """
    SPACE_SUBS = ["_20", "_%20", "_", " - ", "-", "+"]
    outName: str = name
    for tag in SPACE_SUBS:
        outName: str = outName.replace(tag, " ")
    return outName


def FixContractions(name: str) -> str:
    """Fix issues with str.title() which mean I've becomes I'Ve.

    Parameters
    ----------
    name : str
        errant string

    Returns
    -------
    str
        formatted string
    """
    outStr: str = name
    for match in re.finditer(r"'[A-Z]{1}", outStr):
        outStr = outStr.replace(match.group(), match.group().lower())
    return outStr


def RemoveBannedPhrases(name: str) -> str:
    """Remove banned bits from file names.

    Parameters
    ----------
    name : str
        input name

    Returns
    -------
    str
        formatted name
    """
    banned: list[str] = [
        r"\s(P)\s?\d*$",
        r"\s(Pg)\s?\d*$",
        r"\s(Part)\s\d*$",
        r"\s(Part)$",
        r"\s(Pt)\s?\d*$",
        r"\s(Chapter)\s?\d*$",
        r"\s(Commission)\s?",
        r"\s(Tgtf)\s?",
        r"\s(Comm)\s?",
        r"\s(Ch)\s?\d",
        r"\s(#\d?)\d",
        r"(\s{2,})",
        r" (\()",
        r"(\))\s?",
        rf"(\.{2, 50})",
    ]
    outName = name

    for b in banned:
        if m := re.search(b, outName):
            outName = outName.replace(m.group(1), "")
    return outName


def FixNames(path: Path, globFilter: str = "*.*") -> Generator[str]:
    """Fix names according to preferences.

    Parameters
    ----------
    path : Path
        parent path of files
    globFilter : str
        glob pattern to match files

    Returns
    -------
    str
        corrected names
    """
    renamed: int = 0
    totalFiles: int = len(list(path.glob(globFilter)))
    for p in path.glob(globFilter):
        newName = FixSpaceSubs(p.stem.strip())
        newName = CamelToSentence(newName)
        newName = newName.strip().title()
        newName = FixContractions(newName)
        newName = RemoveBannedPhrases(newName)
        newName = re.sub(r"\s+", " ", newName)
        newName = PadFinalNum(newName).strip()
        if p.stem[0] == "_" and newName[0] != "_" and p.is_dir():
            newName = "_" + newName

        if newName != p.stem:
            dst = p.parent / str(newName + p.suffix)
            if dst.exists() and dst != p:
                dst = GenerateUniqueName(p.parent / str(newName + p.suffix))
            with contextlib.suppress(OSError):
                p.rename(dst)
                renamed += 1
        updateRate: int = max(round(totalFiles / 3), 1) if totalFiles > 100 else totalFiles
        if (renamed % updateRate) == 0 and renamed > 0:
            yield f"Progress -> {renamed}/{totalFiles}"

    yield f"{renamed}/{totalFiles} Renamed"


if __name__ == "__main__":
    FixNames(Path(sys.argv[1]), globFilter="*.*" if len(sys.argv) < 3 else sys.argv[2])
