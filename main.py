# import library
import discord
from discord.ext import commands
import instaloader
# inisialisasi variable
prefix = "!"
bot = instaloader.Instaloader()
emot = ['🐄', '🐎', '🐖', '🐏', '🐑', '🦙', 
        '🐐', '🦌', '🐕', '🐩', '🦮', '🐕‍🦺', 
        '🐈','🐄', '🐎', '🐖', '🐏', '🐑', 
        '🦙', '🐐', '🦌', '🐕', '🐩', '🦮',
          '🐕‍🦺', '🐈']
intents = discord.Intents.all()
intents.message_content = True
client = commands.Bot(command_prefix=prefix, intents=intents)
# client = discord.Client( intents=intents )

exec(open("client.py",encoding='utf-8').read())
