import datetime
from utils import get_ticker, add_footer
from utils.sentiment import get_headlines, get_social_media
from discord_lambda import Embedding, CommandRegistry, Interaction, CommandArg


def sentiment(inter: Interaction, type: str, query: str, interval: int = 7) -> None:
    # Parse the arguments
    if interval < 1:
        interval = 1
    elif interval > 30:
        interval = 30
    
    start = (datetime.datetime.now() - datetime.timedelta(days=interval)).strftime("%Y-%m-%d")

    # TODO: Split the following into two commands: one just for data, one for both data and analysis

    # Get the data
    ticker = get_ticker(query)
    headlines = get_headlines(query, ticker, start)
    social_media = get_social_media(ticker, start)

    # Create the embed
    embed = Embedding(f"Sentiment Analysis for \'{query}\' ({get_ticker(query)})", f"Analysis based on {len(headlines)} headlines and {len(social_media)} social media posts.", color=0x00FF00)
    add_footer(inter.timestamp, embed)
    embed.add_field("Headlines", "This is a sample value.", False)
    embed.add_field("Social Media", "This is a sample value.", False)

    if type == "collect":
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
    registry.register_cmd(func=sentiment, name="sentiment", desc="Collect, analyze sentiment data", options=[
        CommandArg("type", "\"collect\" or \"analyze\"", CommandArg.Types.STRING, choices=[
            CommandArg.Choice("collect"),
            CommandArg.Choice("analyze")
        ]),
        CommandArg("query", "Company name or ticker", CommandArg.Types.STRING),
        CommandArg("interval", "Timespan in [1, 30] days; default = 7", CommandArg.Types.INTEGER, required=False)
    ])


        