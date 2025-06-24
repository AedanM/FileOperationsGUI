import sys
from pathlib import Path

from PIL import Image

COLOR: tuple = (0, 0, 0)
TOLERANCE: float = 0.02
BUFFER = 5


def CheckRow(pixels, rangeVal, index, switch=False):
    miss = 0
    match = 0
    for idx in range(rangeVal):
        try:

            if tuple(pixels[index, idx] if switch else pixels[idx, index]) != tuple(COLOR):
                miss += 1
            else:
                match += 1

        except Exception as e:
            print(idx, index, e)
            exit(1)
    return miss / (miss + match)


def TrimEdge(imgPath):
    global COLOR

    img = Image.open(imgPath).convert("RGB")
    width, height = img.size
    if width == 0 or height == 0:
        return img
    pixels = img.load()
    top = 0
    if COLOR is None:
        COLOR = tuple(pixels[0, 0])
    while top < height:
        if CheckRow(pixels, width, top) < TOLERANCE:
            top += 1
        else:
            break

    bottom = height - 1
    while bottom >= top:
        if CheckRow(pixels, width, bottom) < TOLERANCE:
            bottom -= 1
        else:
            break

    if top > bottom:
        left, right = 0, -1
    else:
        left = 0
        while left < width:
            if CheckRow(pixels, bottom + 1, left, True) < TOLERANCE:
                left += 1
            else:
                break

        right = width - 1
        while right >= left:
            if CheckRow(pixels, bottom + 1, right, True) < TOLERANCE:
                right -= 1
            else:
                break
    top = max(top - BUFFER, 0)
    left = max(left - BUFFER, 0)
    bottom = min(bottom + BUFFER, height)
    right = min(right + BUFFER, width)
    if top > bottom or left > right:
        box = (0, 0, 0, 0)
    else:
        box = (left, top, right + 1, bottom + 1)
    img = img.crop(box)
    img.save(imgPath)
    return 1


def TrimAllEdges(parent, keyColor: tuple = (255, 255, 255)):
    global COLOR
    COLOR = keyColor
    files = parent.glob("**/*.*") if parent.is_dir() else [parent]
    successCount, fullCount = 0, 0
    for file in files:
        if file.is_file():
            fullCount += 1
            try:
                successCount += TrimEdge(file)
            except Exception as e:
                print(f"{file} Failed with {e}")
    return f"{successCount}/{fullCount} Trimmed in Place"


if __name__ == "__main__":
    p = Path(sys.argv[1])
    print(TrimAllEdges(p, None))
