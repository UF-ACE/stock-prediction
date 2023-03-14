from discord.ext import commands

class Help_Commands(commands.Cog): 
    """Commands for help and information about the bot"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def ping(self, ctx):
        """Pong! Check if the bot is alive"""
        await ctx.send("*Pong!*")

async def setup(bot):
    await bot.add_cog(Help_Commands(bot))