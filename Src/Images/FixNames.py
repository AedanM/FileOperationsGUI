import re
import sys
from pathlib import Path

SPACE_SUBS = ["_20", "_", "_%20", " - ", "-", "+"]


def PadFinalNum(string):
    numCount = 0
    for s in reversed(string):
        if s.isnumeric():
            numCount += 1
        else:
            break
    if numCount > 0:
        return (
            string[: len(string) - numCount].strip()
            + " "
            + f"{int(string[len(string)-numCount:]):03d}"
        )
    return string


def CamelToSentence(text: str) -> str:
    matches = re.finditer(".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)", text)
    return " ".join([m.group(0) for m in matches])


def FixNames(path: Path, globFilter):
    passed, renamed = 0, 0
    for p in path.glob(globFilter):
        newName = p.stem
        for tag in SPACE_SUBS:
            newName = newName.replace(tag, " ")
        newName = newName.strip().title()
        newName = CamelToSentence(newName)
        newName = PadFinalNum(newName)
        newName = newName.replace("'S", "'s")
        if p.stem[0] == "_" and newName[0] != "_" and p.is_dir():
            newName = "_" + newName
        if newName != p.stem:
            try:
                p.rename(p.parent / str(newName + p.suffix))
                renamed += 1
            except PermissionError:
                pass
        else:
            passed += 1
    return f"{renamed}/{passed+renamed} Renamed"


if __name__ == "__main__":
    FixNames(Path(sys.argv[1]), globFilter="*.*" if len(sys.argv) < 3 else sys.argv[2])
