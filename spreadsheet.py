import gspread
from oauth2client.service_account import ServiceAccountCredentials

from local_settings import GDOC_NAME

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials_google.json', scope)
client = gspread.authorize(creds)
sh = client.open(GDOC_NAME)


def append_row(sheet_name, values):
    sheet = sh.worksheet(sheet_name)
    sheet.append_row(values, value_input_option='USER_ENTERED')
