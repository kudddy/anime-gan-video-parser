import logging
import requests

from time import sleep
from json import dumps

from plugins.workers.crop_photo.crop_photo import insert_face_from_photo
from plugins.rds.connector import queue
from plugins.config import cfg

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def run_crop_worker():
    queue_name = "bot_to_crop_photo"
    while True:

        if queue.qsize(queue_name) > 0:
            data = queue.receive(queue_name)

            file_id = data.get("file_id", "")
            chat_id = data.get("chat_id", "")
            user_id = data.get("user_id", "")
            user_model = data.get("user_model", "")

            log.info("start crop photo")
            try:
                crop_file_id = insert_face_from_photo(
                    file_id=file_id
                )

                log.info("send req to transformer")

                requests.post(
                    url=cfg.app.hosts.sheduler.url,
                    data=dumps(
                        {
                            "file_id": crop_file_id,
                            "chat_id": int(chat_id),
                            "user_id": int(user_id),
                            "user_model": user_model

                        }
                    ),
                    headers={'Content-Type': 'application/json'}
                )
            except Exception as e:
                log.info("something wrong with error - {}".format(e))

        else:
            sleep(0.1)
