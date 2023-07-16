import os
import discord
from dotenv import load_dotenv
import shopping
from . import misc
from . import makeups

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
    
@client.event
async def on_message(msg):
    if msg.content.startswith('!partytime') or msg.content == 'party time': # IMPORTANT DO NOT DELETE
        await msg.channel.send('where the bitches at')

    # food requests are made by prefacing the iterm with !
    # the food steward can generate a shopping list by typing !shoppinglist
    if msg.channel.name == 'food-requests':
        if msg.content.startswith('!shopping'):
            await shopping.make_shopping_list(msg)
    
    if 'emo' in msg.content.lower(): 
        await misc.emo(msg)

    if 'rat' in msg.content.lower() and not msg.author.bot:
        await misc.send_rat(msg)
        
    if msg.channel.name == 'chore-submissions' and not msg.author.bot:
        await msg.channel.send('slay')
        
    if msg.content == 'what':
        await msg.channel.send('chicken butt')
        
    # for the worm to create makeup chores
    if msg.channel.name == 'makeup-chores' and msg.author.get_role(WORM):
        await makeups.create_makeup(msg)
            
@client.event
async def on_raw_reaction_add(payload):
    # this will delete an item from the shopping list when reacted to
    if payload.channel_id == FS_DM_ID:
        await shopping.delete_item(payload)
                
    # allows claiming of makeup chore opportunities or deletion by worm
    if payload.channel_id == MAKEUP_ID:
        server = await client.fetch_guild(SERVER_ID)
        user = await server.fetch_member(payload.user_id)
        
        if not user.bot:
            channel = client.get_channel(MAKEUP_ID)
            message = await channel.fetch_message(payload.message_id)
            
            if message.author.bot:
                text = message.content
                await channel.delete_messages([message])
                
                if not user.get_role(WORM):
                    text = text.removesuffix('\nClick the check mark to claim this chore!')
                    text = f'{text}\n{user.display_name} claimed this chore!'
                    await channel.send(text)

client.run(token)




