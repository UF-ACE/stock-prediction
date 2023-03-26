import html
from utils import get_ticker
import snscrape.modules.twitter as sntwitter
import requests
import time
import datetime


def get_tweets(query: str, start: str, num: int = 100) -> list[str]:
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{query} since:{start} lang:en min_faves:50').get_items()):
        if i >= num:
            break
        tweets.append(html.unescape(tweet.rawContent))
    return tweets


def get_reddit_comments(query: str, start: str, num: int = 100) -> list[str]:
    # Convert the start date to epoch time
    epoch = int(time.mktime(datetime.datetime.strptime(start, "%Y-%m-%d").timetuple()))

    # Send the request to the Pushshift API for comments
    comments_url = f'https://api.pushshift.io/reddit/search/comment/?q={query}&after={epoch}&sort_type=score&size={num}'
    response = requests.get(comments_url)
    data = response.json()

    # Extract the comments and return
    return [html.unescape(comment['body']) for comment in data['data']]


def get_reddit_posts(query: str, num: int = 100) -> list[str]:
    '''TODO: Tweak this to pull relevant posts from Reddit -> pulls a lot of irrelevant posts (ads) right now'''

    # Send the request to the Reddit API
    posts_url = f'https://www.reddit.com/search.json?q={query}&t=week&limit={num}&sort=top'
    response = requests.get(posts_url, headers={'User-agent' :'Mozilla/5.0 (Macintosh; PPC Mac OS X 10_8_7 rv:5.0; en-US) AppleWebKit/533.31.5 (KHTML, like Gecko) Version/4.0 Safari/533.31.5'})
    data = (response.json())['data']['children']

    # Extract the posts and return
    return [html.unescape(post['data']['title']) for post in data]


def get_social_media(query: str, start: str = (datetime.datetime.now() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")) -> list[str]:
    query = get_ticker(query)
    return get_tweets(query, start) + get_reddit_comments(query, start) #+ get_reddit_posts(query, start)
