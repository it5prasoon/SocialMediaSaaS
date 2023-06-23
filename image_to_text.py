import cv2
import pytesseract
from autocorrect import Speller

spell = Speller()


def get_text(img, path_flag=0):
    if (path_flag):
        img = cv2.imread(img)
    # img = cv2.resize(img, (600, 360))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    raw_text = ""
    custom_config = r'--oem 3 --psm 7'

    raw_text = pytesseract.image_to_string(img, config=custom_config).strip()
    return spell(raw_text + " ")
