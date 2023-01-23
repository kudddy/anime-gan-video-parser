import pandas as pd

from plugins.config import cfg
from plugins.workers.sendstat.send_email_with_files import send_mail
from plugins.pg.connector import setup_pg
from plugins.pg.query import query_calc_statistics
from plugins.rds.connector import queue

usr = cfg.app.auth.email.username
pwd = cfg.app.auth.email.gmail_app_password

pg = setup_pg()


def generate_send_stat():
    name = "skillogger_to_worker"

    while True:

        data = queue.receive(name)

        if len(data) > 0:

            res = pg.execute(query_calc_statistics)

            struct = {
                'date': [],
                'count_of_operators': [],
                'count_of_messages': []
            }

            for it in res:
                struct['date'].append(
                    it['date'].strftime("%m/%d/%Y"),
                )

                struct['count_of_operators'].append(
                    it['count_of_operators'],
                )

                struct['count_of_messages'].append(
                    it['count_of_messages'],
                )

            df = pd.DataFrame(struct)
            data = df.to_csv(index=False).encode()

            send_mail(
                send_from=usr,
                send_to=[
                    "kudonline@gmail.com"
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
