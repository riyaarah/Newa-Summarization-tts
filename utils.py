import re
import pandas as pd
from collections import Counter


def clean_text(text: str) -> str:
    """
    Cleans the input text by removing unwanted characters and formatting properly.
    
    Args:
        text (str): The input text to clean.
    
    Returns:
        str: Cleaned and formatted text.
    """
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces and newlines
    return text.replace("\n", " ")


def format_timestamp(timestamp: str) -> str:
    """
    Formats a timestamp string into a more readable date format (YYYY-MM-DD).
    
    Args:
        timestamp (str): The original timestamp string (ISO format).
    
    Returns:
        str: Formatted date or "Unknown" if timestamp is missing.
    """
    return timestamp.split("T")[0] if timestamp else "Unknown"


def extract_top_keywords(text: str, top_n: int = 5) -> dict:
    """
    Extracts the top N keywords from the given text based on word frequency analysis.
    
    Args:
        text (str): The input text for keyword extraction.
        top_n (int): The number of top keywords to return (default is 5).
    
    Returns:
        dict: A dictionary containing the most common words and their frequency.
    """
    words = re.findall(r'\b\w+\b', text.lower())  # Extract words and convert to lowercase
    word_counts = Counter(words)
    return dict(word_counts.most_common(top_n))


def format_sentiment_trends(sentiment_trends: dict) -> pd.DataFrame:
    """
    Converts sentiment trend data into a Pandas DataFrame for easier visualization.
    
    Args:
        sentiment_trends (dict): Dictionary containing sentiment data by date.
    
    Returns:
        pd.DataFrame: A sorted DataFrame with columns ['Date', 'Positive', 'Negative', 'Neutral'].
    """
    data = [
        [date, counts.get("Positive", 0), counts.get("Negative", 0), counts.get("Neutral", 0)]
        for date, counts in sentiment_trends.items()
    ]

    df = pd.DataFrame(data, columns=["Date", "Positive", "Negative", "Neutral"])
    return df.sort_values("Date")  # Ensure chronological order
