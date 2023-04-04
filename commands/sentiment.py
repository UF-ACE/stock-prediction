import datetime
from utils import get_ticker
from utils.discord import Embedding
from utils.sentiment import get_headlines, get_social_media


def sentiment(options: list[dict]) -> Embedding:
    # Parse the arguments
    sub_command = options[0]
    args = sub_command.get("options")
    query = args[0].get("value")
    start = 7 if len(args) == 1 else args[1].get("value")

    if start > 30:
        start = 30
    elif start < 1:
        start = 1
    
    start = (datetime.datetime.now() - datetime.timedelta(days=start)).strftime("%Y-%m-%d")

    # TODO: Split the following into two commands: one just for data, one for both data and analysis

    # Get the data
    ticker = get_ticker(query)
    headlines = get_headlines(query, ticker, start)
    social_media = get_social_media(ticker, start)
    data = headlines + social_media

    # TODO: Analyze the data

    # TODO: Add sample headlines + posts to the embed
    # TODO: Add the results to the embed
    # TODO: Add warning if there is not enough data

    # Send the embed -> TODO: fill out the embed
    embed = Embedding(f"Sentiment Analysis for \'{query}\' ({get_ticker(query)})", f"Analysis based on {len(headlines)} headlines and {len(social_media)} social media posts.", color=0x00FF00)
    embed.add_field("Headlines", "This is a sample value.", False)
    embed.add_field("Social Media", "This is a sample value.", False)
    embed.add_field("Results", "This is a sample value.", False)
    return embed


        