"""Decomposing files into composite parts."""

from collections.abc import Generator
from math import floor
from pathlib import Path

from cv2 import CAP_PROP_FPS, CAP_PROP_FRAME_COUNT, CAP_PROP_POS_FRAMES, VideoCapture, imwrite
from pdf2image import convert_from_path
from PIL import Image

from Src.Utilities.UtilityTools import GetAllVideos


def DecompileVideo(
    inputPath: Path,
    startTime: float = -1,
    endTime: float = -1,
    makeSubDir: bool = True,
) -> Generator[str]:
    """Convert a video section to png sequence.

    Parameters
    ----------
    inputPath : Path
        path to video file or sequence of video files
    startTime : float
        beginning of clip
    endTime : float
        end of clip
    makeSubDir: bool
        create subdirectory for images

    Yields
    ------
    Generator[str]
        status string
    """
    for videoPath in GetAllVideos(inputPath):
        dst = (inputPath / videoPath.stem) if makeSubDir else videoPath.parent
        if not dst.exists():
            dst.mkdir(parents=True)

        # Capture the video
        video = VideoCapture(videoPath)

        # Check if the video opened successfully
        if not video.isOpened():
            yield (f"Error: Could not open video {videoPath}.")

        fps: int = video.get(CAP_PROP_FPS)
        startFrame: int = int(startTime * fps) if startTime > 0 else 0
        endFrame: int = int(endTime * fps) if endTime > 0 else video.get(CAP_PROP_FRAME_COUNT)

        video.set(CAP_PROP_POS_FRAMES, startFrame)

        frameNum: int = startFrame
        while frameNum <= endFrame:
            ret, frame = video.read()
            if not ret:
                break

            imwrite(dst / f"{videoPath.stem} {frameNum:04d}.jpg", frame)
            frameNum += 1

        video.release()
        yield f"Extracted {endFrame - startFrame} frames to {dst}"


def DecompilePDF(inputPath: Path, makeSubdir: bool) -> Generator[str]:
    """Convert pdf files to png sequences.

    Parameters
    ----------
    inputPath : Path
        pdf file or path to folder of pdf files

    Yields
    ------
    Generator[str]
        status string
    """
    pdfList: list[Path] = list(inputPath.glob("*.pdf")) if inputPath.is_dir() else [inputPath]

    for pdf in pdfList:
        if makeSubdir:
            dst = Path(str(pdf).replace(".pdf", ""))
            if dst.exists():
                dst = dst.parent / (dst.name + " PDF")
                dst.mkdir(exist_ok=True)
            else:
                dst.mkdir()
        else:
            dst = pdf.parent

        _pages = convert_from_path(
            pdf_path=pdf,
            fmt="png",
            output_file=f"{dst.name.replace(' PDF', '')} ",
            output_folder=dst,
        )

        yield f"{dst.parent.name}\\{dst.name}"


def DecompileGIF(inputPath: Path, renderToSubDir: bool = False) -> Generator[str]:
    """Convert a GIF file to a sequence of png.

    Parameters
    ----------
    inputPath : Path
        gif file or directory of gif files
    renderToSubDir : bool, optional
        should the output be grouped to a subdir, by default False

    Yields
    ------
    Generator[str]
        status string
    """
    gifList: list[Path] = list(inputPath.glob("*.gif")) if inputPath.is_dir() else [inputPath]
    for path in gifList:
        print(path)
        imageObject: Image.Image = Image.open(path)
        parentDir: Path = path.parent / path.stem if renderToSubDir else path.parent
        parentDir.mkdir(exist_ok=True)
        for frame in range(imageObject.n_frames):  # type: ignore[reportAttributeAccessIssue]
            imageObject.seek(frame)
            imageObject.save(parentDir / f"{path.stem} {frame:03d}.png")
        yield f"Rendered {imageObject.n_frames} frames to {parentDir}"  # type: ignore[reportAttributeAccessIssue]


def SplitIMG(imagePath: Path, gridDim: list[int], makeSubDir: bool = False) -> Generator[str]:
    """Split an image into sub images by a grid.

    Parameters
    ----------
    imagePath : Path
        input image or directory of images
    gridDim : list
        dimensions of grid
    makeSubDir : bool, optional
        should the output be grouped to a subdir, by default False

    Yields
    ------
    Generator[str]
        status string
    """
    imgs: list[Path] = list(imagePath.glob("*.*")) if imagePath.is_dir() else [imagePath]
    for imgPath in imgs:
        image: Image.Image = Image.open(imgPath)
        if len(gridDim) == 1:
            # Add 1-D handling
            finalDim: list[int] = [1, *gridDim] if image.size[0] > image.size[1] else [*gridDim, 1]
        else:
            finalDim: list[int] = gridDim
        image.close()
        yield SplitGrid(imgPath, finalDim, makeSubDir)


def SplitGrid(imagePath: Path, gridSize: list, createSubDir: bool) -> str:
    """Split an image to grid dimensions.

    Parameters
    ----------
    imagePath : Path
        path to image
    gridSize : list
        grid dimensions [x,y]
    subDir : bool
        should a subdir be created

    Returns
    -------
    str
        status string
    """
    x: int = gridSize[0]
    y: int = gridSize[1]
    image: Image.Image = Image.open(imagePath)
    width: int = image.size[0]
    height: int = image.size[1]
    successCount: int = 0
    dstPath: Path = imagePath.parent if not createSubDir else imagePath.parent / imagePath.stem

    if createSubDir and not dstPath.exists():
        dstPath.mkdir(exist_ok=True)

    for i in range(y):
        row: int = i % y
        top: int = floor(height * (row / y))
        bottom: int = floor(height * ((row + 1) / y)) - 1
        for j in range(x):
            col: int = j % x
            cropped: Image.Image = image.crop(
                (
                    floor(width * (col / x)),
                    top,
                    floor(width * ((col + 1) / x)) - 1,
                    bottom,
                ),
            )
            successCount += 1
            cropped.save(dstPath / f"{imagePath.stem} {successCount:02d}.png")

    return f"{successCount}/{x * y} Saved In {imagePath.name}"
