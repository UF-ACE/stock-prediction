import datetime
from utils import get_ticker
from utils.sentiment import get_headlines, get_social_media
from discord_lambda import Embedding, CommandRegistry, Interaction, CommandArg


def sentiment(inter: Interaction, type: str, query: str, start: int) -> None:
    # Parse the arguments
    if start < 1:
        start = 1
    elif start > 30:
        start = 30
    
    start = (datetime.datetime.now() - datetime.timedelta(days=start)).strftime("%Y-%m-%d")

    # TODO: Split the following into two commands: one just for data, one for both data and analysis

    # Get the data
    ticker = get_ticker(query)
    headlines = get_headlines(query, ticker, start)
    social_media = get_social_media(ticker, start)

    # Create the embed
    embed = Embedding(f"Sentiment Analysis for \'{query}\' ({get_ticker(query)})", f"Analysis based on {len(headlines)} headlines and {len(social_media)} social media posts.", color=0x00FF00)
    embed.add_field("Headlines", "This is a sample value.", False)
    embed.add_field("Social Media", "This is a sample value.", False)

    if type == "data":
        inter.send_response(embeds=[embed])
        return
    
    data = headlines + social_media

    # TODO: Analyze the data

    # TODO: Add sample headlines + posts to the embed
    # TODO: Add the results to the embed
    # TODO: Add warning if there is not enough data

    # Send the embed -> TODO: fill out the embed
   
    embed.add_field("Results", "This is a sample value.", False)
    inter.send_response(embeds=[embed])


def setup(registry: CommandRegistry):
    registry.register_cmd(func=sentiment, name="sentiment", desc="Collects data, performs sentiment analysis on a company based on news and social media posts.", options=[
        CommandArg("type", "can be \"data\" or \"analyze\" to choose between (only) collecting data or running an analysis", CommandArg.Types.STRING, choices=[
            CommandArg.Choice("data"),
            CommandArg.Choice("analyze")
        ]),
        CommandArg("company", "the company to analyze; can be a company name or ticker symbol", CommandArg.Types.STRING),
        CommandArg("interval", "the timespan (days into the past) to collect data from; must be in [1, 30]; default is 7 days", CommandArg.Types.INTEGER, required=False)
    ])


        