News Summarization and TTS Application

Introduction
The News Summarization and Text-to-Speech (TTS) application is designed to extract, summarize, analyze sentiment, and convert news articles into speech. This project integrates web scraping, NLP-based text summarization, sentiment analysis, and text-to-speech conversion into a single web-based tool, allowing users to efficiently consume news content in multiple formats.

Features
    • News Extraction: Fetches articles using web scraping techniques.
    • Summarization: Generates concise summaries of lengthy news articles.
    • Sentiment Analysis: Determines the sentiment (positive, negative, or neutral) of summarized content.
    • Text-to-Speech Conversion: Converts text into speech, supporting Hindi and English.
    • User-Friendly Interface: A web-based UI built using Streamlit.
    • API Integration: Backend API for summarization, sentiment analysis, and text-to-speech functionalities.
    
Installation and Setup

Prerequisites
Ensure you have the following installed on your system:
    • Python 3.8 or later
    • Git
    • Virtual environment (optional but recommended)
    
Steps to Set Up the Project
    1. Clone the Repository
git clone https://huggingface.co/spaces/riyaarahim/news-summarization-tts
cd news-summarization-app
    2. Create and Activate a Virtual Environment
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
    3. Install Dependencies
pip install -r requirements.txt
    4. Run the Backend API
python api.py
    5. Run the Frontend Application
streamlit run app.py
    6. Deploying on Hugging Face Spaces
        ○ Ensure all dependencies are listed in requirements.txt.
        ○ Push the repository to Hugging Face.
        ○ Set app.py as the entry point.
Dependencies
The following key libraries and frameworks are used in this project:
    • Flask: For backend API development.
    • Streamlit: For building an interactive web application.
    • Newspaper3k: For extracting news content from websites.
    • Hugging Face Transformers: For NLP-based text summarization and sentiment analysis.
    • VADER (NLTK): A rule-based sentiment analysis tool.
    • gTTS: A Python library for text-to-speech conversion.
Install all dependencies using:
pip install -r requirements.txt

API Endpoints
    1. Summarization API
        ○ Endpoint: /summarize
        ○ Method: POST
        ○ Input: 
{ "text": "<news content>" }
        ○ Output: 
{ "summary": "<shortened text>" }
    2. Sentiment Analysis API
        ○ Endpoint: /sentiment
        ○ Method: POST
        ○ Input: 
{ "text": "<summarized text>" }
        ○ Output: 
{ "sentiment": "Positive/Negative/Neutral", "score": 0.85 }
    3. Text-to-Speech API
        ○ Endpoint: /tts
        ○ Method: POST
        ○ Input: 
{ "text": "<summarized text>", "language": "hi" }
        ○ Output: 
{ "audio_url": "<link to generated audio file>" }
    
Testing the API with Postman
    1. Open Postman and create a new request.
    2. Select POST and enter the endpoint URL.
    3. In the Body section, select raw -> JSON.
    4. Provide the required input JSON.
    5. Click Send and verify the response.
    
Assumptions & Limitations
Assumptions
    • Input news articles follow a structured format suitable for NLP processing.
    • A stable internet connection is required to fetch external models.
    • Summarization is optimized for longer texts.
Limitations
    • The accuracy of summarization and sentiment analysis depends on the models used.
    • The TTS feature currently supports only Hindi and English.
    • Response times may vary based on text length and model complexity.
    • Some websites may block web scraping, limiting article extraction.
Future Enhancements
    • Support for more languages in TTS.
    • Improved accuracy in summarization and sentiment analysis.
    • Real-time news updates and categorization.
    • Enhanced UI with additional interactive features.
    
