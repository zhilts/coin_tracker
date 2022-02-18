#!/usr/bin/env python3
from datetime import datetime, timedelta

import requests

from local_settings import DUCO_WALLET
from spreadsheet import append_row
from telegram_rest_api import send_message

WALLET = DUCO_WALLET
DUCO_WALLET_URL = f"https://server.duinocoin.com/users/{WALLET}"

TRANSACTION_DATETIME_FORMAT = '%d/%m/%Y %H:%M:%S'


def get_is_yesterday_transaction(now):
    yesterday = now.date() - timedelta(days=1)

    def is_yesterday(transaction):
        dt_str = transaction.get('datetime')
        dt = datetime.strptime(dt_str, TRANSACTION_DATETIME_FORMAT)
        return dt.date() == yesterday

    return is_yesterday


def get_data(timestamp):
    data = requests.get(DUCO_WALLET_URL).json().get("result")
    balance = data.get('balance').get('balance')
    miners = data.get('miners')
    miner_names = [m.get('identifier') for m in miners]
    transactions = data.get('transactions')
    is_yesterday = get_is_yesterday_transaction(timestamp)
    today_transactions = list(filter(is_yesterday, transactions))
    return balance, miner_names, today_transactions


def publish_telegram(balance, miners, *_):
    msg = '''
    ᕲ Duino Coin
    \t 🪙 Balance: <code>{balance:.2f} ᕲ</code>
    \t ⛏ Workers: <code>{workers}</code>
    '''.format(balance=balance, workers=len(miners))
    send_message(msg)


def publish_spreads(timestamp, balance, miners, transactions):
    worker_list = "\n".join(miners)
    transactions_sum = sum([t.get('amount') for t in transactions])
    values = [timestamp, balance, transactions_sum, len(miners), worker_list]
    append_row("DUCO", values)


if __name__ == '__main__':
    timestamp = datetime.now()
    timestamp_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
    balance, miners, transactions = get_data(timestamp)
    publish_telegram(balance, miners)
    publish_spreads(timestamp_str, balance, miners, transactions)
