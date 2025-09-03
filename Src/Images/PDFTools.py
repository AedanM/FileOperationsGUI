"""Uses poppler to merge folders into pdf files.

Install poppler -> conda install -c conda-forge poppler.
"""

from collections.abc import Generator
from contextlib import suppress
from pathlib import Path
from statistics import mode

from PIL import Image, UnidentifiedImageError
from pypdf import PdfWriter

from Src.Utilities.UtilityTools import IMG_EXTS, DeleteFolder, GenerateMessage, GenerateUniqueName


def GetFileExtensions(path: Path) -> set[str]:
    ext: set[str] = {x.suffix.replace(".", "").lower() for x in path.glob("*.*")}
    if list(path.glob("*/")):
        ext.add("/")

    return ext


def MergePDF(folderPath: Path) -> Generator[str]:
    merger = PdfWriter()
    for pdf in folderPath.glob("*.pdf"):
        merger.append(pdf)
    if list(folderPath.glob("*.pdf")):
        merger.write(folderPath.parent / (folderPath.name + ".pdf"))
        merger.close()
        yield folderPath.name + ".pdf Written"


def GetPageHeight(imgs: list[Image.Image]) -> int:
    heights = []
    for img in imgs:
        with suppress(ValueError):
            heights.append(img.size[1])
    return int(round(min(mode(heights), 2160), 0))


def CompileImages(dirPath: Path, quality: float) -> Generator[str]:
    files: list[Path] = list(dirPath.glob("*.*"))
    if len(files) > 1:
        output: list[Image.Image] = []
        imgs: list[Image.Image] = []

        try:
            imgs: list[Image.Image] = [Image.open(file).copy() for file in files]
        except UnidentifiedImageError as e:
            yield f"Unable to compile {dirPath} -> {e} {type(e)}"

        if imgs:
            height = round((GetPageHeight(imgs=imgs) * quality) / 100)
            for im in imgs:
                newWidth: int = im.size[0]
                if im.size[1] != height:
                    newWidth: int = round(im.size[0] * (height / im.size[1]))
                    im = im.resize((newWidth, height))
                output.append(im)

        if output:
            pdfPath = GenerateUniqueName(dirPath.parent / (dirPath.stem + ".pdf"))
            output[0].save(pdfPath, "PDF", save_all=True, append_images=output[1:])
            yield f"{pdfPath.name} - {len(output)} pages"

    elif len(files) == 1:
        file = files[0]
        file.rename(dirPath.parent / f"{dirPath.name}{file.suffix}")
        DeleteFolder(dirPath)
        yield f"{file.stem} simplified"
    else:
        yield f"Error with {dirPath}"


def CompileFolders(p: Path, quality: float) -> Generator[str]:
    for dirPath in [x for x in p.glob("*/") if x.stem[0] != "_"]:
        exts = GetFileExtensions(dirPath)
        if "/" in exts:
            yield from GenerateMessage(f"ERROR -> subfolder found in {dirPath}")
        elif exts == {"pdf"}:
            yield from MergePDF(dirPath)
        elif all(x in IMG_EXTS for x in exts):
            yield from CompileImages(dirPath, quality)
        else:
            yield from GenerateMessage(
                "Incompatible files found "
                f"({','.join([x for x in exts if x not in IMG_EXTS])})"
                f" -> {dirPath.stem}",
            )
