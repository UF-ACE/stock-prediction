import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


def setup_vader() -> SentimentIntensityAnalyzer:
    nltk.data.path.append("/tmp")
    try:
        nltk.data.find("vader_lexicon")
    except LookupError:
        nltk.download("vader_lexicon", download_dir="/tmp")
    analyzer = SentimentIntensityAnalyzer()
    return analyzer


def analyze_sentence(text: str, analyzer: SentimentIntensityAnalyzer) -> float:
    return analyzer.polarity_scores(text)["compound"]


def analyze_data(data: list[dict]) -> None:
    analyzer = setup_vader()
    avg = 0
    for x in data:
        score = analyze_sentence(x["title"], analyzer)
        x["score"] = score
        x["sentiment"] = "positive" if score > 0 else "negative" if score < 0 else "neutral"
        avg += score

    return avg / len(data)
