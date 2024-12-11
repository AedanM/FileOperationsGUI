import sys

import cv2
import pytesseract
from translate import Translator


def TranslateIMG(fromLang: str, path: str):
    # pylint:disable=E1101
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    translator = Translator(
        provider="mymemory",
        from_lang=fromLang,
        to_lang="en",
        email="aedan.mchale@gmail.com",
    )
    text = pytesseract.image_to_string(img).lower()
    t = translator.translate(text)
    return t


if __name__ == "__main__":
    print(TranslateIMG(sys.argv[2], sys.argv[1]))
