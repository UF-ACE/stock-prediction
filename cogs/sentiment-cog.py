import os
import sys
from discord.ext import commands
from sentiment.headlines import retrieve_headlines

class Sentiment(commands.Cog):
    """
    Commands for retrieving sentiment data from online sources
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def news_sentiment(self, ctx, *, ticker):
        """
        Analyze sentiment surrounding a given company based on news headlines from the past week
        """
        # Try to retrieve headlines
        await ctx.send(f"***Retrieving news articles for {ticker}...***")
        try:
            headlines_list = retrieve_headlines(ticker)
        except Exception as e:
            await ctx.send(f"**Error:** {e}")
            return
        
        # Send 5 of the headlines in chat
        await ctx.send("Here's some that I found:")
        for i, headline in enumerate(headlines_list):
            if i == 5:
                break
            await ctx.send(f"{i+1}. {headline}")
        
        # Try to analyze sentiment
        await ctx.send("***Analyzing sentiment...***")


async def setup(bot):
    await bot.add_cog(Sentiment(bot))