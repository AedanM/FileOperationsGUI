"""conda install -c conda-forge poppler"""

import sys
from pathlib import Path
from statistics import median

from PIL import Image


def GetPageHeight(parentPath: Path):
    heights = []
    for img in parentPath.glob("*.*"):
        try:
            im = Image.open(img)
            heights.append(im.size[1])
        except ValueError:
            pass
    return int(round(min(median(heights), 2160), 0))


def CompilePDF(parentPath: Path, quality: float) -> tuple[str, int]:
    if parentPath.exists() and parentPath.is_dir():
        files = list(parentPath.glob("*.*"))
        if len(files) > 1:
            imgs: list[Image.Image] = []
            height = GetPageHeight(parentPath=parentPath)
            for img in sorted(
                files,
                key=lambda x: int(x.stem) if x.stem.isnumeric() else ord(str(x.stem)[0]),
            ):
                try:
                    im = Image.open(img)
                    newWidth = im.size[0]
                    if im.size[1] != height:
                        newWidth = int(round(im.size[0] * (quality / 100) * (height / im.size[1])))
                    im = im.resize((newWidth, height))  # type: ignore
                    imgs.append(im)
                except ValueError as e:
                    print(e, img)

            if imgs:
                pdfPath = parentPath.parent / (str(parentPath.stem) + ".pdf")
                imgs[0].save(pdfPath, "PDF", save_all=True, append_images=imgs[1:])
                return str(pdfPath.name), len(imgs)
        elif len(files) == 1:
            file = files[0]
            file.rename(parentPath.parent / f"{parentPath.name}{file.suffix}")
            try:
                parentPath.unlink()
            except:
                pass
    return f"Error with {parentPath}", 0


def CompileFolderToPDFs(inputPath: Path, quality: float):
    files = []
    for dirPath in [x for x in inputPath.glob("*") if x.is_dir()]:  # + [inputPath]:
        if dirPath.stem[0] != "_":
            name, length = CompilePDF(parentPath=dirPath, quality=quality)
            files.append((name, length))
    madeList = [f"\t{x[0]} - {x[1]} pages\n" for x in files]
    return f"Made:\n{''.join(madeList)}"


if __name__ == "__main__":
    inPath = Path(sys.argv[1])
    CompileFolderToPDFs(inPath, 100)
