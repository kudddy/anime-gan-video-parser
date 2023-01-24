import logging
import json
from dataclasses import dataclass

from aiohttp_requests import requests
import requests as req

from structures.service_bot_struct import GetFile
from structures.message_struct import RespMessage

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)

log.setLevel(logging.DEBUG)

URL_SEND_MESSAGE = "https://api.telegram.org/bot{}/sendMessage"
URL_EDIT_MESSAGE = "https://api.telegram.org/bot{}/editMessageText"
URL_SEND_ANIMATION = "https://api.telegram.org/bot{}/sendAnimation"
URL_SEND_VIDEO = "https://api.telegram.org/bot{}/sendVideo"
URL_SEND_PHOTO = "https://api.telegram.org/bot{}/sendPhoto?chat_id={}"

URL_GET_FILE = "https://api.telegram.org/bot{}/getFile?file_id={}"
URL_GENERATE_URL = "https://api.telegram.org/file/bot{}/{}"


@dataclass
class AServiceBot:
    token: str

    async def get_file(self, file_id: str) -> GetFile:
        headers = {
            "Content-Type": "application/json"
        }

        response = await requests.get(URL_GET_FILE.format(self.token, file_id),
                                      headers=headers,
                                      ssl=False)

        response = await response.json()

        return GetFile(**response)

    def generate_file_url(self, file_path: str) -> str:
        return URL_GENERATE_URL.format(self.token, file_path)


@dataclass
class ServiceBot:
    token: str

    def get_file(self, file_id: str) -> GetFile:
        headers = {
            "Content-Type": "application/json"
        }

        response = req.get(
            URL_GET_FILE.format(self.token, file_id),
            headers=headers
        )

        response = response.json()

        return GetFile(**response)

    def generate_file_url(self, file_path: str) -> str:
        return URL_GENERATE_URL.format(self.token, file_path)


class AMessagingBot:
    def __init__(self, token):
        self.token = token

    async def send_message(self,
                           chat_id: int,
                           text: str,
                           parse_mode: str = None,
                           buttons: list or None = None,
                           inline_keyboard: list or None = None,
                           one_time_keyboard: bool = True,
                           resize_keyboard: bool = True,
                           remove_keyboard: bool = False):
        payload = {
            "chat_id": chat_id,
            "text": text[:4095],
            "reply_markup": {
                "remove_keyboard": remove_keyboard
            }
        }

        if parse_mode:
            payload.update({"parse_mode": parse_mode})

        if buttons:
            # TODO hardcode
            keyboards = [[{"text": text}] for text in buttons]
            payload["reply_markup"].update({
                "keyboard": keyboards,
                "resize_keyboard": resize_keyboard,
                "one_time_keyboard": one_time_keyboard
            })

        if inline_keyboard:
            payload["reply_markup"].update({"inline_keyboard": inline_keyboard})

        headers = {
            "Content-Type": "application/json"
        }

        response = await requests.get(URL_SEND_MESSAGE.format(self.token), headers=headers, data=json.dumps(payload),
                                      ssl=False)

        response = await response.json()

        res = response.get("ok")

        # маскирование текста
        payload["text"] = "*******"

        if res:
            log.debug("request with payload: %s success delivered to tlg", payload)
        else:
            log.debug("request with payload: %s delivered to tlg with error: %s", payload, response)

    async def edit_message(self,
                           text: str,
                           chat_id: int or str = None,
                           message_id: int = None,
                           inline_keyboard: list or None = None,
                           inline_message_id: str = None,
                           parse_mode: str = None,
                           entities: str = None,
                           disable_web_page_preview: bool = None,
                           ):
        payload = {
            "text": text[:4095]
        }
        if chat_id:
            payload.update({"chat_id": chat_id})
        if message_id:
            payload.update({"message_id": message_id})
        if parse_mode:
            payload.update({"parse_mode": parse_mode})

        headers = {
            "Content-Type": "application/json",
        }

        if inline_keyboard:
            payload.update(
                {"reply_markup": {
                    "inline_keyboard": inline_keyboard}
                })

        response = await requests.get(URL_EDIT_MESSAGE.format(self.token),
                                      headers=headers,
                                      data=json.dumps(payload),
                                      ssl=False)

        response = await response.json()

        res = response.get("ok")

        payload["text"] = "*******"

        if res:
            log.debug("request with payload: %s success delivered to tlg", payload)
        else:
            log.debug("request with payload: %s delivered to tlg with error: %s", payload, response)

    async def send_animation(self,
                             chat_id: int,
                             file_id: str):
        headers = {
            "Content-Type": "application/json",
        }

        payload = {
            "chat_id": chat_id,
            "animation": file_id
        }

        response = await requests.get(URL_SEND_ANIMATION.format(self.token), headers=headers, data=json.dumps(payload),
                                      ssl=False)
        response = await response.json()
        res = response.get("ok")

        if res:
            log.debug("request with payload: %s success delivered to tlg", payload)
        else:
            log.debug("request with payload: %s delivered to tlg with error: %s", payload, response)

    async def send_video(self, chat_id: int, file_id: str):
        headers = {
            "Content-Type": "application/json",
        }

        payload = {
            "chat_id": chat_id,
            "video": file_id
        }

        response = await requests.get(URL_SEND_VIDEO.format(self.token), headers=headers, data=json.dumps(payload),
                                      ssl=False)
        response = await response.json()
        res = response.get("ok")

        if res:
            log.debug("request with payload: %s success delivered to tlg", payload)
        else:
            log.debug("request with payload: %s delivered to tlg with error: %s", payload, response)

    def send_photo(self, chat_id: int, image_bytes: bytes) -> RespMessage:
        payload = {}
        headers = {}
        files = [
            ('photo', ('frame0.jpg', image_bytes, 'image/jpeg'))
        ]
        response = req.get(URL_SEND_PHOTO.format(self.token, chat_id), headers=headers, data=payload, files=files)

        response = response.json()

        return RespMessage(**response)


class MessagingBot:
    def __init__(self, token):
        self.token = token

    def send_message(self,
                     chat_id: int,
                     text: str,
                     parse_mode: str = None,
                     buttons: list or None = None,
                     inline_keyboard: list or None = None,
                     one_time_keyboard: bool = True,
                     resize_keyboard: bool = True,
                     remove_keyboard: bool = False):
        payload = {
            "chat_id": chat_id,
            "text": text[:4095],
            "reply_markup": {
                "remove_keyboard": remove_keyboard
            }
        }

        if parse_mode:
            payload.update({"parse_mode": parse_mode})

        if buttons:
            # TODO hardcode
            keyboards = [[{"text": text}] for text in buttons]
            payload["reply_markup"].update({
                "keyboard": keyboards,
                "resize_keyboard": resize_keyboard,
                "one_time_keyboard": one_time_keyboard
            })

        if inline_keyboard:
            payload["reply_markup"].update({"inline_keyboard": inline_keyboard})

        headers = {
            "Content-Type": "application/json"
        }

        response = req.get(URL_SEND_MESSAGE.format(self.token),
                           headers=headers,
                           data=json.dumps(payload))

        response = response.json()

        res = response.get("ok")

        # маскирование текста
        payload["text"] = "*******"

        if res:
            log.debug("request with payload: %s success delivered to tlg", payload)
        else:
            log.debug("request with payload: %s delivered to tlg with error: %s", payload, response)

    def edit_message(self,
                     text: str,
                     chat_id: int or str = None,
                     message_id: int = None,
                     inline_keyboard: list or None = None,
                     inline_message_id: str = None,
                     parse_mode: str = None,
                     entities: str = None,
                     disable_web_page_preview: bool = None,
                     ):
        payload = {
            "text": text[:4095]
        }
        if chat_id:
            payload.update({"chat_id": chat_id})
        if message_id:
            payload.update({"message_id": message_id})
        if parse_mode:
            payload.update({"parse_mode": parse_mode})

        headers = {
            "Content-Type": "application/json",
        }

        if inline_keyboard:
            payload.update(
                {"reply_markup": {
                    "inline_keyboard": inline_keyboard}
                })

        response = req.get(
            url=URL_EDIT_MESSAGE.format(self.token),
            headers=headers,
            data=json.dumps(payload)
        )

        response = response.json()

        res = response.get("ok")

        payload["text"] = "*******"

        if res:
            log.debug("request with payload: %s success delivered to tlg", payload)
        else:
            log.debug("request with payload: %s delivered to tlg with error: %s", payload, response)

    def send_animation(self,
                       chat_id: int,
                       file_id: str):
        headers = {
            "Content-Type": "application/json",
        }

        payload = {
            "chat_id": chat_id,
            "animation": file_id
        }

        response = req.get(
            url=URL_SEND_ANIMATION.format(self.token),
            headers=headers,
            data=json.dumps(payload)
        )
        response = response.json()
        res = response.get("ok")

        if res:
            log.debug("request with payload: %s success delivered to tlg", payload)
        else:
            log.debug("request with payload: %s delivered to tlg with error: %s", payload, response)

    def send_video(self, chat_id: int, file_id: str):
        headers = {
            "Content-Type": "application/json",
        }

        payload = {
            "chat_id": chat_id,
            "video": file_id
        }

        response = req.get(
            url=URL_SEND_VIDEO.format(self.token),
            headers=headers,
            data=json.dumps(payload)
        )
        response = response.json()
        res = response.get("ok")

        if res:
            log.debug("request with payload: %s success delivered to tlg", payload)
        else:
            log.debug("request with payload: %s delivered to tlg with error: %s", payload, response)

    def send_photo(self, chat_id: int, image_bytes: bytes) -> RespMessage:
        payload = {}
        headers = {}
        files = [
            ('photo', ('frame0.jpg', image_bytes, 'image/jpeg'))
        ]
        response = req.get(URL_SEND_PHOTO.format(self.token, chat_id), headers=headers, data=payload, files=files)

        response = response.json()

        return RespMessage(**response)


# @dataclass
# class Bot:
#     token: str
#     messaging = MessagingBot(token)
#     servicing: ServiceBot()

# class ABot:
#     def __init__(self, token: str):
#         self.messaging = AMessagingBot(token)
#         self.servicing = AServiceBot(token)

# @dataclass
# class Bot:
#     token: str
#     messaging = MessagingBot(token)
#     servicing = ServiceBot(token)

class Bot:
    def __init__(self, token: str):
        self.messaging = MessagingBot(token)
        self.servicing = ServiceBot(token)
