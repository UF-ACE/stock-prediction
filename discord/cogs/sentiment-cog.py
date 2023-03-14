from discord.ext import commands

class Sentiment_Commands(commands.Cog):
    """Commands for retrieving sentiment data about a particular stock"""
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def news_sentiment(self, ctx, ticker, start, end):
        """Analyze sentiment of a given company for a given time period based on news headlines"""
        # Pass 'ticker' to some function for parsing input and ensuring it is valid
            # If invalid, return error message
        # Call backend functions for data retrieval and sentiment analysis
        pass

async def setup(bot):
    await bot.add_cog(Sentiment_Commands(bot))