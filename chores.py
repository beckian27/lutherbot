import gspread
import google.auth
from googleapiclient.discovery import build


def sheets_init():
    gc = gspread.service_account(filename='creds.json')
    sh = gc.open('chore sched')
    print(sh.sheet1.get('A1'))





async def submit_chore(msg):
    return

# def get_values(spreadsheet_id, range_name):
#     """
#     Creates the batch_update the user has access to.
#     Load pre-authorized user credentials from the environment.
#     TODO(developer) - See https://developers.google.com/identity
#     for guides on implementing OAuth2 for the application.
#         """
#     creds, _ = google.auth.default()
#     # pylint: disable=maybe-no-member
#     try:
#         service = build('sheets', 'v4', credentials=creds)

#         result = service.spreadsheets().values().get(
#             spreadsheetId=spreadsheet_id, range=range_name).execute()
#         rows = result.get('values', [])
#         print(f"{len(rows)} rows retrieved")
#         return result
#     except HttpError as error:
#         print(f"An error occurred: {error}")
#         return error