import os
import discord
from dotenv import load_dotenv


load_dotenv()
token = os.getenv("token")
client = discord.Client(intents=discord.Intents.all())
    
@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")
    
@client.event
async def on_message(msg):
    if msg.content.startswith("!partytime"):
        await msg.channel.send('where the bitches at')
        
    print(msg.channel)
client.run(token)
