import requests
import os
import finnhub
import datetime
from GoogleNews import GoogleNews
import yfinance as yf
from newsapi import NewsApiClient

NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
FINNHUB_API_KEY = os.environ.get('FINNHUB_API_KEY')
news_api = NewsApiClient(api_key=NEWS_API_KEY)
finnhub_client = finnhub.Client(api_key=FINNHUB_API_KEY)


# Given a company name, start, end dates -> return a list of news headlines from News API
def get_news_api(query: str, ticker: str, start: str) -> list[dict]:
    # Search for the company name and its ticker
    res = []
    for query in [query, ticker]:
        # Submit the request to the News API
        data = news_api.get_everything(q=query, language='en', from_param=start, to=datetime.datetime.now().strftime("%Y-%m-%d"), sort_by='relevancy', page_size=50)

        # Extract the news headlines from the response
        res += [{"title": article['title'], "link": article['url']} for article in data['articles']]

    return res


# Given a company name, start, end dates -> return a list of news headlines from Google News API
def get_google_news(query: str, ticker: str, start: str) -> list[dict]:
    '''TODO: Make this work on Lambda environment -> currently causes timeout'''
    res = []
    # Create the GoogleNews object
    googlenews = GoogleNews(start=start, end=datetime.datetime.now().strftime("%m-%d-%Y"), lang='en', region='US')

    # Search for the common name
    googlenews.search(query)
    res += [{"title": googlenews.result()[x]['title'], "link": googlenews.result()[x]['link']} for x in range(len(googlenews.result()))]

    # Clear the object and search for the ticker
    googlenews.clear()
    googlenews.search(ticker)
    res += [{"title": googlenews.result()[x]['title'], "link": googlenews.result()[x]['link']} for x in range(len(googlenews.result()))]
    
    return res
    

# Given a ticker, start, end dates -> return a list of news headlines from Finnhub API
def get_finnhub(ticker: str, start: str) -> list[dict]:
    # Submit the request to the Finnhub API
    res = finnhub_client.company_news(ticker, _from=start, to=datetime.datetime.now().strftime("%Y-%m-%d"))

    # Extract headlines and return
    res = [{"title": article['headline'], "link": article['url']} for article in res]
    return res


# Given a ticker, start, end dates -> return a list of news headlines from Yahoo Finance API
def get_yahoo(ticker: str, start: str) -> list[str]:
    yf_obj = yf.Ticker(ticker)
    return [{"title": x['title'], "link": x['link']} for x in yf_obj.news]


def get_headlines(query: str, ticker: str, start: str) -> list[dict]:
    headlines = []
    headlines += get_finnhub(ticker, start)
    headlines += get_news_api(query, ticker, start)
    # headlines += get_google_news(query, ticker, datetime.datetime.strptime(start, "%Y-%m-%d").strftime("%m-%d-%Y"))
    headlines += get_yahoo(ticker, start)
    return headlines