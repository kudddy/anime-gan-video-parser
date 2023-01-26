import logging
import requests

from io import BytesIO

import cv2
import dlib
import numpy as np
from PIL import Image

from plugins.bot import Bot
from plugins.config import cfg

bot = Bot(token=cfg.app.constants.bot_token)
face_detector = dlib.get_frontal_face_detector()

x_top = cfg.app.constants.image.top
x_bottom = cfg.app.constants.image.bottom
x_left = cfg.app.constants.image.left
x_right = cfg.app.constants.image.right

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

log.debug("top - {}, bottom - {}, left - {}, right - {}".format(x_top,
                                                                x_bottom,
                                                                x_left,
                                                                x_right))


def insert_face_from_photo(file_id: str):
    resp = bot.servicing.get_file(file_id=file_id)
    # generate url photo
    pic_url = bot.servicing.generate_file_url(resp.result.file_path)

    response = requests.get(pic_url)

    img = Image.open(BytesIO(response.content))

    image_to_np = np.array(img)

    image_to_np = cv2.cvtColor(image_to_np, cv2.COLOR_BGR2RGB)

    max_height = image_to_np.shape[0]
    max_width = image_to_np.shape[1]

    detected_faces = face_detector(image_to_np, 1)
    if len(detected_faces) > 0:
        face_rect = detected_faces[0]

        top = 0 if face_rect.top() - x_top < 0 else face_rect.top() - x_top
        bottom = max_height if face_rect.bottom() + x_bottom > max_height else face_rect.bottom() + x_bottom
        left = 0 if face_rect.left() - x_left < 0 else face_rect.left() - x_left
        right = max_width if face_rect.right() + x_right > max_width else face_rect.right() + x_right

        crop = image_to_np[top:bottom, left:right]
        crop = cv2.imencode('.jpg ', crop, [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tobytes()
    else:
        crop = cv2.imencode('.jpg ', image_to_np, [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tobytes()

    resp = bot.messaging.send_photo(chat_id=710828013, image_bytes=crop)

    return resp.result.get_file_id()
