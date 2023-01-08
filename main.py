import asyncio
import logging

import aioredis

from plugins.bot import Bot
from plugins.logic import pars_video
from plugins.queue import Queue
from plugins.config import cfg

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

bot = Bot(token=cfg.app.constants.bot_token)

redis = aioredis.from_url(cfg.app.hosts.redis.url, decode_responses=True)


async def start_working():
    name = "bot_to_video_parser"
    queue = Queue(redis=redis)

    while True:
        data = await queue.receive(name)

        file_id = data.get("file_id", "")
        chat_id = data.get("chat_id", "")
        user_id = data.get("user_id", "")
        user_model = data.get("user_model", "")

        if len(file_id) > 0:
            # получаем file_id фоток
            log.info("start working")
            try:
                await bot.messaging.send_message(chat_id=chat_id, text="Начинаю парсить видео!🦥")
                arr_for_ids = await pars_video(file_id)

                struct = {str(k): v for k, v in enumerate(arr_for_ids)}
                struct.update({
                    "chat_id": chat_id,
                    "user_id": user_id,
                    "user_model": user_model
                })

                log.info("send message to queen - {}".format("parser_to_creator"))

                await bot.messaging.send_message(chat_id=chat_id, text="Закончил парсинг! Начинаю обработку видео🦥")

                await queue.send(name="parser_to_transformer", struct=struct)
            except Exception as e:
                log.info("something wrong with error - {}".format(e))

        else:

            await asyncio.sleep(5)


asyncio.run(start_working())
