import requests
import os
from utils import get_headlines, get_ticker, get_social_media


def sentiment(options):
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
    return {
        "embeds": [
            {
                "title": f"Sentiment Analysis for \'{query}\' ({get_ticker(query)})",
                "description": f"Analysis based on {len(headlines)} headlines and {len(social_media)} social media posts.",
                "color": 0x00FF00,
                "fields": [
                    {
                        "name": "Headlines",
                        "value": "This is a sample value.",
                        "inline": False
                    },
                    {
                        "name": "Social Media",
                        "value": "This is a sample value.",
                        "inline": False
                    },
                    {
                        "name": "Results",
                        "value": "This is a sample value.",
                        "inline": False
                    }
                ]
            }
        ]
    }
        