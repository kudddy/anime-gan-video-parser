import asyncio

from plugins.workers.sendstat.generate_send import generate_send_stat


asyncio.run(generate_send_stat())
