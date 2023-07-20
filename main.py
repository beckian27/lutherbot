import os
import discord
from dotenv import load_dotenv
import shopping
import misc
import makeups
import chores

CHECK_MARK_CODE = '\U00002705'
FS_DM_ID = 1110021975109288006 #hardcode the DM where the shopping list is generated
MAKEUP_ID = 1115356156307718144
SERVER_ID = 1100528927803461634
WORM = 1103462042490384434
PREZ = 1103461097803092079

load_dotenv() # store the discord token in a text file called ".env"
token = os.getenv('token') # im sure this is super secure but idrc
client = discord.Client(intents=discord.Intents.all()) # lets the bot do whatever it wants
    
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    chores.sheets_init()

    
@client.event
async def on_message(msg):
    # food requests are made by prefacing the term with !
    # the food steward can generate a shopping list by typing !shoppinglist
    if msg.channel.name == 'food-requests':
        if msg.content.startswith('!shopping'):
            await shopping.make_shopping_list(msg, client, FS_DM_ID, CHECK_MARK_CODE)

    # for the worm to create makeup chores
    elif msg.channel.name == 'makeup-chores' and msg.author.get_role(WORM):
        await makeups.create_makeup(msg, CHECK_MARK_CODE)
    
    if 'emo' in msg.content.lower(): 
        await misc.emo(msg)

    if 'rat' in msg.content.lower() and not msg.author.bot:
        await misc.send_rat(msg)
        
    if msg.channel.name == 'chore-submissions' and not msg.author.bot:
        await msg.channel.send('slay')
        
    if msg.content == 'what':
        await msg.channel.send('chicken butt')
    
    if msg.content.startswith('!partytime') or msg.content == 'party time': # IMPORTANT DO NOT DELETE
        await msg.channel.send('where the bitches at')

    if 'penis' in msg.content.lower():
        await misc.penis(client)

    if msg.channel.name == 'bot-test':
        # if msg.attachments:
        #     print('hi')
        chores.submit_chore()
            
@client.event
async def on_raw_reaction_add(payload):
    # this will delete an item from the shopping list when reacted to
    if payload.channel_id == FS_DM_ID:
        await shopping.delete_item(payload, client, FS_DM_ID)
                
    # allows claiming of makeup chore opportunities or deletion by worm
    elif payload.channel_id == MAKEUP_ID:
        await makeups.claim_makeup(payload, client, SERVER_ID, MAKEUP_ID, WORM)

    if payload.channel_id == 1106246078472409201:
        print(str(payload.emoji))
        if str(payload.emoji) == CHECK_MARK_CODE:
            print('yay')

client.run(token)

# lutherbot@lutherbot.iam.gserviceaccount.com
