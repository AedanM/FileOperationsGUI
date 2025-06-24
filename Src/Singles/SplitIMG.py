import sys
from math import floor
from pathlib import Path

from PIL import Image


def SplitIMG(imagePath: Path, gridDim: list, makeSubDir: bool = False):
    imgs = list(imagePath.glob("*.*")) if imagePath.is_dir() else [imagePath]
    print(imgs)
    outPut = ""
    for imgPath in imgs:
        image = Image.open(imgPath)
        if len(gridDim) == 1:
            if image.size[0] > image.size[1]:
                gridDim.append(1)
            else:
                gridDim = [1] + gridDim
        outPut += "\n" + SplitGrid(imgPath, gridDim, image, makeSubDir)
    return outPut


def SplitGrid(parentPath: Path, gridSize: list, image: Image.Image, subDir: bool):
    x, y = gridSize[:2]
    width, height = image.size
    imCount = 0
    if subDir and not (parentPath.parent / parentPath.stem).exists():
        (parentPath.parent / parentPath.stem).mkdir(exist_ok=True)
    for i in range(y):
        row = i % y
        top = floor(height * (row / y))
        bottom = floor(height * ((row + 1) / y)) - 1
        for j in range(x):
            col = j % x
            cropped = image.crop(
                (
                    floor(width * (col / x)),
                    top,
                    floor(width * ((col + 1) / x)) - 1,
                    bottom,
                )
            )
            imCount += 1
            dstPath = parentPath.parent if not subDir else parentPath.parent / parentPath.stem
            cropped.save(dstPath / f"{parentPath.stem} {imCount:02d}.png")

    return f"{imCount}/{x * y} Saved In {parentPath.name}"


# if __name__ == "__main__":
#     path = Path(sys.argv[1])
#     grid = [int(x) for x in sys.argv[2].split("x")]
#     SplitIMG(path, grid)

if __name__ == "__main__":
    path = Path(sys.argv[1])
    grid = [int(x) for x in sys.argv[2].split("x")]
    SplitIMG(path, grid)
