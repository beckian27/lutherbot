import gspread
import json
import datetime

CHORE_CHANNEL = 1100529167201734657
# CHORE_CHANNEL = 1106246078472409201 #test channel

# key for matching discord names to names in the spreadsheet, needs to be manually updated
USERNAMES = {
    'failedcorporatecumslut': 'Lily Garcia',
    'cassie.eissac': 'Cassie Prokopowicz',
    'Devon_Risacher': 'Devon Risacher',
    '_nullwalker': 'DJ Mungo',
    'niickoliiver': 'Nick Oliver',
    'reckless__': 'Jacob Phelps',
    'abigailzoetewey': 'Abby Zoetewey',
    'Adam': 'Adam Kane',
    'Awmeo Azad': 'Awmeo Azad',
    'lights0123': 'Ben Schattinger',
    'benjyn.': 'Ben Nacht',
    'benrecht': 'Ben Recht',
    'brandon23669': 'Brandon Palomino-Alonso',
    'Emma0022': 'Emma Bassett',
    'haylie': 'Haylie Toth',
    'dathrax.': 'Jack Handzel',
    'johnfoxbro': 'John Fox',
    'lilianagarcia_73938': 'Lily Garcia',
    'crab3296': 'Ashton Ross',
    'mayaschne': 'Maya Schneider',
    'madisonisdead': 'Madison Dennis',
    'ndinolfo': 'Nate Dinolfo',
    'nohdinerman': 'Noah Dinerman',
    'elizabeth_camilli': 'Liz Camilli',
    'avameester': 'Ava Meester',
    'kushal9653': 'Kushal Sodum',
    'bict0': 'Victo Hungerman',
    'alexkautz': 'Alex Kautz',
    'ameninga': 'Amanda Meninga',
    'shirarb': 'Shira Baker',
    'raili.8': 'Raili Nelson',
    'laylahh8837': 'Laylah Perez',
    'tripforte': 'Shane Collins',
    'johnnyboy1341': 'Tyler Esch',
    'johnny boy': 'John Brink',
    'mauriciodk2': 'Mauricio Kaddatz',
    'haylie916': 'Haylie Toth',
    'lesbiancomrademiku': 'Rocke Ramsey'
}

NUMBER_EMOJIS = {'1️⃣': 1, '2️⃣': 2, '3️⃣': 3, '4️⃣': 4, '5️⃣': 5, '6️⃣': 6}

weekdays = {
            "Thursday": 0,
            "Friday": 1,
            "Saturday": 2,
            "Sunday": 3,
            "Monday": 4,
            "Tuesday": 5,
            "Wednesday": 6
            }

def sheets_init(): # connect to and return spreadsheet object
    gc = gspread.service_account(filename='creds.json')
    sh = gc.open('Winter 2024 Chore Schedule')
    return sh

def get_schedule(): # gets the chore schedule from the spreadsheet and stores it in a json
    # manually called whenever the chore schedule is updated
    sh = sheets_init()
    template = sh.worksheet('Schedule by Day')
    schedule = {}

    for column in range(1,10): # The chore schedule is 7 columns with the day names in the first row, then 2 cols of undated chores
        col = template.col_values(column)
        day, col = col[0], col[1::] # split data
        currentchore = ''

        for cell in col:
            # we can see if a cell is a chore name because it will end in the chore hour value
            if cell and cell[-1].isnumeric():
                cell = cell.replace('\n', ' ')
                currentchore, _ = cell.split(',')
                if column < 8:
                    currentchore = f'{day} {currentchore}'

            # nonblank cells following a chore will be names of participants
            elif cell and cell != 'Makeup':
                if cell not in schedule:
                    schedule[cell] = [currentchore]
                else:
                    schedule[cell].append(currentchore)

    # we store the schedule in a json for ease of data access and not making api calls all the time
    file = open('schedule.json', 'w')
    json.dump(schedule, file)

# triggered when the worm checks off a chore
async def submit_chore(msg):
    file = open('schedule.json', 'r')
    schedule = json.load(file)

    name = USERNAMES[msg.author.name]

    # send a message with a menu to select the correct chore
    choices = f'{name}, which chore are you submitting?'
    for index, chore in enumerate(schedule[name], start=1):
        choices += f'\n{index}: {chore}'

    # react with options to this message
    # when one is selected, triggers prepare_confirm()
    mymsg = await msg.reply(choices)
    for emoji in NUMBER_EMOJIS:
        if NUMBER_EMOJIS[emoji] <= len(schedule[name]):
            await mymsg.add_reaction(emoji)

# reformats the message to await confirmation of chore by the worm
async def prepare_confirm(payload, client):
    channel = client.get_channel(CHORE_CHANNEL)
    msg = await channel.fetch_message(payload.message_id)
    # splitting by space and getting the first two results gives the submitter's name
    name = msg.content.split()[0] + ' ' + msg.content.split()[1]
    name = name.strip(',')

    # convert number emoji to int using a dictionary to decode
    index = NUMBER_EMOJIS[str(payload.emoji)]
    # we find the chore name by breaking the message by line. Conviently, 1-indexing skips the first line of text
    chore = msg.content.split('\n')[index]
    chore = chore[chore.find(':') + 2:]
    msg = await msg.edit(content=f'{name}, {chore}')

    names = []
    file = open('schedule.json', 'r')
    schedule = json.load(file)
    for person in schedule:
        if chore in schedule[person]:
            if person not in [name, 'Makeup', 'Ian Beck...?']:
                names.append(person)
    
    # when the worm clicks this check, the chore will be approved
    await msg.add_reaction('✅')
    for person in names:
        mymsg = await msg.reply(f'Also submitting for {person}?')
        await mymsg.add_reaction('✅')
        await mymsg.add_reaction('❌')

    await msg.channel.send('slay')

async def confirm_teammate(msg, client):
    channel = client.get_channel(msg.reference.channel_id)
    choremsg = await channel.fetch_message(msg.reference.message_id)
    name = msg.content.removeprefix('Also submitting for ').strip('?')
    await choremsg.edit(content=f'{name}, {choremsg.content}')
    await channel.delete_messages([msg])


async def confirm_chore(payload, client):
    channel = client.get_channel(CHORE_CHANNEL)
    wholemsg = await channel.fetch_message(payload.message_id)
    msg = wholemsg.content.split(',')
    for i, word in enumerate(msg):
        msg[i] = word.strip()
    names, chore = msg[:-1], msg[-1]

    choreday = chore.split(' ')[0].strip(',')
    if choreday in weekdays:
        chore = chore[chore.find(' ') + 1:]
    else:
        choreday = ''
    submit_date = wholemsg.created_at # finds the date of the most recent thursday
    submit_date -= datetime.timedelta(hours=5) # convert from UTC to EST
    thursday_offset = (submit_date.isoweekday() + 3) % 7
    
    if choreday and thursday_offset < weekdays[choreday]: # someone is submitting a chore from the prev week
        thursday_offset += 7

    last_thursday = submit_date - datetime.timedelta(days=thursday_offset)
    last_thursday = datetime.date.strftime(last_thursday, "%m/%d/%Y")

    sheet_name = f'Week of {last_thursday}'
    sh = sheets_init()
    try:
        thisweek = sh.worksheet(sheet_name)
    except gspread.WorksheetNotFound:
        template = sh.worksheet('Schedule by Day')
        template.duplicate(new_sheet_name=sheet_name)
        thisweek = sh.worksheet(sheet_name)

    column = 8
    found = False # days are inconsistent with formatting so we have to parse for the chore
    if choreday:
        column = weekdays[choreday] + 1 #sheets 1-indexes
    for _ in range(2):
        if found:
            break
        col = thisweek.col_values(column)
        col = col[1:]
        row = 2 # skip the day name cell
        for cell in col:
            if found:
                if cell in names:
                    coord = chr(column + 64) + str(row)
                    thisweek.format(f'{coord}:{coord}', {
                        'backgroundColor': {
                        'red': 0.8509803921568627,
                        'green': 0.9176470588235294,
                        'blue': 0.8274509803921568
                    }})
                    names.remove(cell)
                    if not names:
                        break
            if cell.replace('\n', ' ').startswith(chore):
                found = True
            row += 1
        column = 9


    #simplify

