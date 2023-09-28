import datetime
from utils import get_ticker, add_footer
from utils.sentiment import get_headlines, analyze_data
from discord_lambda import Embedding, CommandRegistry, Interaction, CommandArg


def collect_helper(embed: Embedding, headlines: list[dict]) -> None:
    # Add sample headlines
    headlines_samples = ""
    for i, headline in enumerate(headlines[:5]):
        headline['title'].replace("\n", " ")
        headlines_samples += f"{i+1}. [{headline['title']}]({headline['link']})\n"
    embed.add_field("News Headlines", headlines_samples, False)


def analyze_helper(embed: Embedding, headlines: list[dict]) -> None:
    # Run the analysis
    headlines_avg = analyze_data(headlines)

    # Sort the data
    headlines = sorted(headlines, key=lambda x: abs(x['score']), reverse=True)

    # Add headline samples and results
    headlines_samples = ""
    for i, headline in enumerate(headlines[:3]):
        headline['title'] = headline['title'].replace("\n", " ")
        headlines_samples += f"{i+1}. [{headline['title']}]({headline['link']})\n"

    headlines_sentiment = ""
    for i, headline in enumerate(headlines[:3]):
        headlines_sentiment += f"{i+1}. {round(headline['score'], 2)} - {headline['sentiment']}\n"
    headlines_sentiment += f"**Average:** {round(headlines_avg, 2)}"

    embed.add_field("News Headlines", headlines_samples, True)
    embed.add_field("Sentiment", headlines_sentiment, True)
    embed.add_field("", "", False)


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

    # Create the embed
    embed = Embedding(f"Sentiment Analysis for \'{query}\' ({get_ticker(query)})",
                       f"Found {len(headlines)} headlines." + 
                       (" Higher sentiment scores indicate more positive sentiment." if type == "analyze" else ""),
                         color=0x00FF00)

    # Add the appropriate fields
    if type == "collect":
        collect_helper(embed, headlines)
    else:
        analyze_helper(embed, headlines)

    # Add a warning if the sample size is small
    if (len(headlines)) < 25:
        embed.add_field(":warning:  Warning", "*The sample size for this query is small. Consider using a more popular company or a larger timespan.*", False)
        embed.set_color(0xFF8000)

    # TODO: Add option to download the data as a CSV file

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