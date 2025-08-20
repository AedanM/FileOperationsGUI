"""Translate a foreign language image to english in place."""

import sys
from collections.abc import Generator
from pathlib import Path
from typing import Any

import cv2
import pytesseract
from pytesseract import Output
from translate import Translator

# pylint:disable=E1101


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
    x, y, w, h = box["shape"]
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 0), -1)
    imScale = CalcTextScale(box)
    cv2.putText(
        image,
        box["text"],
        (x + 10, y + ((3 * h) // 4)),
        cv2.FONT_HERSHEY_DUPLEX,
        imScale,
        (255, 255, 255),
        2,
    )
    return image


def CalcTextScale(box: dict) -> float:
    _x, _y, w, _h = box["shape"]
    textSize = cv2.getTextSize(
        text=box["text"],
        fontFace=cv2.FONT_HERSHEY_DUPLEX,
        fontScale=1,
        thickness=2,
    )
    imScale = (w / textSize[0][0]) * 0.95
    return imScale


def TranslateV2(fromLang: str, path: str) -> Generator[str]:
    translator = Translator(
        provider="mymemory",
        from_lang=fromLang,
        to_lang="en",
        email="aedan.mchale@gmail.com",
    )
    image = cv2.imread(path)
    results = pytesseract.image_to_data(image, output_type=Output.DICT)
    masterList = []
    for box in BoxExtract(results):
        if not CheckMatchingLines(masterList, box):
            masterList.append(box)
    for b in masterList:
        b["text"] = translator.translate(b["text"])
        image = DrawFunc(image, b)
    p = Path(path)
    cv2.imwrite(str(p.parent / f"{p.stem}-translated.png"), image)
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
    print(TranslateV2(sys.argv[2], sys.argv[1]))
