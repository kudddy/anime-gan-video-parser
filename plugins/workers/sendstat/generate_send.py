import logging

import pandas as pd
from time import sleep
from datetime import timedelta, datetime

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

start_delta = timedelta(days=7)

pg = setup_pg()


def get_percent(
        sum_one: int,
        sum_two: int,
):
    if sum_one == 0 or sum_two == 0:
        sum_percent = 100
    else:
        sum_percent = int(100 - (sum_one / sum_two) * 100)

    return sum_percent


class StatCalc:
    def __init__(self):
        self._memory = {
            'date': [],
            'count_of_operators': [],
            'count_of_messages': [],
            'automation': []
        }
        self.sum_count_of_messages_month = 0
        self.sum_count_of_operators_month = 0

        self.sum_count_of_messages_week = 0
        self.sum_count_of_operators_week = 0

        self.start_of_week = datetime.now() - start_delta

    def add_stat(self, date: datetime or str,
                 count_of_operators: int,
                 count_of_messages: int,
                 automation: int):

        if isinstance(date, datetime):
            self._memory['date'].append(date.strftime("%m/%d/%Y"))
        elif isinstance(date, str):
            self._memory['date'].append(date)
        self._memory['count_of_operators'].append(count_of_operators)
        self._memory['count_of_messages'].append(count_of_messages)
        self._memory['automation'].append(automation)

    def calc(self, date: datetime,
             count_of_operators: int,
             count_of_messages: int,
             automation: int):

        self.add_stat(
            date=date,
            count_of_operators=count_of_operators,
            count_of_messages=count_of_messages,
            automation=automation
        )

        self.sum_count_of_messages_month += count_of_messages
        self.sum_count_of_operators_month += count_of_operators

        if date >= self.start_of_week.date():
            self.sum_count_of_messages_week += count_of_messages
            self.sum_count_of_operators_week += count_of_operators

    def perform(self):

        self.add_stat(
            date="Current Week",
            count_of_operators=self.sum_count_of_operators_week,
            count_of_messages=self.sum_count_of_messages_week,
            automation=get_percent(
                self.sum_count_of_operators_week,
                self.sum_count_of_messages_week
            )
        )

        self.add_stat(
            date="Current Month",
            count_of_operators=self.sum_count_of_operators_month,
            count_of_messages=self.sum_count_of_messages_month,
            automation=get_percent(
                self.sum_count_of_operators_month,
                self.sum_count_of_messages_month
            )
        )

    def done(self) -> dict:
        self.perform()
        return self._memory

    def init(self):
        self._memory = {
            'date': [],
            'count_of_operators': [],
            'count_of_messages': [],
            'automation': []
        }
        self.sum_count_of_messages_month = 0
        self.sum_count_of_operators_month = 0

        self.sum_count_of_messages_week = 0
        self.sum_count_of_operators_week = 0

        self.start_of_week = datetime.now() - start_delta


stat = StatCalc()


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

                stat.init()

                for it in res:
                    date = it[0]
                    count_of_operators = it[2]
                    count_of_messages = it[1]

                    if count_of_messages == 0 or count_of_operators == 0:
                        percent = 100
                    else:
                        percent = int(100 - (count_of_operators / count_of_messages) * 100)

                    stat.calc(
                        date=date,
                        count_of_operators=count_of_operators,
                        count_of_messages=count_of_messages,
                        automation=percent

                    )
                cur.close()

                df = pd.DataFrame(stat.done())
                data = df.to_csv(index=False).encode()

                send_mail(
                    send_from=usr,
                    send_to=[
                        e_mail
                    ],
                    subject="Отчетность!",
                    message="Отчетность приложена в формате csv.",
                    files=[
                        data
                    ],
                    username=usr,
                    password=pwd,
                    server="smtp.gmail.com",
                    port=465
                )

            else:
                sleep(0.1)

        except Exception as e:
            log.info("something wrong in generate_send_stat_worker with error - {}".format(e))
