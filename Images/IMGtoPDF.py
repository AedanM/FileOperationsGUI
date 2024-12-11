"""conda install -c conda-forge poppler"""

import sys
from pathlib import Path

from PIL import Image


def CompilePDF(parentPath: Path, quality: float) -> tuple[str, int]:
    if parentPath.exists() and parentPath.is_dir():
        imgs: list[Image.Image] = []
        for img in sorted(
            list(parentPath.glob("*.*")),
            key=lambda x: int(x.stem) if x.stem.isnumeric() else ord(str(x.stem)[0]),
        ):
            try:
                im = Image.open(img)
                newSize = [int(round(x * quality / 100)) for x in im.size]
                im = im.resize(tuple(newSize))  # type: ignore
                imgs.append(im)
            except ValueError as e:
                print(e, img)

        if imgs:
            pdfPath = parentPath.parent / (str(parentPath.stem) + ".pdf")
            imgs[0].save(pdfPath, "PDF", save_all=True, append_images=imgs[1:])
            return str(pdfPath.name), len(imgs)
    return f"Error with {parentPath}", 0


def CompileFolderToPDFs(inputPath: Path, quality: float):
    files = []
    for dirPath in [x for x in inputPath.glob("*") if x.is_dir()]:  # + [inputPath]:
        name, length = CompilePDF(parentPath=dirPath, quality=quality)
        files.append((name, length))
    madeList = [f"\t{x[0]} - {x[1]} pages\n" for x in files]
    return f"Made:\n{''.join(madeList)}"


if __name__ == "__main__":
    inPath = Path(sys.argv[1])
    CompileFolderToPDFs(inPath, 100)
