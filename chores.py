import gspread
import json

global usernames
usernames = {
    'failedcorporatecumslut': 'Ian Beck',
    'benmech99': 'Ben Portelli',
    'cassie.eissac': 'Cassie Prokopowicz',
    'Devon_Risacher': 'Devon Risacher',
    '_nullwalker': 'DJ Mungo',
    'frog': 'Jonah Nunez',
    'maebh': 'Maebh Ring',
    'Michaela Bell': 'Michaela Bell',
    'niickoliiver': 'Nick Oliver',
    'pixiesharts': 'Emma Grindon',
    'shannonmarm': 'Shannon Armstrong',
    'sugarsean': 'Shane Collins'
}


def sheets_init():
    gc = gspread.service_account(filename='creds.json')
    sh = gc.open('chore sched')
    print(sh.sheet1.get('A1'))
    get_schedule(sh)

def get_schedule(sh):
    template = sh.worksheet('Template (Edit Here)')
    schedule = {}
    for column in range(1,7):
        col = template.col_values(column)
        day, col = col[0], col[1::]
        currentchore = ''
        hours = 0
        for cell in col:
            if cell and cell[-1].isnumeric():
                cell = cell.replace('\n', '')
                currentchore, hours = cell.split(',')
                hours.strip()
                currentchore = f'{day} {currentchore}'
                #print(cell)

            elif cell and cell != 'MAKEUP OP':
                if '/' in cell:
                    cell, otherperson = cell.split('/')
                    if otherperson not in schedule:
                        schedule[otherperson] = [currentchore, hours]
                    else:
                        schedule[otherperson].append(currentchore)
                        schedule[otherperson].append(hours)
                if cell not in schedule:
                    schedule[cell] = [currentchore, hours]
                else:
                    schedule[cell].append(currentchore)
                    schedule[cell].append(hours)

    json.dump(schedule, 'schedule.json')
                    
                





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