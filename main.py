import os
import discord
from dotenv import load_dotenv

CHECK_MARK_CODE = '\U00002705'
FS_DM_ID = 1106246078472409201 #hardcode the DM where the shopping list is generated

load_dotenv()
token = os.getenv('token')
client = discord.Client(intents=discord.Intents.all())

    
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    
@client.event
async def on_message(msg):
    if msg.content.startswith('!partytime'): # IMPORTANT DO NOT DELETE
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
            
            fs_dm = client.get_channel(FS_DM_ID)    

            # generates alphabetized shopping list in DM channel
            # adds a reaction to each item to act as a check off button
            for request in sorted(requests):
                mymsg = await fs_dm.send(request)
                await mymsg.add_reaction(CHECK_MARK_CODE)
    
    if 'emo' in msg.content.lower():
        if not msg.author.bot and 'gay boy' not in msg.author.roles:
            await msg.channel.send('"Real Emo" only consists of the dc Emotional Hardcore scene and the late 90\'s Screamo scene. What is known by "Midwest Emo" is nothing but Alternative Rock with questionable real emo influence. When people try to argue that bands like My Chemical Romance are not real emo, while saying that Sunny Day Real Estate is, I can\'t help not to cringe because they are just as fake emo as My Chemical Romance (plus the pretentiousness). Real emo sounds ENERGETIC, POWERFUL and somewhat HATEFUL. Fake emo is weak, self pity and a failed attempt to direct energy and emotion into music. Some examples of REAL EMO are Pg 99, Rites of Spring, Cap n Jazz (the only real emo band from the midwest scene) and Loma Prieta. Some examples of FAKE EMO are American Football, My Chemical Romance and Mineral EMO BELONGS TO HARDCORE NOT TO INDIE, POP PUNK, ALT ROCK OR ANY OTHER MAINSTREAM GENRE')

@client.event
async def on_raw_reaction_add(payload):
    # this will delete an item from the shopping list when reacted to
    if payload.channel_id == FS_DM_ID:
        user = await client.fetch_user(payload.user_id)
        
        if not user.bot:
            fs_dm = client.get_channel(FS_DM_ID)
            message = await fs_dm.fetch_message(payload.message_id)
            
            if message.author.bot:
                await fs_dm.delete_messages([message])

client.run(token)
