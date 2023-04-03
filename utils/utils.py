import requests


# Given a company name, return the corresponding ticker
def get_ticker(query: str) -> str:
    yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
    params = {"q": query, "quotes_count": 0, "country": "United States"}

    res = requests.get(url=yfinance, params=params, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})
    data = res.json()
    return data['quotes'][0]['symbol']
