import os
import discord
from dotenv import load_dotenv

CHECK_MARK_CODE = '\U00002705'
FS_DM_ID = 1106246078472409201


load_dotenv()
token = os.getenv("token")
client = discord.Client(intents=discord.Intents.all())
    
@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    
@client.event
async def on_message(msg):
    if msg.content.startswith("!partytime"): # IMPORTANT DO NOT DELETE
        await msg.channel.send('where the bitches at')

    if msg.channel.name == 'bot-test':
        if msg.content.startswith('!shoppinglist'):
            requests = []
            async for request in msg.channel.history(limit = 2000, before = msg):
                # scans messages until previous list request
                if request.content.startswith('!shoppinglist'):
                    break
                if request.content.startswith('!'):
                    requests.append(request.content.strip('!'))
                    
            FS_DM = client.get_channel(FS_DM_ID)

            for request in sorted(requests):
                await FS_DM.send(request)
                
            
    if msg.content == 'test':
        mymsg = await msg.channel.send('reaction')
        await mymsg.add_reaction(CHECK_MARK_CODE)
        

client.run(token)
