import cv2
from image_to_text import get_text


def vid_to_text(path):
    vidcap = cv2.VideoCapture(path)
    success, image = vidcap.read()
    count = 0
    text_blob = ""
    while success:
        success, image = vidcap.read()
        print('frames', vidcap.get(cv2.CAP_PROP_FPS))
        if (not count % (vidcap.get(cv2.CAP_PROP_FPS) * 2)):
            temp = get_text(image).replace("\n", " ").strip()
            if (temp not in text_blob):
                text_blob += temp
        print('Read a new frame: ', success)
        count += 1
        print(count)
    return text_blob
