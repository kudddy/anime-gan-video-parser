import uuid
import logging

from aioredis.client import Redis

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


class Queue:
    def __init__(self, redis: Redis):
        self.redis = redis

    async def send(self, name: str, struct: dict):

        uid = str(uuid.uuid4())

        log.info("send task with uuid - {}".format(uid))

        await self.redis.hmset(uid, struct)

        await self.redis.lpush(name, uid)

    async def receive(self, name: str) -> dict:
        task_uid = await self.redis.rpop(name)

        if task_uid:

            log.info("job uuid is - {}".format(task_uid))

            data_for_task = await self.redis.hgetall(task_uid)

        else:
            data_for_task = {}

        return data_for_task
