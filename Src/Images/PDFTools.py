"""Uses poppler to merge folders into pdf files.

Install poppler -> conda install -c conda-forge poppler.
"""

from collections.abc import Generator
from pathlib import Path
from statistics import mode

from PIL import Image
from pypdf import PdfWriter

from Src.Utilities.UtilityTools import DeleteFolder, GenerateUniqueName


def MergePDF(parentDir: Path) -> Generator[str]:
    for p in [x for x in parentDir.glob("**/*") if x.is_dir()]:
        merger = PdfWriter()
        for pdf in p.glob("*.pdf"):
            merger.append(pdf)
        if list(p.glob("*.pdf")):
            merger.write(p.parent / (p.name + ".pdf"))
            merger.close()
            yield p.name + ".pdf Written"


def GetPageHeight(parentPath: Path) -> int:
    heights = []
    for img in parentPath.glob("*.*"):
        try:
            im = Image.open(img)
            heights.append(im.size[1])
        except ValueError:
            pass
    return int(round(min(mode(heights), 2160), 0))


def CompileImages(p: Path, quality: float) -> Generator[str]:
    for dirPath in [x for x in p.glob("*/") if x.stem[0] != "_"]:
        files: list[Path] = list(dirPath.glob("*.*"))

        if len(files) > 1:
            imgs: list[Image.Image] = []
            height: int = round((GetPageHeight(parentPath=dirPath) * quality) / 100)
            for img in sorted(files):
                im: Image.Image = Image.open(img)
                newWidth: int = im.size[0]
                if im.size[1] != height:
                    newWidth: int = round(im.size[0] * (height / im.size[1]))
                    im = im.resize((newWidth, height))
                imgs.append(im)

            if imgs:
                pdfPath = GenerateUniqueName(dirPath.parent / (dirPath.stem + ".pdf"))
                imgs[0].save(pdfPath, "PDF", save_all=True, append_images=imgs[1:])
                yield f"{pdfPath.name} - {len(imgs)} pages"

        elif len(files) == 1:
            file = files[0]
            file.rename(dirPath.parent / f"{dirPath.name}{file.suffix}")
            DeleteFolder(dirPath)
            yield f"{file.stem} simplified"
        else:
            yield f"Error with {dirPath}"
