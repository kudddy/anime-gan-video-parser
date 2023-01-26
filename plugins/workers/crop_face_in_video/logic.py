import logging

import cv2
import dlib
import numpy as np

from plugins.bot import Bot
from plugins.logger import send_log
from plugins.config import cfg

bot = Bot(token=cfg.app.constants.bot_token)
face_detector = dlib.get_frontal_face_detector()
duration_target = 3

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


def pars_video(file_id: str):
    resp = bot.servicing.get_file(file_id=file_id)

    # генерируем url c видео для загрузки
    video_url = bot.servicing.generate_file_url(resp.result.file_path)

    # загружаем видео
    video = cv2.VideoCapture(video_url)

    video.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    video.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    # определяем параметры видео
    fps = video.get(cv2.CAP_PROP_FPS)  # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    # определяем коэф продолжительности видео
    coefficient = duration / duration_target
    # если коэф > 1 то режем видео иначе ничего не делаем
    if coefficient > 1:
        target_count_frames = frame_count / coefficient
    else:
        target_count_frames = frame_count

    print('кол-во кадров после обрезки: ' + str(target_count_frames))

    print('fps = ' + str(fps))
    print('number of frames = ' + str(frame_count))
    print('duration (S) = ' + str(duration))
    minutes = int(duration / 60)
    seconds = duration % 60
    print('duration (M:S) = ' + str(minutes) + ':' + str(seconds))

    # TODO обрезаем видео до 10 секунд и убираем каждый второй кадр

    success, image = video.read()
    count = 0
    file_ids_arr = []

    while success:
        # пропускаем каждый второй кадры для оптимизации
        try:
            if count % 2 == 0:

                image_to_np = np.array(image)

                detected_faces = face_detector(image_to_np, 1)
                if len(detected_faces) > 0:
                    face_rect = detected_faces[0]

                    crop = image_to_np[face_rect.top() - x_top:face_rect.bottom() + x_bottom,
                           face_rect.left() - x_left:face_rect.right() + x_right]
                    crop = cv2.imencode('.jpg', crop, [cv2.IMWRITE_JPEG_QUALITY, 100])[1].tobytes()
                else:
                    crop = image_to_np
                # получаем видео от telegram

                resp = bot.messaging.send_photo(chat_id=710828013, image_bytes=crop)

                # записываем в массив id файлов с самым большим разрешением
                # этот массив мы должны передать на обработку
                file_ids_arr.append(resp.result.get_file_id())
        except Exception as e:
            send_log(
                {
                    "MESSAGE_NAME": "LOGGER_INFO",
                    "DATA": {
                        "log_info": "[anime-gan-video-parser] Error - {}".format(str(e)),
                        "bot_type": "AnimeGanServiceBot",
                        "error_status": False
                    }
                }
            )


        # переходим к следующему кадру
        success, image = video.read()
        count += 1

        if count >= target_count_frames:
            break

    return file_ids_arr
