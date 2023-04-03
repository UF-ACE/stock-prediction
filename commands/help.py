import requests
import os

VERSION = "1.0.0"

SENTIMENT = {
    "embeds": [
        {
            "title": "Sentiment Analysis",
            "description": "Performs sentiment analysis on a company based on recent (7d) news and social media posts.",
            "color": 0x00FF00,
            "fields": [
                {
                    "name": "Usage",
                    "value": "`/sentiment <company>`",
                    "inline": False
                },
                {
                    "name": "Parameters",
                    "value": "`company`: the company to analyze; can be a company name or ticker symbol",
                    "inline": False
                },
                {
                    "name": "Example",
                    "value": "`/sentiment Apple`",
                    "inline": False
                }
            ]
        }
    ] 
}
HELP = {
    "embeds": [
        {
            "title": "ACE Stock Bot",
            "description": "Use `/help <module>` to gain more information about that module :smiley:",
            "color": 0x00FF00,
            "fields": [
                {
                    "name": "Modules",
                    "value": "`sentiment`\nPerforms sentiment analysis on a company based on recent (7d) news and social media posts.",
                    "inline": False
                },
                {
                    "name": "About",
                    "value": "This bot is developed by UF ACE.\nPlease visit the [GitHub](https://github.com/UF-ACE/stock-prediction) to submit ideas or bugs.",
                    "inline": False
                }
            ],
            "footer": {
                "text": f"Bot is running version {VERSION}"
            }
        }
    ]
}


def help(options):
    # Check if the user wants more information about a module
    if options:
        module = options[0].get("value").lower()
        if module == "sentiment":
            return SENTIMENT
        else:
            raise Exception(f"Invalid module: {module}")
    
    # Else, send the help menu
    else:
        return HELP




