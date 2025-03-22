import os
from collections import Counter
from flask import Flask, request, jsonify
from news_extraction import fetch_news
from comparative_analysis import comparative_sentiment_analysis
from tts_converter import text_to_speech_hindi

app = Flask(__name__)


@app.route("/fetch_news", methods=["GET"])
def get_news():
    """
    Endpoint to fetch news articles related to a given company.
    """
    company = request.args.get("company")
    if not company:
        return jsonify({"error": "Company name is required"}), 400

    news_list = fetch_news(company)
    if not news_list:
        return jsonify({"error": "No news found for this company"}), 404

    return jsonify(news_list)


@app.route("/analyze", methods=["GET"])
def analyze_sentiment():
    """
    Endpoint to analyze sentiment and extract insights from news articles.
    """
    company = request.args.get("company")
    if not company:
        return jsonify({"error": "Company name is required"}), 400

    # Fetch news articles
    news_list = fetch_news(company)
    if not news_list:
        return jsonify({"error": "No news found for this company"}), 404

    # Perform comparative sentiment analysis
    sentiment_data = comparative_sentiment_analysis(news_list)

    # Extract sentiment distribution
    sentiment_counts = Counter(news["sentiment"] for news in news_list)
    sentiment_distribution = {
        "Positive": sentiment_counts.get("Positive", 0),
        "Negative": sentiment_counts.get("Negative", 0),
        "Neutral": sentiment_counts.get("Neutral", 0),
    }

    # Extract date-wise sentiment trend
    sentiment_trends = {}
    for news in news_list:
        date = news["timestamp"][:10]  # Extract date part (YYYY-MM-DD)
        sentiment_trends.setdefault(date, {"Positive": 0, "Negative": 0, "Neutral": 0})
        sentiment_trends[date][news["sentiment"]] += 1

    # Extract keyword frequency
    all_keywords = [keyword for news in news_list for keyword in news.get("keywords", [])]
    keyword_counts = dict(Counter(all_keywords).most_common(10))  # Top 10 keywords

    # Prepare response
    response_data = {
        "sentiment_distribution": sentiment_distribution,
        "sentiment_trends": sentiment_trends,
        "keyword_frequency": keyword_counts,
        "news_list": news_list,  # Send back news for display
        "analysis_summary": sentiment_data,  # Additional insights from comparative analysis
    }

    return jsonify(response_data)


@app.route("/convert_text_to_speech", methods=["POST"])
def convert_tts():
    """
    Endpoint to convert text to speech (Hindi).
    """
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Text is required"}), 400

    audio_file = text_to_speech_hindi(data["text"])
    return jsonify({"audio_file": audio_file})


if __name__ == "__main__":
    app.run(debug=True, port=5000)


