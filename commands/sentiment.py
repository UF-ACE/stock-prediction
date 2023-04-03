from utils import get_ticker
from utils.discord import Embedding
from utils.sentiment import get_headlines, get_social_media


def sentiment(options: list[str]) -> dict:
    # Retrieve the data
    query = options[0].get("value")
    headlines = get_headlines(query)
    social_media = get_social_media(query)
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
        