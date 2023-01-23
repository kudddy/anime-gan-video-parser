import redis

from plugins.rds.queue import Queue
from plugins.config import cfg

# redis = aioredis.from_url(cfg.app.hosts.redis.url, decode_responses=True)

r = redis.Redis(host=cfg.app.hosts.redis.url, decode_responses=True)

# TODO it is excess
queue = Queue(redis=r)

# queue = Queue(redis=redis)
