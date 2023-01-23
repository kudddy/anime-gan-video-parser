import logging

import psycopg2

from pathlib import Path

from plugins.config import cfg

MAX_QUERY_ARGS = 32767
MAX_INTEGER = 2147483647

pg_pool_min_size = 10
pg_pool_max_size = 10
PROJECT_PATH = Path(__file__).parent.parent.resolve()

log = logging.getLogger(__name__)


def setup_pg():
    log.info('Connecting to database')
    pg = None
    try:
        pg = psycopg2.connect(
            dbname=cfg.app.auth.pg.dbname,
            user=cfg.app.auth.pg.user,
            password=cfg.app.auth.pg.password,
            host=cfg.app.auth.pg.host,
            port=cfg.app.auth.pg.port
        )

        pg.fetchval('SELECT 1')

        log.info('Connected to database')
    except Exception as e:
        log.critical("connecting fail with error - {}".format(str(e)))

    return pg

# async def setup_pg() -> PG:
#     log.info('Connecting to database: %s', DEFAULT_PG_URL)
#
#
#
#     pg = PG()
#     await pg.init(
#         str(DEFAULT_PG_URL),
#         min_size=pg_pool_min_size,
#         max_size=pg_pool_max_size
#     )
#     await pg.fetchval('SELECT 1')
#
#     log.info('Connected to database %s', DEFAULT_PG_URL)
#
#     return pg
#
#
# def rounded(column, fraction: int = 2):
#     return func.round(cast(column, Numeric), fraction)
#
#
# class SelectQuery(AsyncIterable):
#     """
#     Используется чтобы отправлять данные из PostgreSQL клиенту сразу после
#     получения, по частям, без буфферизации всех данных.
#     """
#     PREFETCH = 1000
#
#     slots = (
#         'query', 'transaction_ctx', 'prefetch', 'timeout'
#     )
#
#     def __init__(self, query: Select,
#                  transaction_ctx: ConnectionTransactionContextManager,
#                  prefetch: int = None,
#                  timeout: float = None):
#         self.query = query
#         self.transaction_ctx = transaction_ctx
#         self.prefetch = prefetch or self.PREFETCH
#         self.timeout = timeout
#
#     async def __aiter__(self):
#         async with self.transaction_ctx as conn:
#             cursor = conn.cursor(self.query, prefetch=self.prefetch,
#                                  timeout=self.timeout)
#             async for row in cursor:
#                 yield row
