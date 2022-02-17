#!/usr/bin/env python3
import datetime

import prettytable as pt
import requests

from local_settings import XMR_WALLET
from spreadsheet import append_row
from telegram_rest_api import send_message

WALLET = XMR_WALLET
BASE_API_URL = 'https://minexmr.com/api/main'
USER_STAT_URL = f"{BASE_API_URL}/user/stats"
WORKERS_STAT_URL = f"{BASE_API_URL}/user/workers"


def get_data():
    user_data = requests.get(USER_STAT_URL, params=dict(address=WALLET)).json()
    workers_data = requests.get(WORKERS_STAT_URL, params=dict(address=WALLET)).json()
    balance = int(user_data.get('balance')) / (10 ** 12)
    return balance, workers_data


def publish_telegram(balance, workers):
    table = pt.PrettyTable(['Name', 'Hashrate'])
    table.align['Name'] = 'l'
    table.align['Hashrate'] = 'r'
    for w in sorted(workers, key=lambda w: -w.get('hashrate')):
        table.add_row([w.get('name'), '{:.2f}'.format(w.get('hashrate'))])
    message = '''
    ɱ Monero Coin (MineXMR)
    \t 🪙 Balance: <code>{balance} ɱ</code>
    \t ⛏ Workers: <code>{workers_count}</code>
    \n<pre>{workers}</pre>
    '''.format(balance=balance, workers_count=len(workers), workers=table)
    send_message(message)


def publish_spreads(timestamp, balance, miners):
    active_miners = list(filter(lambda m: m.get('hashrate') > 0, miners))
    worker_list = "\n".join([m.get('name') for m in active_miners])
    values = [timestamp, balance, len(active_miners), worker_list]
    append_row("XMR_mine", values)


if __name__ == '__main__':
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    balance, workers = get_data()
    publish_telegram(balance, workers)
    publish_spreads(timestamp, balance, workers)
