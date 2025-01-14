import os
import sys

from cv2 import CAP_PROP_FPS, CAP_PROP_POS_FRAMES, VideoCapture, imwrite


def VideoToIMGSeq(inPath, startTime: float, endTime: float):
    # Create the output directory if it doesn't exist
    outDir = inPath.parent / inPath.name
    if not os.path.exists(outDir):
        os.makedirs(outDir)

    # Capture the video
    video = VideoCapture(inPath)  # type: ignore

    # Check if the video opened successfully
    if not video.isOpened():
        print("Error: Could not open video.")
        sys.exit()

    fps = video.get(CAP_PROP_FPS)
    startFrame = int(startTime * fps)
    endFrame = int(endTime * fps)

    video.set(CAP_PROP_POS_FRAMES, startFrame)

    frameNum = startFrame
    while frameNum <= endFrame:
        ret, frame = video.read()
        if not ret:
            break

        fileName = os.path.join(outDir, f"frame_{frameNum:04d}.jpg")
        imwrite(fileName, frame)
        frameNum += 1

    video.release()
    return f"Extracted frames from {startTime}s to {endTime}s seconds to {outDir}"
