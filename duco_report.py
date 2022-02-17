#!/usr/bin/env python3
import datetime

import requests

from local_settings import DUCO_WALLET
from spreadsheet import append_row
from telegram_rest_api import send_message

WALLET = DUCO_WALLET
DUCO_WALLET_URL = f"https://server.duinocoin.com/users/{WALLET}"


def get_data():
    data = requests.get(DUCO_WALLET_URL).json().get("result")
    balance = data.get('balance').get('balance')
    miners = data.get('miners')
    miner_names = [m.get('identifier') for m in miners]
    return balance, miner_names


def publish_telegram(balance, miners):
    msg = '''
    ᕲ Duino Coin
    \t 🪙 Balance: <code>{balance:.2f} ᕲ</code>
    \t ⛏ Workers: <code>{workers}</code>
    '''.format(balance=balance, workers=len(miners))
    send_message(msg)


def publish_spreads(timestamp, balance, miners):
    worker_list = "\n".join(miners)
    values = [timestamp, balance, len(miners), worker_list]
    append_row("DUCO", values)


if __name__ == '__main__':
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    balance, miners = get_data()
    publish_telegram(balance, miners)
    publish_spreads(timestamp, balance, miners)
