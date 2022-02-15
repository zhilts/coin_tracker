#!/usr/bin/env python3
import datetime

import prettytable as pt
import requests

from local_settings import XMR_WALLET
from spreadsheet import append_row
from telegram import send_message

WALLET = XMR_WALLET
API_DATA_URL = f'https://xmr.nanopool.org/api/v1/user/{WALLET}'


def get_data():
    data = requests.get(API_DATA_URL).json().get('data')
    balance = float(data.get('balance'))
    workers = [dict(name=w.get('id'), hashrate=float(w.get('hashrate'))) for w in data.get('workers')]
    return balance, workers


def publish_telegram(balance, workers):
    table = pt.PrettyTable(['Name', 'Hashrate'])
    table.align['Name'] = 'l'
    table.align['Hashrate'] = 'r'
    for w in sorted(workers, key=lambda w: -w.get('hashrate')):
        table.add_row([w.get('name'), '{:.2f}'.format(w.get('hashrate'))])
    message = '''
    ɱ Monero Coin (NanoPool) 
    \t 🪙 Balance: <code>{balance} ɱ</code>
    \t ⛏ Workers: <code>{workers_count}</code>
    \n<pre>{workers}</pre>
    '''.format(balance=balance, workers_count=len(workers), workers=table)
    send_message(message)


def publish_spreads(timestamp, balance, miners):
    active_miners = list(filter(lambda m: m.get('hashrate') > 0, miners))
    worker_list = "\n".join([m.get('name') for m in active_miners])
    values = [timestamp, balance, len(active_miners), worker_list]
    append_row("XMR_nano", values)


if __name__ == '__main__':
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    balance, workers = get_data()
    publish_telegram(balance, workers)
    publish_spreads(timestamp, balance, workers)
