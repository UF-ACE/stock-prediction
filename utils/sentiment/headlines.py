import requests
import os
import finnhub
import datetime
from GoogleNews import GoogleNews
import yfinance as yf

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
FINNHUB_API_KEY = os.environ.get('FINNHUB_API_KEY')
news_api_endpoint = "https://newsapi.org/v2/everything/"
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)


# Given a company name, start, end dates -> return a list of news headlines from News API
def get_news_api(query: str, ticker: str, start: str) -> list[str]:
    # Search for the company name and its ticker
    headlines = []
    for query in [query, ticker]:
        # Construct the request parameters
        request_params = {
            'q': query,
            'language': 'en',
            'from': start,
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
def get_google_news(query: str, ticker: str, start: str) -> list[str]:
    '''TODO: Make this work on Lambda environment -> currently causes timeout'''
    headlines = []
    # Create the GoogleNews object
    googlenews = GoogleNews(start=start, end=datetime.datetime.now().strftime("%m-%d-%Y"), lang='en', region='US')

    # Search for the common name
    googlenews.search(query)
    headlines += [x['title'] for x in googlenews.result()]

    # Clear the object and search for the ticker
    googlenews.clear()
    googlenews.search(ticker)
    headlines += [googlenews.result()[x]['title'] for x in range(len(googlenews.result()))]
    
    return headlines
    

# Given a ticker, start, end dates -> return a list of news headlines from Finnhub API
def get_finnhub(ticker: str, start: str) -> list[str]:
    # Submit the request to the Finnhub API
    headlines = finnhub_client.company_news(ticker, _from=start, to=datetime.datetime.now().strftime("%Y-%m-%d"))

    # Extract headlines and return
    headlines = [article['headline'] for article in headlines]
    return headlines


# Given a ticker, start, end dates -> return a list of news headlines from Yahoo Finance API
def get_yahoo(ticker: str, start: str) -> list[str]:
    yf_obj = yf.Ticker(ticker)
    return [x['title'] for x in yf_obj.news]


def get_headlines(query: str, ticker: str, start: str) -> list[str]:
    headlines = set()
    headlines.update(get_finnhub(ticker, start))
    headlines.update(get_news_api(query, ticker, start))
    #headlines.update(get_google_news(query, ticker, datetime.datetime.strptime(start, "%Y-%m-%d").strftime("%m-%d-%Y")))
    headlines.update(get_yahoo(ticker, start))
    return list(headlines)