import os
import discord
from discord import app_commands
from dotenv import load_dotenv
import shopping
import misc
import makeups
import chores
import datetime

GREEN_CHECK = '\U00002705'
SHOPPING_ID = 1110021975109288006
MAKEUP_ID = 1115356156307718144
SERVER_ID = 1100528927803461634
WORM = 1103462042490384434
PREZ = 1103461097803092079
FOOD_STEWARD = 1103461475152039956

load_dotenv() # store the discord token in a text file called ".env"
token = os.getenv('token') # im sure this is super secure but idrc
client = discord.Client(intents=discord.Intents.all()) # lets the bot do whatever it wants
tree = app_commands.CommandTree(client) # this is for commands

    
@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=SERVER_ID))
    print(f'{client.user} has connected to Discord!')
    chores.sheets_init()

@tree.command(
    name="update",
    description="Updates the stored list of chores",
    guild=discord.Object(id=SERVER_ID)
)
async def first_command(interaction):
    chores.get_schedule()
    await interaction.response.send_message("Schedule updated!")

    
@client.event
async def on_message(msg):
    # food requests are made by prefacing the term with !
    # the food steward can generate a shopping list by typing !shoppinglist
    if msg.channel.name == 'food-requests':
        if msg.content.startswith('!shopping') and (msg.author.get_role(FOOD_STEWARD) or msg.author.name == 'failedcorporatecumslut'):
            await shopping.make_shopping_list(msg, client, SHOPPING_ID, GREEN_CHECK)

    # for the worm to create makeup chores
    elif msg.channel.name == 'makeup-opportunities' and msg.author.get_role(WORM):
        await makeups.create_makeup(msg, GREEN_CHECK)

    elif msg.channel.name == 'chore-submissions' and not msg.author.bot:
        if msg.attachments:
            await chores.submit_chore(msg)
        
        if msg.content.startswith('!update') and msg.author.get_role(WORM):
            chores.get_schedule()
    
    if 'emo' in msg.content.lower(): 
        await misc.emo(msg)

    if 'rat' in msg.content.lower() and not msg.author.bot:
        await misc.send_rat(msg)

    if msg.author.name == 'vivcifi' and msg.content.lower() == 'shut up':
        await misc.shut_up(msg)
                
    if msg.content.lower() == 'what':
        await msg.channel.send('chicken butt')

    if msg.author.name in ['emma0022_', 'brandon23669']:
        await msg.channel.send('meow')

    if 'meow' in msg.content.lower() and not msg.author.bot:
        print('todo')

    if msg.channel.name == 'bot-test':
        print(msg.created_at)
            
@client.event
async def on_raw_reaction_add(payload):
    # this will delete an item from the shopping list when reacted to
    if payload.channel_id == SHOPPING_ID:
        await shopping.delete_item(payload, client, SHOPPING_ID)
                
    # allows claiming of makeup chore opportunities or deletion by worm
    elif payload.channel_id == MAKEUP_ID:
        await makeups.claim_makeup(payload, client, SERVER_ID, MAKEUP_ID, WORM)

    if payload.channel_id == chores.CHORE_CHANNEL:
        server = await client.fetch_guild(SERVER_ID)
        user = await server.fetch_member(payload.user_id)

        if not user.bot:
            channel = client.get_channel(chores.CHORE_CHANNEL)
            msg = await channel.fetch_message(payload.message_id)
            if msg.content.startswith('Also submitting for '):
                if str(payload.emoji) == '✅':
                    await chores.confirm_teammate(msg, client)
                elif str(payload.emoji) == '❌':
                    channel = client.get_channel(chores.CHORE_CHANNEL)
                    await channel.delete_messages([msg])

            elif str(payload.emoji) == '✅' and user.get_role(WORM):
                await chores.confirm_chore(payload, client)
            elif str(payload.emoji) in chores.NUMBER_EMOJIS:
                await chores.prepare_confirm(payload, client)

client.run(token)

# lutherbot@lutherbot.iam.gserviceaccount.com
