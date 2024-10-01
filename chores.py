import gspread
import json
import datetime
import time

CHORE_CHANNEL = 1100529167201734657
# CHORE_CHANNEL = 1106246078472409201 #test channel

TRACKER = 'F24 Makeup & Fine Tracker'

# key for matching discord names to names in the spreadsheet, needs to be manually updated
USERNAMES = {
    'failedcorporatecumslut': 'Ian Beck',
    '_nullwalker': 'DJ Mungo',
    'reckless__': 'Jacob Phelps',
    'adam055593': 'Adam Kane',
    'lights0123': 'Ben Schattinger',
    'dathrax.': 'Jack Handzel',
    'johnfoxbro': 'John Fox',
    'lilianagarcia_73938': 'Lily Garcia',
    'crab3296': 'Ashton Ross',
    'madisonisdead': 'Madison Dennis',
    'nohdinerman': 'Noah Dinerman',
    'avameester': 'Ava Meester',
    'kushal9653': 'Kushal Sodum',
    'shirarb': 'Shira Baker',
    'raili.8': 'Raili Nelson',
    'laylahh8837': 'Laylah Perez',
    'tripforte': 'Shane Collins',
    'vanniboy239': 'John Brink',
    'lesbiancomrademiku': 'Rocke Ramsey',
    'abug22': 'Aaron Bugner',
    'fxjupiter': 'Charlie Swan',
    'yopinky': 'Olivia Korensky',
    'beelzeschlub418': 'Philip Tyler',
    'badbxtchslayer': 'Ella Lado',
    'juicyjchen': 'Jordan Chen',
    'redheadedmiddlechild': 'Kevin Alfaro-Ortiz',
    'gr0ss': 'Alex Alanis',
    'elianaaaa113': 'Eliana Levy',
    'ethanjohnson24': 'Ethan Johnson',
    'isopodbowls': 'Eve Sotham',
    'woba6y4748': 'Layla Salaheldin',
    'niickoliiver': 'Nick Oliver',
    'skalvert': 'Sasha Kalvert',
    'will019319': 'William McCall',
    '.deathbyhamster': 'Jagger Pacheco',
    'ioana.jpeg': 'Ioana Dumitrascu',
    'saucy_max': 'Max West',
    'clarina1113': 'Clarina Hsu',
    'babingobango': 'Ethan Marshall',
    'christjesus7971': 'Christian Loza',
    'lyrical0865': 'Lyric Okoro'
}

NUMBER_EMOJIS = {'1️⃣': 1, '2️⃣': 2, '3️⃣': 3, '4️⃣': 4, '5️⃣': 5, '6️⃣': 6}

weekdays = {
            "Thursday": 3,
            "Friday": 4,
            "Saturday": 5,
            "Sunday": 6,
            "Monday": 0,
            "Tuesday": 1,
            "Wednesday": 2
            }

def sheets_init(sheet_name): # connect to and return spreadsheet object
    gc = gspread.service_account(filename='creds.json')
    sh = gc.open(sheet_name)
    return sh

def get_schedule(): # gets the chore schedule from the spreadsheet and stores it in a json
    # manually called whenever the chore schedule is updated
    sh = sheets_init('Fall 2024 Chore Schedule')
    template = sh.worksheet('Schedule by Day')
    schedule = {}

    for column in range(1,9): # The chore schedule is 7 columns with the day names in the first row, then 2 cols of undated chores
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
                cell = cell.strip()
                if cell not in schedule:
                    schedule[cell] = [currentchore]
                else:
                    schedule[cell].append(currentchore)

    # we store the schedule in a json for ease of data access and not making api calls all the time
    file = open('schedule.json', 'w')
    json.dump(schedule, file)

    # this section updates the list the bot uses to track chore completion week-by-week
    #TODO remove old chores
    sh = sheets_init(TRACKER)
    chorelist = sh.worksheet('All Chore List')
    chores = chorelist.col_values(1)
    chores = chores[1:]
    row = len(chores) + 2
    
    rows_to_add = []
    for person in schedule:
        for chore in schedule[person]:
            if not f'{person}, {chore}' in chores:
                hours = 1
                # THIS SECTION MAY NEED TO BE MANUALLY ADJUSTED WITH NEW SCHEDULES
                if 'Cook' in chore and '\'' not in chore:
                    hours = 4
                elif 'After Din' in chore or 'Eve Kitchen' in chore:
                    hours = 2
                elif 'Porches' in chore:
                    hours = .5

                rows_to_add.append([f'{person}, {chore}', hours, 1])

    chorelist.update(f'A{row}:C{row + len(rows_to_add)}', rows_to_add)


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
    await msg.clear_reactions()
    await msg.add_reaction('✅')
    for person in names:
        mymsg = await msg.reply(f'Also submitting for {person}?')
        await mymsg.add_reaction('✅')
        await mymsg.add_reaction('❌')

    await msg.channel.send('Slay')

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

    update_tracker(names, chore)

    choreday = chore.split(' ')[0].strip(',')
    if choreday in weekdays:
        chore = chore[chore.find(' ') + 1:]
    else:
        choreday = ''
    submit_date = wholemsg.created_at # finds the date of the most recent monday
    submit_date -= datetime.timedelta(hours=5) # convert from UTC to EST
    monday_offset = submit_date.weekday()
    
    if choreday and monday_offset < weekdays[choreday]: # someone is submitting a chore from the prev week
        monday_offset += 7

    last_monday = submit_date - datetime.timedelta(days=monday_offset)
    last_monday = datetime.date.strftime(last_monday, "%m/%d/%Y")

    sheet_name = f'Week of {last_monday}'
    sh = sheets_init('Fall 2024 Chore Schedule')
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
                if cell.strip() in names:
                    coord = chr(column + 64) + str(row)
                    thisweek.format(f'{coord}:{coord}', {
                        'backgroundColor': {
                        'red': 0.8509803921568627,
                        'green': 0.9176470588235294,
                        'blue': 0.8274509803921568
                    }})
                    names.remove(cell.strip())
                    if not names:
                        break
            if cell.replace('\n', ' ').startswith(chore):
                found = True
            row += 1
        column = 9

def update_tracker(names, chore):
    tracker = sheets_init(TRACKER)
    chorelist = tracker.worksheet('All Chore List')
    chorenames = chorelist.col_values(1)
    for name in names:
        i = chorenames.index(f'{name}, {chore}') + 1
        while True: # TODO thread this to avoid blocking
            try:
                chorelist.update_cell(i, 3, 0)
                break
            except:
                time.sleep(60)
                continue


def generate_missed_chores():
    tracker = sheets_init(TRACKER)
    chorelist = tracker.worksheet('All Chore List')
    chores = chorelist.col_values(1)
    hours = chorelist.col_values(2)
    weeks_missed = chorelist.col_values(3)

    missed_chore_list = {}

    for index, hours in enumerate(weeks_missed, start=1):
        if int(hours) > 0:
            [name, chore] = chores[index].split(',')
            chore = chore.strip()

            if int(hours) > 1:
                chore = f'{chore}, {hours} weeks in a row'
            if name in missed_chore_list:
                missed_chore_list[name].append(chores[index])
            else:
                missed_chore_list[name] = [chores[index]]
    print(missed_chore_list)