import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())
bot.remove_command('help')

@bot.event
async def on_ready():
    for file in os.listdir('cogs/'):
        if file.endswith('.py') and file != '__init__.py':
            await bot.load_extension(f'cogs.{file[:-3]}')
    print(f'{bot.user.name} has connected to Discord!')

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)