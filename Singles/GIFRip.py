import sys
from pathlib import Path

from PIL import Image


def GIFToIMGSeq(path: Path):
    imageObject = Image.open(path)
    parentDir = path.parent / path.stem
    parentDir.mkdir(exist_ok=True)
    print(f"Rendering {imageObject.n_frames} frames")  # type: ignore
    for frame in range(0, imageObject.n_frames):  # type: ignore
        imageObject.seek(frame)
        imageObject.save(parentDir / f"{path.stem} {frame:03d}.png")


if __name__ == "__main__":
    p = Path(sys.argv[1])
    GIFToIMGSeq(p)
