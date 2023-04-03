from utils.discord import Embedding

VERSION = "1.0.0"   # TODO: sync this with GitHub releases


def help(options: list[str]) -> Embedding:
    embed = None
    # Check if the user wants more information about a module
    if options:
        module = options[0].get("value").lower()
        if module == "sentiment":
            embed = Embedding("Sentiment Analysis", "Performs sentiment analysis on a company based on recent (7d) news and social media posts.", color=0x00FF00)
            embed.add_field("Usage", "`/sentiment <company>`", False)
            embed.add_field("Parameters", "`company`: the company to analyze; can be a company name or ticker symbol", False)
            embed.add_field("Example", "`/sentiment Apple`", False)
    
    # Else, send the help menu
    else:
        embed = Embedding("ACE Stock Bot", "Use `/help <module>` to gain more information about that module :smiley:", color=0x00FF00)
        embed.add_field("Modules", 
               "`sentiment`\nPerforms sentiment analysis on a company based on recent (7d) news and social media posts.\n \
                ",
                False)
        embed.add_field("About", "This bot is developed by UF ACE.\nPlease visit the [GitHub](https://github.com/UF-ACE/stock-prediction) to submit ideas or bugs.", False)

    embed.set_footer(f"Bot is running version {VERSION}")
    return embed



