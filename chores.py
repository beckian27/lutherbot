import gspread
from oauth2client.service_account import ServiceAccountCredentials

def sheets_init():
    gc = gspread.service_account(filename='creds.json')
    gc.open('chore sched')

async def submit_chore(msg):
    return