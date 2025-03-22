import re
from collections import Counter
from itertools import combinations
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import os

# Ensure necessary NLTK downloads
nltk.download("punkt")
nltk.download("stopwords")

# Load spaCy model (fixed)
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    print(" spaCy model not found! Downloading now...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
    print(" Model downloaded! Loading now...")
    nlp = spacy.load("en_core_web_sm")

# (Rest of your script remains unchanged)


def extract_topics(text, num_topics=3):
    """Extracts meaningful topics using TF-IDF and Named Entity Recognition (NER)"""
    if not text:
        return ["No topics identified"]  # Fallback for empty summaries

    # Named Entity Recognition (NER) for Companies, Tech, and Places
    doc = nlp(text)
    named_entities = [ent.text for ent in doc.ents if ent.label_ in ["ORG", "GPE", "PRODUCT"]]

    # TF-IDF for Keyword Extraction
    words = word_tokenize(text.lower())  # Tokenize
    words = [word for word in words if word.isalpha()]  # Remove punctuation
    words = [word for word in words if word not in stopwords.words("english")]  # Remove stopwords
    
    vectorizer = TfidfVectorizer(max_features=10)
    tfidf_matrix = vectorizer.fit_transform([" ".join(words)])
    feature_names = vectorizer.get_feature_names_out()
    
    # 3️⃣ Combine Results (NER + TF-IDF)
    topics = list(set(named_entities + list(feature_names[:num_topics])))  

    return topics if topics else ["No topics identified"]  # Ensure non-empty output

def extract_keywords(text: str) -> list:
    """
    Extract common keywords from a given text while removing stop words.

    Args:
        text (str): Input text (typically a news title).

    Returns:
        list: A list of extracted keywords.
    """
    words = re.findall(r"\b\w+\b", text.lower())  # Tokenize words
    stop_words = {"the", "of", "a", "and", "to", "in", "on", "for", "with", "is", "at", "by"}
    return [word for word in words if word not in stop_words]


def comparative_sentiment_analysis(news_list: list) -> dict:
    """
    Perform comparative sentiment analysis on a list of news articles.

    Args:
        news_list (list): List of news articles (each article is a dictionary with "title" and "sentiment").

    Returns:
        dict: Dictionary containing sentiment distribution, major trends, sentiment shifts, coverage differences, 
              keyword frequency, and most extreme sentiment articles.
    """
    if not news_list:
        return {
            "Sentiment Distribution": {},
            "Majority Sentiment": "Neutral",
            "Sentiment Shifts": [],
            "Coverage Differences": [],
            "Keyword Frequency": {},
            "Most Positive Article": "None",
            "Most Negative Article": "None",
        }

    # 🔹 Sentiment Distribution
    sentiment_counts = Counter(article["sentiment"] for article in news_list)
    majority_sentiment = max(sentiment_counts, key=sentiment_counts.get, default="Neutral")

    # 🔹 Detect Sentiment Shifts
    sentiment_shifts = [
        {
            "Change": f"Shift from {news_list[i]['sentiment']} in '{news_list[i]['title']}' "
            f"to {news_list[i + 1]['sentiment']} in '{news_list[i + 1]['title']}'."
        }
        for i in range(len(news_list) - 1)
        if news_list[i]["sentiment"] != news_list[i + 1]["sentiment"]
    ]

    # 🔹 Identify Most Positive & Negative Articles
    most_positive = next((article["title"] for article in news_list if article["sentiment"] == "Positive"), "None")
    most_negative = next((article["title"] for article in news_list if article["sentiment"] == "Negative"), "None")

    # 🔹 Keyword Frequency Analysis
    keyword_counter = Counter()
    for article in news_list:
        keyword_counter.update(extract_keywords(article["title"]))

    # 🔹 Coverage Differences (Comparing Article Focus)
    coverage_differences = [
        {
            "Comparison": f"Article {i} discusses \"{article1['title']}\", while Article {j} focuses on \"{article2['title']}\".",
            "Impact": f"Article {i} presents a {article1['sentiment']} view, while Article {j} takes a {article2['sentiment']} stance.",
        }
        for (i, article1), (j, article2) in combinations(enumerate(news_list, 1), 2)
    ]

    return {
        "Sentiment Distribution": dict(sentiment_counts),
        "Majority Sentiment": majority_sentiment,
        "Sentiment Shifts": sentiment_shifts,
        "Coverage Differences": coverage_differences,
        "Keyword Frequency": dict(keyword_counter.most_common(5)),  # Top 5 keywords
        "Most Positive Article": most_positive,
        "Most Negative Article": most_negative,
    }

