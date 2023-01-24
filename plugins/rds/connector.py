import redis

from plugins.rds.queue import Queue
from plugins.config import cfg

# redis = aioredis.from_url(cfg.app.hosts.redis.url, decode_responses=True)

# r = redis.Redis(host=cfg.app.hosts.redis.url, decode_responses=True)

r = redis.Redis(
    host=cfg.app.hosts.redis.host,
    port=cfg.app.hosts.redis.port,
    db=cfg.app.hosts.redis.db,
    decode_responses=True
)

# TODO it is exist
queue = Queue(redis=r)
