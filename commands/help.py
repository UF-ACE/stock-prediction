from utils.discord import Embedding

VERSION = "1.0.0"   # TODO: sync this with GitHub releases


def help(options: list[dict]) -> Embedding:
    embed = None
    # Send the help menu if requested
    if not options or options[0].get("value") == "help":
        embed = Embedding("ACE Stock Bot", "Use `/help <module>` to gain more information about that module :smiley:", color=0x00FF00)
        embed.add_field("Modules", 
               "`sentiment`\nPerforms sentiment analysis on a company based on recent (7d) news and social media posts.\n \
                ",
                False)
        embed.add_field("About", "This bot is developed by UF ACE.\nPlease visit the [GitHub](https://github.com/UF-ACE/stock-prediction) to submit ideas or bugs.", False)

    # Check which module the user would like info on
    elif options[0].get("value") == "sentiment":
        embed = Embedding("Sentiment Analysis", "Collects data and performs sentiment analysis on a company based on news and social media posts.", color=0x00FF00)
        embed.add_field("Usage", "`/sentiment <type> <company> <interval>`", False)
        embed.add_field("Parameters", 
                        "`type`: can be \"data\" or \"analze\" to choose between just collecting data or running an analysis\n"
                        "`company`: the company to analyze; can be a company name or ticker symbol\n \
                        `interval`: the timespan (days into the past) to collect data from; must be in [1, 365]; default is 7 days", 
                        False)
        embed.add_field("Examples", "`/sentiment data Apple`\n \
                                     `/sentiment analyze AAPL 30`",
                         False)
        

    embed.set_footer(f"Bot is running version {VERSION}")
    return embed



