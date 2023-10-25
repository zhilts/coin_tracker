import gspread
from oauth2client.service_account import ServiceAccountCredentials

from local_settings import GDOC_NAME

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
GOOGLE_CREDENTIALS_FILE = 'credentials_google.json'

sh = None


def __init_sh():
    global sh
    if not sh:
        creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_FILE, scope)
        client = gspread.authorize(creds)
        sh = client.open(GDOC_NAME)


def append_row(sheet_name, values):
    __init_sh()
    sheet = sh.worksheet(sheet_name)
    last_row = len(sheet.get_all_values())
    new_row = last_row + 1
    sheet.append_row(
        [*values, f'=IF(B{new_row}, IF(ISNUMBER(B{last_row}), B{new_row}-C{new_row}-B{last_row}, ""), "")',
         f'=IF(F{new_row},F{new_row}*30,"")', f'=IF(ISNUMBER(F{new_row}),AVERAGE(F$2:F$99999),"")',
         f'=IF(ISNUMBER(F{new_row}),AVERAGE(F$2:F{new_row}),"")',
         f'=IF(ISNUMBER(F{new_row}),AVERAGE(INDIRECT(ADDRESS(MAX(ROW()-4,2),6)&":"&ADDRESS(ROW(),6))),"")',
         f'=IF(ISNUMBER(F{new_row}),AVERAGE(INDIRECT(ADDRESS(MAX(ROW()-29,2),6)&":"&ADDRESS(ROW(),6))),"")'],
        value_input_option='USER_ENTERED')

    sheet.format(f"A{new_row}:A{new_row}", {
        "numberFormat": {"type": "DATE", "pattern": "yyyy-mm-dd"},
    })
    sheet.format(f"B{new_row}:C{new_row}", {
        "numberFormat": {"type": "NUMBER", "pattern": "0.00"},
    })
    sheet.format(f"F{new_row}:K{new_row}", {
        "numberFormat": {"type": "NUMBER", "pattern": "0.00"},
    })
