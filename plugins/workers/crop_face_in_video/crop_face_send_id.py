import logging
from time import sleep

from plugins.bot import Bot
from plugins.workers.crop_face_in_video.logic import pars_video
from plugins.rds.connector import queue
from plugins.config import cfg

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

bot = Bot(token=cfg.app.constants.bot_token)


def start_listening_and_pars():
    name = "bot_to_video_parser"

    while True:
        data = queue.receive(name)

        file_id = data.get("file_id", "")
        chat_id = data.get("chat_id", "")
        user_id = data.get("user_id", "")
        user_model = data.get("user_model", "")

        if len(file_id) > 0:
            # получаем file_id фоток
            log.info("start working")
            try:
                bot.messaging.send_message(chat_id=chat_id, text="Начинаю парсить видео!🦥")
                arr_for_ids = pars_video(file_id)

                struct = {str(k): v for k, v in enumerate(arr_for_ids)}

                struct.update({
                    "chat_id": chat_id,
                    "user_id": user_id,
                    "user_model": user_model
                })

                log.info("send message to queen - {}".format("parser_to_creator"))

                bot.messaging.send_message(chat_id=chat_id, text="Закончил парсинг! Начинаю обработку видео🦥")

                queue.send(name="parser_to_transformer", struct=struct)
            except Exception as e:
                log.info("something wrong with error - {}".format(e))

        else:
            sleep(5)
