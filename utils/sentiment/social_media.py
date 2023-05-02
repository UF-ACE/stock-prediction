import html
import snscrape.modules.twitter as sntwitter
import requests
import time
import datetime


def get_tweets(ticker: str, start: str, num: int = 100) -> list[str]:
    tweets = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{ticker} since:{start} lang:en min_faves:50').get_items()):
        if i >= num:
            break
        tweets.append(html.unescape(tweet.rawContent))
    return tweets


def get_reddit_comments(ticker: str, start: str, num: int = 100) -> list[dict]:
    # Convert the start date to epoch time
    epoch = int(time.mktime(datetime.datetime.strptime(start, "%Y-%m-%d").timetuple()))

    # Send the request to the Pushshift API for comments
    comments_url = f'https://api.pushshift.io/reddit/search/comment/?q={ticker}&after={epoch}&sort_type=score&size={num}'
    response = requests.get(comments_url)
    data = response.json()

    # Extract the comments and return
    return [{"title": html.unescape(comment['body']), "link": "https://reddit.com" + comment['permalink']} for comment in data['data']]


def get_reddit_posts(ticker: str, start: str, num: int = 100) -> list[dict]:
    # Convert the start date to epoch time
    epoch = int(time.mktime(datetime.datetime.strptime(start, "%Y-%m-%d").timetuple()))

    # Send the request to the Reddit API
    posts_url = f'https://www.reddit.com/search.json?q={ticker}+title:{ticker}&after={epoch}&limit={num}&sort=score&restrict_sr=1'
    response = requests.get(posts_url, headers={'User-agent' :'Mozilla/5.0 (Macintosh; PPC Mac OS X 10_8_7 rv:5.0; en-US) AppleWebKit/533.31.5 (KHTML, like Gecko) Version/4.0 Safari/533.31.5'})
    data = (response.json())['data']['children']

    # Extract the posts and return
    return [{"title": html.unescape(post['data']['title']), "link": html.unescape(post['data']['url'])} for post in data if 
            (post['data']['title'].lower().find("free trial") == -1 and
              post['data']['title'].lower().find("webull") == -1 and
                post['data']['title'].lower().find("refer") == -1
            )]


def get_social_media(ticker: str, start: str) -> list[dict]:
    return get_reddit_comments(ticker, start) + get_reddit_posts(ticker, start) # + get_tweets(ticker, start)