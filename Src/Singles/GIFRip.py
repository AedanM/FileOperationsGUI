import sys
from pathlib import Path

from PIL import Image


def GIFToIMGSeq(path: Path, subDir: bool):
    imageObject = Image.open(path)
    parentDir = path.parent / path.stem if subDir else path.parent
    parentDir.mkdir(exist_ok=True)
    for frame in range(0, imageObject.n_frames):  # type: ignore
        imageObject.seek(frame)
        imageObject.save(parentDir / f"{path.stem} {frame:03d}.png")
    return f"Rendered {imageObject.n_frames} frames to {parentDir}"  # type: ignore


if __name__ == "__main__":
    p = Path(sys.argv[1])
    GIFToIMGSeq(p, False)
