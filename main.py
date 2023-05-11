import os
import discord
from dotenv import load_dotenv


load_dotenv()
token = os.getenv("token")
client = discord.Client(discord.Intents.all())
client.run(str(token))
    
@client.event
async def on_ready():
    print(f"{client.user} has connected to Discord!")