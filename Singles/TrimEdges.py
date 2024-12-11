import sys
from pathlib import Path

import numpy as np
from PIL import Image


def TrimEdge(imgPath: Path, keyColor=None):
    if keyColor is None:
        keyColor = [0, 0, 0]
    keyColor = np.array(keyColor)
    try:
        image = Image.open(imgPath).convert("RGB")
    except ValueError:
        return 0

    imgArr = np.array(image)
    colorPxl = np.any(imgArr != keyColor, axis=-1)

    if np.any(colorPxl):
        coords = np.argwhere(colorPxl)
        yMin, xMin = coords.min(axis=0)
        yMax, xMax = coords.max(axis=0) + 1  # +1 to include the max bound
        image = image.crop((xMin, yMin, xMax, yMax))
    image.save(str(imgPath))
    return 1


def TrimAllEdges(parent, keyColor=None):
    files = parent.glob("**/*.*") if parent.is_dir() else [parent]
    successCount, fullCount = 0, 0
    for file in files:
        if file.is_file():
            fullCount += 1
            successCount += TrimEdge(file, keyColor)
    return f"{successCount}/{fullCount} Trimmed in Place"


if __name__ == "__main__":
    p = Path(r"D:\NP\Abimboleb\PDF")
    TrimAllEdges(p, [255, 255, 255])
