import requests
import os
import finnhub
import datetime
from GoogleNews import GoogleNews
import yfinance as yf
from utils import get_ticker

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
FINNHUB_API_KEY = os.environ.get('FINNHUB_API_KEY')
news_api_endpoint = "https://newsapi.org/v2/everything/"
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)


# Given a company name, start, end dates -> return a list of news headlines from News API
def get_news_api(query: str, start: str, end: str) -> list[str]:
    # Search for the company name and its ticker
    headlines = []
    for query in [query, get_ticker(query)]:
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


# Given a company name, start, end dates -> return a list of news headlines from Google News API
def get_google_news(query: str, start: str, end: str) -> list[str]:
    '''TODO: Make this work on Lambda environment -> currently causes timeout'''
    headlines = []
    # Create the GoogleNews object
    googlenews = GoogleNews(start=start, end=end, lang='en', region='US')

    # Search for the common name
    googlenews.search(query)
    headlines += [x['title'] for x in googlenews.result()]

    # Clear the object and search for the ticker
    googlenews.clear()
    googlenews.search(get_ticker(query))
    headlines += [googlenews.result()[x]['title'] for x in range(len(googlenews.result()))]
    
    return headlines
    

# Given a ticker, start, end dates -> return a list of news headlines from Finnhub API
def get_finnhub(query: str, start: str, end: str) -> list[str]:
    # Submit the request to the Finnhub API
    headlines = finnhub_client.company_news(get_ticker(query), _from=start, to=end)

    # Extract headlines and return
    headlines = [article['headline'] for article in headlines]
    return headlines


# Given a ticker, start, end dates -> return a list of news headlines from Yahoo Finance API
def get_yahoo(query: str, start: str, end: str) -> list[str]:
    yf_obj = yf.Ticker(get_ticker(query))
    return [x['title'] for x in yf_obj.news]


def get_headlines(query: str, start: str = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d"), end: str = datetime.datetime.now().strftime("%Y-%m-%d")) -> list[str]:
    headlines = set()
    headlines.update(get_finnhub(query, start, end))
    headlines.update(get_news_api(query, start, end))
    #headlines.update(get_google_news(query, datetime.datetime.strptime(start, "%Y-%m-%d").strftime("%m-%d-%Y"), datetime.datetime.strptime(end, "%Y-%m-%d").strftime("%m-%d-%Y")))
    headlines.update(get_yahoo(query, start, end))
    return list(headlines)