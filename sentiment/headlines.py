import requests
from dotenv import load_dotenv, find_dotenv
import os
import finnhub

load_dotenv(find_dotenv())
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
FINNHUB_API_KEY = os.getenv('FINNHUB_API_KEY')
news_api_endpoint = "https://newsapi.org/v2/everything/"
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)

# Given a company name, return the corresponding ticker
def getTicker(company_name):
    yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
    params = {"q": company_name, "quotes_count": 1, "country": "United States"}

    res = requests.get(url=yfinance, params=params, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'})
    data = res.json()

    company_code = data['quotes'][0]['symbol']
    return company_code


# Given a company name, start, end dates -> return a list of news headlines from News API
def retrieve_news_api(name: str, start: str, end: str) -> list[str]:
    # Search for the company name and its ticker
    headlines = []
    for query in [name, getTicker(name)]:
        # Construct the request parameters
        request_params = {
            'q': query,
            'language': 'en',
            'from': start,
            'to': end,
            'searchIn': 'title',
            'apiKey': NEWS_API_KEY,
            'sortBy': 'relevancy',
            'pageSize': 50
        }

        # Submit the request to the News API
        response = requests.get(news_api_endpoint, params=request_params)
        response.raise_for_status()
        data = response.json()

        # Extract the news headlines from the response
        headlines += [article['title'] for article in data['articles']]

    return headlines


# Given a ticker, start, end dates -> return a list of news headlines from Finnhub API
def retrieve_finnhub(ticker: str, start: str, end: str) -> list[str]:
    # Submit the request to the Finnhub API
    headlines = finnhub_client.company_news(ticker, _from=start, to=end)

    # Extract headlines and return
    headlines = [article['headline'] for article in headlines]
    return headlines


def retrieve_headlines(name: str, start: str, end: str) -> list[str]:
    headlines = set()
    headlines.update(retrieve_news_api(name, start, end))
    headlines.update(retrieve_finnhub(getTicker(name), start, end))
    return list(headlines)