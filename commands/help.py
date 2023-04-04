from utils.discord import Embedding


def help(options: list[dict]) -> Embedding:
    embed = None
    # Send the help menu if requested
    if not options or options[0].get("value") == "help":
        embed = Embedding("ACE Stock Bot", "Use `/help <command>` to gain more information about that command :smiley:", color=0x00FF00)
        embed.add_field("Commands", 
               "`sentiment`\nPerforms sentiment data collection and analysis.\n",
                False)
        embed.add_field("About", 
                        "This bot is developed by UF ACE.\n" \
                        "Please visit the [GitHub](https://github.com/UF-ACE/stock-prediction) to submit ideas or bugs.\n",
                        False)

    # Check which command the user would like info on
    elif options[0].get("value") == "sentiment":
        embed = Embedding("Sentiment Analysis", "Collects data, performs sentiment analysis on a company based on news and social media posts.", color=0x00FF00)
        embed.add_field("Usage", "`/sentiment <type> <company> <interval>`", False)
        embed.add_field("Parameters", 
                        "`type`: can be \"data\" or \"analyze\" to choose between (only) collecting data or running an analysis\n" \
                        "`company`: the company to analyze; can be a company name or ticker symbol\n" \
                        "`interval`: the timespan (days into the past) to collect data from; must be in [1, 365]; default is 7 days\n", 
                        False)
        embed.add_field("Examples", 
                        "`/sentiment data Apple`\n" \
                        "`/sentiment analyze AAPL 30`\n",
                         False)
        
    return embed



