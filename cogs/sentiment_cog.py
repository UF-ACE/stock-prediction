import discord
from discord.ext import commands
from utils import get_headlines, get_ticker, get_social_media, orange_or_blue


class sentiment(commands.Cog):
    """
    Commands for retrieving stock sentiment data from online sources.
    """
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def sentiment(self, ctx, *, query):
        """
        Analyze sentiment surrounding a given company based on news and social media data from the past week.
        Usage: $sentiment <company name>
        """
        # Retrieve the data
        message = await ctx.send("*Retrieving data...*")
        try:
            headlines = get_headlines(query)
            social_media = get_social_media(query)
            data = headlines + social_media
        except Exception as e:
            await message.edit(content=f"*Retrieving data...* Error!")
            embed = discord.Embed(title=f":x:  Error retrieving data for \'{query}\'", color=discord.Color.dark_red(),  
                                  description="Make sure you entered a valid, publicly traded company name.")
            await ctx.send(embed=embed)
            return
        await message.edit(content=f"*Retrieving data...* Done!")

        # Analyze the data
        message = await ctx.send("*Conducting analysis...*")
        # TODO: Analyze the data
        await message.edit(content=f"*Conducting analysis...* Done!")

        # Construct and send the results
        embed = discord.Embed(title=f"Sentiment Analysis for \'{query}\' ({get_ticker(query)})", color=orange_or_blue(), 
                              description=f"Analysis is based on **{len(headlines)}** headlines and **{len(social_media)}** posts from the past week.")
        # TODO: Add sample headlines + posts to the embed
        # TODO: Add the results to the embed
        # TODO: Add warning if there is not enough data
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(sentiment(bot))