from json import dumps
from aiohttp_requests import requests as async_req

from plugins.config import cfg

LOGGER_HOST = cfg.app.hosts.logger.url


async def send_log(payload: dict):

    await async_req.post(LOGGER_HOST,
                         data=dumps(payload),
                         ssl=False,
                         headers={'Content-Type': 'application/json'})
