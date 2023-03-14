import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())

@bot.event
async def on_ready():
    for file in os.listdir('discord/cogs/'):
        if file.endswith('.py'):
            await bot.load_extension(f'cogs.{file[:-3]}')
    print(f'{bot.user.name} has connected to Discord!')

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)