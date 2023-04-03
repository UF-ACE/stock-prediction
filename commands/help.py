from utils import Embedding

VERSION = "1.0.0"

SENTIMENT = Embedding("Sentiment Analysis", "Performs sentiment analysis on a company based on recent (7d) news and social media posts.", color=0x00FF00)
SENTIMENT.add_field("Usage", "`/sentiment <company>`", False)
SENTIMENT.add_field("Parameters", "`company`: the company to analyze; can be a company name or ticker symbol", False)
SENTIMENT.add_field("Example", "`/sentiment Apple`", False)
SENTIMENT.set_footer(f"Bot is running version {VERSION}")

HELP = Embedding("ACE Stock Bot", "Use `/help <module>` to gain more information about that module :smiley:", color=0x00FF00)
HELP.add_field("Modules", "`sentiment`\nPerforms sentiment analysis on a company based on recent (7d) news and social media posts.", False)
HELP.add_field("About", "This bot is developed by UF ACE.\nPlease visit the [GitHub](https://github.com/UF-ACE/stock-prediction) to submit ideas or bugs.", False)
HELP.set_footer(f"Bot is running version {VERSION}")


def help(options: list[str]) -> Embedding:
    # Check if the user wants more information about a module
    if options:
        module = options[0].get("value").lower()
        if module == "sentiment":
            return SENTIMENT
    
    # Else, send the help menu
    else:
        return HELP




