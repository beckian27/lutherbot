import os
import random
import discord
from dotenv import load_dotenv

CHECK_MARK_CODE = '\U00002705'
FS_DM_ID = 1110021975109288006 #hardcode the DM where the shopping list is generated
WORM = 1103462042490384434

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
        if msg.content.startswith('!shoppinglist'):
            requests = []
            async for request in msg.channel.history(limit = 2000, before = msg):
                # scans messages until previous list request
                if request.content.startswith('!shoppinglist'):
                    break
                if request.content.startswith('!'):
                    requests.append(request.content.strip('!'))
            
            fs_dm = client.get_channel(FS_DM_ID)    

            # generates alphabetized shopping list in private channel
            # adds a reaction to each item to act as a check off button
            for request in sorted(requests):
                mymsg = await fs_dm.send(request)
                await mymsg.add_reaction(CHECK_MARK_CODE)
                
            copypaste = '' # also sends a single copy-pasteable message for this who prefer not to use this
            for request in sorted(requests):
                if len(copypaste) > 1950: # if message approches discord char limit
                    await fs_dm.send(copypaste)
                    copypaste = ''

                copypaste = copypaste + request + '\n'
                
            
            await fs_dm.send(copypaste)
    
    if 'emo' in msg.content.lower(): 
        if not msg.author.bot:
            taz = False # taz is immune to the emo copypasta
            for role in msg.author.roles:
                if role.name == 'gay boy':
                    taz = True
                    break
            if not taz:
                await msg.channel.send('"Real Emo" only consists of the dc Emotional Hardcore scene and the late 90\'s Screamo scene. What is known by "Midwest Emo" is nothing but Alternative Rock with questionable real emo influence. When people try to argue that bands like My Chemical Romance are not real emo, while saying that Sunny Day Real Estate is, I can\'t help not to cringe because they are just as fake emo as My Chemical Romance (plus the pretentiousness). Real emo sounds ENERGETIC, POWERFUL and somewhat HATEFUL. Fake emo is weak, self pity and a failed attempt to direct energy and emotion into music. Some examples of REAL EMO are Pg 99, Rites of Spring, Cap n Jazz (the only real emo band from the midwest scene) and Loma Prieta. Some examples of FAKE EMO are American Football, My Chemical Romance and Mineral EMO BELONGS TO HARDCORE NOT TO INDIE, POP PUNK, ALT ROCK OR ANY OTHER MAINSTREAM GENRE')

    if 'rat' in msg.content.lower() and not msg.author.bot:
        pic = random.choice(
            [
                'https://www.peta.org/wp-content/uploads/2015/04/10903825_872344489483233_7702124773103899276_o-668x336.jpg?20190103121630',
                'https://imgur.com/r7WkJOX',
                'https://media.istockphoto.com/id/1197373509/photo/a-grey-pet-rat-sits-on-a-toy-motorcycle.jpg?s=170667a&w=0&k=20&c=wHXqWJ5NB4TmNbzwYm9KclN8gcsSRIWBJlfwGk0jehY=',
                'https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/46_Dick_Cheney_3x4.jpg/640px-46_Dick_Cheney_3x4.jpg',
            ]
            
        )
        await msg.channel.send(pic)
        
    if msg.channel.name == 'chore-submissions' and not msg.author.bot:
        await msg.channel.send('slay')
        
    if msg.content == 'what':
        await msg.channel.send('chicken butt')
        
    if msg.channel.name == 'makeup-chores' and msg.author.get_role(WORM):
        if msg.content.startswith('!makeup'):
            opportunity = msg.content.removeprefix('!makeup ')
            opportunity = opportunity + '\n Click the check mark to claim this chore!'
            await msg.channel.delete_messages([msg])
            msg = await msg.channel.send(opportunity)
            await msg.add_reaction(CHECK_MARK_CODE)
            
        
        

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


