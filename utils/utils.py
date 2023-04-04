import requests
from utils.discord import Embedding


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


def send_embed(webhook_url: str, embed: Embedding) -> None:
        requests.patch(webhook_url, json={"embeds": [embed.to_dict()]}).raise_for_status()