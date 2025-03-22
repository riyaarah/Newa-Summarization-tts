import requests
from bs4 import BeautifulSoup
import nltk

nltk.download("vader_lexicon")
from sentiment_analysis import analyze_sentiment


def fetch_news(company_name: str) -> list:
    """
    Fetch top 10 news articles related to the given company from Bing News.

    Args:
        company_name (str): The name of the company to search news for.

    Returns:
        list: A list of dictionaries containing news details (title, summary, URL, timestamp, sentiment).
    """
    search_url = f"https://www.bing.com/news/search?q={company_name}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        response.raise_for_status()  # Raise exception for HTTP errors
    except requests.RequestException as e:
        print(f"Error fetching news: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = []

    for item in soup.select(".news-card")[:10]:  # Bing News uses .news-card for articles
        title_tag = item.select_one("a.title")
        description_tag = item.select_one(".snippet")
        timestamp_tag = item.select_one(".source")

        if not title_tag:
            continue  # Skip if no valid title

        title = title_tag.text.strip()
        link = title_tag["href"]
        description = description_tag.text.strip() if description_tag else "No description available"
        timestamp = timestamp_tag.text.strip() if timestamp_tag else "No timestamp available"
        sentiment = analyze_sentiment(description)  # Perform sentiment analysis

        articles.append(
            {
                "title": title,
                "summary": description,
                "url": link,
                "timestamp": timestamp,
                "sentiment": sentiment,
            }
        )

    return articles





