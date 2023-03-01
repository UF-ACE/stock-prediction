import os
import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='$', intents=discord.Intents.all())

class Help_Commands(commands.Cog): 
    """Commands for help and information about the bot"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Pong! Check if the bot is alive"""
        await ctx.send("*Pong!*")

class Sentiment_Commands(commands.Cog):
    """Commands for retrieving sentiment data about a particular stock"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def sentiment(self, ctx, ticker, days):
        """Analyze sentiment of a given stock"""
        # Pass 'ticker' to some function for parsing input and ensuring it is valid
            # If invalid, return error message
        # Call backend functions for data retrieval and sentiment analysis
        pass

@bot.event
async def on_ready():
    await bot.add_cog(Help_Commands(bot))
    await bot.add_cog(Sentiment_Commands(bot))
    print(f'{bot.user.name} has connected to Discord!')

if __name__ == "__main__":
    bot.run(TOKEN)