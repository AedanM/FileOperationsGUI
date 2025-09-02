"""Doc to trim borders from images."""

import sys
from collections.abc import Generator
from pathlib import Path
from typing import Any

from PIL import Image, UnidentifiedImageError

CONFIG = {
    "BORDER_COLOR": [255, 255, 255],
    "TOLERANCE": 10,
    "PADDING": 0,
    "AUTO": True,
}


def IsBorder(pixel: tuple) -> bool:
    return all(abs(pixel[i] - CONFIG["BORDER_COLOR"][i]) <= CONFIG["TOLERANCE"] for i in range(3))


def DetermineBoundary(
    pixels: Any,
    width: int,
    height: int,
) -> tuple[int, int, int, int]:
    top = 0
    for y in range(height):
        if any(not IsBorder(pixels[x, y]) for x in range(width)):
            break
        top += 1

    bottom = height - 1
    for y in range(height - 1, -1, -1):
        if any(not IsBorder(pixels[x, y]) for x in range(width)):
            break
        bottom -= 1

    left = 0
    for x in range(width):
        if any(not IsBorder(pixels[x, y]) for y in range(height)):
            break
        left += 1

    right = width - 1
    for x in range(width - 1, -1, -1):
        if any(not IsBorder(pixels[x, y]) for y in range(height)):
            break
        right -= 1
    return top, bottom, left, right


def StripBorders(
    image_path: Path,
    border_color: None | str = None,
    save_path: Path | None = None,
) -> bool:
    """Strip uneven borders from an image based on a given border color, with optional tolerance.

    Args:
        image_path (str): Path to the input image.
        border_color (tuple): RGB tuple of the border to remove (e.g (255, 255, 255) for white)
        save_path (str, optional): Path to save the processed image. If None, does not save.

    Returns
    -------
        Image: Pillow Image object without the border.
    """
    img = Image.open(image_path).convert("RGB")
    pixels = img.load()
    if pixels is None:
        raise UnidentifiedImageError(image_path)

    if isinstance(border_color, str):
        CONFIG["BORDER_COLOR"] = [int(x) for x in border_color.split(",")]
        CONFIG["AUTO"] = False
    if CONFIG["AUTO"]:
        CONFIG["BORDER_COLOR"] = pixels[0, 0]

    width, height = img.size

    # Determine crop boundaries
    top, bottom, left, right = DetermineBoundary(pixels, width, height)
    # Crop the image
    cropped = img.crop(
        (
            max(0, left - CONFIG["PADDING"]),
            max(0, top - CONFIG["PADDING"]),
            min(right + 1 + CONFIG["PADDING"], width),
            min(bottom + 1 + CONFIG["PADDING"], height),
        ),
    )
    if save_path and cropped.size != img.size:
        print(f"Saved to {save_path.stem}")
        cropped.save(save_path)
        return True
    return False


def TrimAllEdges(path: Path, color: str | None = None) -> Generator[str]:
    files = list(path.glob("*.*"))
    failed = 0
    for file in files:
        try:
            if not StripBorders(
                image_path=file,
                border_color=color,
                save_path=file,
            ):
                failed += 1
        except UnidentifiedImageError as e:
            failed + 1  # type: ignore[reportUnusedExpression]
            yield f"Error {e} -> {file}"
    yield f"{len(files) - failed}/{len(files)} trimmed"


if __name__ == "__main__":
    p = Path(sys.argv[1])
    print(TrimAllEdges(p, None))
