"""Translate a foreign language image to english in place."""

# /// script
# dependencies = [
#     "pytesseract",
#     "opencv-python",
#     "pillow",
#     "translate",
# ]
# ///
import sys
from collections.abc import Generator
from pathlib import Path
from typing import Any

import pytesseract
from cv2 import FONT_HERSHEY_TRIPLEX, getTextSize, imread, imwrite, putText, rectangle
from translate import Translator


def BoxExtract(results: dict) -> list[dict]:
    boxList = []
    for i in range(len(results["text"])):
        if (
            results["word_num"][i] > 0
            and results["conf"][i] > 0
            and [x for x in results["text"][i].strip() if x.isalnum()]
        ):
            box = {}
            x = results["left"][i]
            y = results["top"][i]

            w = results["width"][i]
            h = results["height"][i]
            box["shape"] = (x, y, w, h)
            box["words"] = results["word_num"][i]
            box["idx"] = i
            box["text"] = results["text"][i]
            boxList.append(box)
    return boxList


def DrawFunc(image: Any, box: dict) -> Any:
    import numpy as np

    x, y, w, h = box["shape"]
    # Crop the region
    roi = image[y : y + h, x : x + w]
    # Reshape to a list of pixels
    pixels = roi.reshape(-1, roi.shape[2]) if len(roi.shape) == 3 else roi.reshape(-1, 1)
    # Count unique colors
    colors, counts = np.unique(pixels, axis=0, return_counts=True)
    # Sort by count descending
    sorted_idx = np.argsort(-counts)
    most_common = colors[sorted_idx[0]] if len(sorted_idx) > 0 else np.array([0, 0, 0])
    fg_color = np.array([255, 255, 255])
    if len(sorted_idx) > 1:
        fg_color = colors[sorted_idx[1]]
    bg_color = tuple(int(c) for c in most_common)
    fg_color = tuple(int(c) for c in fg_color)
    # Draw background
    rectangle(image, (x, y), (x + w, y + h), bg_color, -1)
    imScale = CalcTextScale(box)
    # Calculate text size for centering
    (text_w, text_h), baseline = getTextSize(
        box["text"],
        FONT_HERSHEY_TRIPLEX,
        imScale,
        2,
    )
    # Center horizontally and vertically
    text_x = x + (w - text_w) // 2
    text_y = y + (h + text_h) // 2 - baseline
    putText(
        image,
        box["text"],
        (text_x, text_y),
        FONT_HERSHEY_TRIPLEX,
        imScale,
        fg_color,
        2,
    )
    return image


def CalcTextScale(box: dict) -> float:
    _x, _y, w, _h = box["shape"]
    textSize = getTextSize(
        text=box["text"],
        fontFace=FONT_HERSHEY_TRIPLEX,
        fontScale=1,
        thickness=2,
    )
    imScale = (w / textSize[0][0]) * 0.95
    return imScale


def Extract(image, lang="jpn"):
    # Use pytesseract to get bounding box data
    data = pytesseract.image_to_data(image, lang=lang, output_type=pytesseract.Output.DICT)
    n_boxes = len(data["level"])
    raw_boxes = []
    CONFIDENCE_THRESHOLD = 60
    print(data)
    for i in range(n_boxes):
        text = data["text"][i].strip()
        print(data["conf"][i], f"'{text}'")
        if text and data["conf"][i] >= CONFIDENCE_THRESHOLD:
            x, y, w, h = data["left"][i], data["top"][i], data["width"][i], data["height"][i]
            raw_boxes.append(
                {
                    "shape": (x, y, w, h),
                    "text": text,
                    "conf": data["conf"][i],
                },
            )

    # Sort by y, then x (top to bottom, left to right)
    raw_boxes.sort(key=lambda b: (b["shape"][1], b["shape"][0]))

    merged_boxes = []
    for box in raw_boxes:
        x, y, w, h = box["shape"]
        found = False
        for m in merged_boxes:
            mx, my, mw, mh = m["shape"]
            # If vertically close and horizontally overlapping or close, merge
            vertical_close = abs(y - my) < max(h, mh) * 0.7
            horizontal_overlap = (x < mx + mw + 20) and (mx < x + w + 20)
            if vertical_close and horizontal_overlap:
                # Merge bounding box
                min_x = min(mx, x)
                min_y = min(my, y)
                max_x = max(mx + mw, x + w)
                max_y = max(my + mh, y + h)
                m["shape"] = (min_x, min_y, max_x - min_x, max_y - min_y)
                m["text"] += " " + box["text"]
                found = True
                break
        if not found:
            merged_boxes.append(box)
    return merged_boxes


def TranslateV2(fromLang: str, path: str) -> Generator[str]:
    translator = Translator(
        provider="mymemory",
        from_lang=fromLang,
        to_lang="en",
        email="aedan.mchale@gmail.com",
    )
    image = imread(path)

    masterList = Extract(image, lang=fromLang if fromLang.lower() != "zh" else "jpn")
    for b in masterList:
        print(b["text"], end=" -> ")
        b["text"] = translator.translate(b["text"])
        print(b["text"])
        image = DrawFunc(image, b)
    p = Path(path)
    imwrite(str(p.parent / f"{p.stem}-translated.png"), image)
    yield f"{p.stem}-translated.png Written"


def CheckMatchingLines(masterList: list, box: dict) -> bool:
    match = False
    for idx, mBox in enumerate(masterList):
        mx, my, mw, mh = mBox["shape"]
        x, y, w, h = box["shape"]

        if x <= (mx + (mw * 1.5)) and y <= (my + (mh * 0.5)):
            masterList[idx]["shape"] = (
                mx,
                min(my, y),
                max((x + w) - mx, mw),
                max(mh, h),
            )
            masterList[idx]["text"] += " " + box["text"]
            match = True
            break
    return match


if __name__ == "__main__":
    for x in TranslateV2(sys.argv[2], sys.argv[1]):
        print(x)
