import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# Ensure VADER is available
nltk.download("vader_lexicon")

# Initialize Sentiment Analyzer once to avoid redundant reloading
SIA = SentimentIntensityAnalyzer()


def analyze_sentiment(text: str) -> str:
    """
    Analyze the sentiment of a given text using VADER.

    Args:
        text (str): The text to analyze.

    Returns:
        str: "Positive", "Negative", or "Neutral" based on sentiment score.
    """
    if not text:  # If empty text, return "Neutral"
        return "Neutral"

    score = SIA.polarity_scores(text)["compound"]

    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    return "Neutral"
