import logging

import pandas as pd
from time import sleep

from plugins.config import cfg
from plugins.workers.sendstat.send_email_with_files import send_mail
from plugins.pg.connector import setup_pg
from plugins.pg.query import query_calc_statistics, get_table_by_bot
from plugins.rds.connector import queue

usr = cfg.app.auth.email.username
pwd = cfg.app.auth.email.gmail_app_password

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

pg = setup_pg()


def generate_send_stat():
    name = "skillogger_to_worker"

    while True:

        try:

            if queue.qsize(name) > 0:

                log.info("start process")

                data = queue.receive(name)
                skill_name = data.get("bot_name")
                e_mail = data.get("e_mail")

                table_name, exist = get_table_by_bot(skill_name)

                if not exist:
                    log.info("table name not exist")
                    break

                sql_query = query_calc_statistics.format(table_name)

                cur = pg.cursor()
                cur.execute(sql_query)
                res = cur.fetchall()

                struct = {
                    'date': [],
                    'count_of_operators': [],
                    'count_of_messages': []
                }

                for it in res:
                    struct['date'].append(
                        it[0].strftime("%m/%d/%Y"),
                    )

                    struct['count_of_operators'].append(
                        it[2],
                    )

                    struct['count_of_messages'].append(
                        it[1],
                    )

                df = pd.DataFrame(struct)
                data = df.to_csv(index=False).encode()

                send_mail(
                    send_from=usr,
                    send_to=[
                        e_mail
                    ],
                    subject="Test",
                    message="Все будет нормально, главное стремиться!",
                    files=[
                        data
                    ],
                    username=usr,
                    password=pwd,
                    server="smtp.gmail.com",
                    port=465
                )

                cur.close()
            else:
                sleep(0.1)

        except Exception as e:
            log.info("something wrong in generate_send_stat_worker with error - {}".format(e))
