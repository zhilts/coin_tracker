import requests

from local_settings import TELEGRAM_TOKEN, TELEGRAM_ID

TOKEN = TELEGRAM_TOKEN
ID = TELEGRAM_ID
URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'


def send_message(msg):
    requests.post(
        URL,
        data=dict(text=msg, parse_mode="HTML", disable_notification=True),
        params=dict(chat_id=ID)
    )
