import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download('vader_lexicon')
analyzer = SentimentIntensityAnalyzer()


def analyze_sentence(text: str) -> float:
    return analyzer.polarity_scores(text)["compound"]


def analyze_data(data: list[dict]) -> None:
    avg = 0
    for x in data:
        score = analyze_sentence(x["title"])
        x["score"] = score
        x["sentiment"] = "positive" if score > 0 else "negative" if score < 0 else "neutral"
        avg += score

    return avg / len(data)
