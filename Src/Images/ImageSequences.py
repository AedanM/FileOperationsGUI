"""Decomposing files into composite parts."""

import itertools
from collections.abc import Generator
from pathlib import Path

from cv2 import CAP_PROP_FPS, CAP_PROP_FRAME_COUNT, CAP_PROP_POS_FRAMES, VideoCapture, imwrite
from pdf2image import convert_from_path
from PIL import Image

from Src.Utilities.UtilityTools import DigitizeStr, GetAllVideos


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
    vidList = GetAllVideos(inputPath)
    for videoPath in vidList:
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
    if not vidList:
        yield "No video files found"


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
    if not pdfList:
        yield "No .pdf files found"


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
    if not gifList:
        yield "No .gif files found"


def Ranges(i: list[int]) -> Generator[tuple[int, int]]:
    for _a, b in itertools.groupby(enumerate(i), lambda pair: pair[1] - pair[0]):
        b = list(b)
        yield b[0][1], b[-1][1]


def CheckSequence(filePath: Path) -> list:
    fileNums: set[int] = set()
    for file in [x for x in filePath.glob("**/*") if isinstance(x, Path)]:
        fileNums.add(DigitizeStr(inString=file.stem))
    numList: list[int] = sorted(fileNums)

    prevVal: int = numList[0]
    missingVals: list[int] = []
    for num in numList[1:]:
        if prevVal != num - 1:
            missingVals += range(prevVal + 1, num)
        prevVal = num
    return list(Ranges(missingVals))


def CheckSeq(path: Path) -> Generator[str]:
    missing = CheckSequence(path)
    if missing:
        missingList = [f"{x[0]} to {x[1]}" if x[0] != x[1] else str(x[0]) for x in missing]
        outStr = f"Missing {', '.join(missingList)}"
    else:
        fileNums: set[int] = set()
        for file in [x for x in path.glob("**/*") if isinstance(x, Path)]:
            fileNums.add(DigitizeStr(inString=file.stem))
        numList: list[int] = sorted(fileNums)
        outStr = f"Complete Sequence from {numList[0]}-{numList[-1]}"
    yield outStr
