import gspread
import json

CHORE_CHANNEL = 1106246078472409201 #1100529167201734657
# global USERNAMES
USERNAMES = {
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

# global NUMBER_EMOJIS
NUMBER_EMOJIS = {'1️⃣': 1, '2️⃣': 2, '3️⃣': 3, '4️⃣': 4, '5️⃣': 5, '6️⃣': 6}

def sheets_init():
    gc = gspread.service_account(filename='creds.json')
    sh = gc.open('chore sched')

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

    file = open('schedule.json', 'w')
    json.dump(schedule, file)

async def submit_chore(msg):
    file = open('schedule.json', 'r')
    schedule = json.load(file)

    name = USERNAMES[msg.author.name]
    chore_list = []
    for index in range(0, len(schedule[name]), 2):
        chore_list.append(schedule[name][index])

    choices = f'{name}, which chore are you submitting?'
    for index in range(len(chore_list)):
        choices = choices + f'\n{index + 1}: {chore_list[index]}'

    mymsg = await msg.reply(choices)
    for emoji in NUMBER_EMOJIS:
        if NUMBER_EMOJIS[emoji] <= len(chore_list):
            await mymsg.add_reaction(emoji)

async def prepare_confirm(payload, client):
    channel = client.get_channel(CHORE_CHANNEL)
    msg = await channel.fetch_message(payload.message_id)
    name = msg.content.split()[0] + ' ' + msg.content.split()[1]
    print(name)
    name.strip(', \n')
    print(name)

    index = NUMBER_EMOJIS[str(payload.emoji)]
    chore = msg.content.split('\n')[index].strip('123456: ')
    msg = await msg.edit(content=f'{name}, {chore}')
    await msg.add_reaction('✅')

async def confirm_chore(payload, client):
    channel = client.get_channel(CHORE_CHANNEL)
    msg = await channel.fetch_message(payload.message_id)
    msg = msg.content.split(',')
    [name, chore] = msg
    chore.strip()
    print(name, chore)
