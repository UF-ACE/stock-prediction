import requests
import time
from discord_lambda import Embedding


# Given a company name, return the corresponding ticker
def get_ticker(query: str) -> str:
    yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
    params = {"q": query, "quotes_count": 0, "country": "United States"}

    res = requests.get(url=yfinance, params=params, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})
    data = res.json()
    try:
        return data['quotes'][0]['symbol']
    except Exception as e:
        raise Exception("Invalid company name.")


# Add the generic footer to the embed
def add_footer(timestamp: float, embed: Embedding) -> None:
    embed.set_footer(text=f"Request completed in {round(time.time() - timestamp, 2)}s", icon_url="https://uf-ace.com/static/media/logo-min.1380c5e0.png")
