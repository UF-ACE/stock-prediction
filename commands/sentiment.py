import datetime
from utils import get_ticker, add_footer
from utils.sentiment import get_headlines, get_social_media, analyze_data
from discord_lambda import Embedding, CommandRegistry, Interaction, CommandArg


def collect_helper(embed: Embedding, headlines: list[dict], social_media: list[dict]) -> None:
    # Add sample headlines
    headlines_samples = ""
    for i, headline in enumerate(headlines[:5]):
        headlines_samples += f"{i+1}. [{headline['title']}]({headline['link']})\n"
    embed.add_field("News Headlines", headlines_samples, True)

    # Add sample social media posts
    social_media_samples = ""
    for i, post in enumerate(social_media[:5]):
        social_media_samples += f"{i+1}. [{post['title']}]({post['link']})\n"
    embed.add_field("Social Media Posts", social_media_samples, True)


def analyze_helper(embed: Embedding, headlines: list[dict], social_media: list[dict]) -> None:
    # Run the analysis
    headlines_avg = analyze_data(headlines)
    social_media_avg = analyze_data(social_media)

    # Add headline samples and results
    headlines_samples = ""
    for i, headline in enumerate(headlines[:5]):
        headlines_samples += f"{i+1}. [{headline['title']}]({headline['link']})\n"

    headlines_sentiment = ""
    for i, headline in enumerate(headlines[:5]):
        headlines_sentiment += f"{i+1}. {round(headline['score'], 2)} - {headline['sentiment']}\n"
    headlines_sentiment += f"**Average:** {round(headlines_avg, 2)}"

    embed.add_field("News Headlines", headlines_samples, True)
    embed.add_field("Sentiment", headlines_sentiment, True)
    embed.add_field("", "", False)

    # Add social media samples and results
    social_media_samples = ""
    for i, post in enumerate(social_media[:5]):
        social_media_samples += f"{i+1}. [{post['title']}]({post['link']})\n"
    
    social_media_sentiment = ""
    for i, post in enumerate(social_media[:5]):
        social_media_sentiment += f"{round(post['score'], 2)} - {post['sentiment']}\n"
    social_media_sentiment += f"**Average:** {round(social_media_avg, 2)}"

    embed.add_field("Social Media Posts", social_media_samples, True)
    embed.add_field("Sentiment", social_media_sentiment, True)


def sentiment(inter: Interaction, type: str, query: str, interval: int = 7) -> None:
    # Parse the arguments
    if interval < 1:
        interval = 1
    elif interval > 30:
        interval = 30
    
    start = (datetime.datetime.now() - datetime.timedelta(days=interval)).strftime("%Y-%m-%d")

    # Get the data
    ticker = get_ticker(query)
    headlines = get_headlines(query, ticker, start)
    social_media = get_social_media(ticker, start)
    headlines = sorted(headlines, key=lambda x: abs(x['score']))
    social_media = sorted(social_media, key=lambda x: abs(x['score']))

    # Create the embed
    embed = Embedding(f"Sentiment Analysis for \'{query}\' ({get_ticker(query)})",
                       f"Found {len(headlines)} headlines and {len(social_media)} social media posts." + 
                       (" Higher sentiment scores indicate more positive sentiment." if type == "analyze" else ""),
                         color=0x00FF00)

    # Add the appropriate fields
    if type == "collect":
        collect_helper(embed, headlines, social_media)
    else:
        analyze_helper(embed, headlines, social_media)

    # Add a warning if the sample size is small
    if (len(headlines) + len(social_media)) < 25:
        embed.add_field(":warning:  Warning", "*The sample size for this query is small. Consider using a more popular company or a larger timespan.*")
        embed.set_color(0xFF8000)

    # Add the footer and send the response
    add_footer(inter.timestamp, embed)
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


        