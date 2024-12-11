import sys
from pathlib import Path

from pypdf import PdfWriter


def MergePDFs(path: Path) -> str:
    merger = PdfWriter()
    files = 0
    for pdf in path.glob("*.pdf"):
        merger.append(pdf)
        files += 1

    if files:
        merger.write(path.parent / (path.name + ".pdf"))
        merger.close()

        return path.name + ".pdf Written"
    return "No Files"


def MergePDFFolders(parentDir):
    out = ""
    for p in list(parentDir.glob("**/*")):
        if p.is_dir():
            out += "\n" + MergePDFs(p)
    return out


if __name__ == "__main__":
    parent = Path(sys.argv[1])
    MergePDFFolders(parent)
