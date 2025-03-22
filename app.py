import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from news_extraction import fetch_news
from comparative_analysis import comparative_sentiment_analysis
from tts_converter import text_to_speech_hindi
import seaborn as sns
# ----------------------------- Page Configuration ----------------------------- #
st.set_page_config(page_title="The News Summarization and Text-to-Speech (TTS) application ", layout="wide")

# ----------------------------- Custom Styling ----------------------------- #
st.markdown("""
    <style>
        body { font-family: 'Inter', sans-serif; background-color: #121212; color: #EEEEEE; }
        
        /* Sidebar */
        .css-1lcbmhc { background-color: #1E1E1E !important; color: white; }

        /* Header */
        .main-title { font-size: 32px; font-weight: bold; color: #00ADB5; text-align: center; margin-bottom: 15px; }
        .section-title { font-size: 22px; font-weight: bold; color: #00ADB5; margin-top: 20px; border-left: 5px solid #00ADB5; padding-left: 12px; }

        /* News Cards */
        .news-card {
            background: #1E1E1E; padding: 20px; border-radius: 12px;
            margin-bottom: 15px; box-shadow: 0px 5px 12px rgba(0, 0, 0, 0.3);
            transition: transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out;
        }
        .news-card:hover {
            transform: translateY(-5px);
            box-shadow: 0px 8px 18px rgba(0, 0, 0, 0.5);
        }
        .news-title { font-size: 18px; font-weight: bold; color: #00ADB5; margin-bottom: 5px; }
        .news-summary { font-size: 15px; color: #BBBBBB; }

        /* Sentiment Colors */
        .sentiment-positive { color: #27ae60; font-weight: bold; }
        .sentiment-negative { color: #e74c3c; font-weight: bold; }
        .sentiment-neutral { color: #f1c40f; font-weight: bold; }

        /* Buttons */
        .stButton>button {
            font-size: 16px; font-weight: bold; padding: 12px 18px;
            background-color: #00ADB5 !important; color: white !important;
            border: none; border-radius: 6px; cursor: pointer;
            transition: all 0.3s ease-in-out;
        }
        .stButton>button:hover {
            background-color: #007a99 !important; transform: translateY(-3px);
            box-shadow: 0px 5px 15px rgba(0, 0, 0, 0.5);
        }

        /* Audio Player */
        audio { width: 100%; margin-top: 10px; }

    </style>
""", unsafe_allow_html=True)

# ----------------------------- Sidebar: Search News ----------------------------- #
with st.sidebar:
    st.image("https://www.streamlit.io/images/brand/streamlit-mark-color.png", width=150)
    st.markdown("## 🔍 SEARCH NEWS HERE")
    company = st.text_input("Enter a Company Name", placeholder="E.g., Tesla, Google, Amazon")

# ----------------------------- Fetch & Display News ----------------------------- #
if company:
    try:
        news_list = fetch_news(company)

        if not news_list:
            st.warning(f"No news found for '{company}'. Try another keyword.")
        else:
            sentiment_analysis = comparative_sentiment_analysis(news_list)

            # -------------------- JSON Structure Layout -------------------- #
            final_data = {
                "Company": company,
                "Articles": [
                    {
                        "Title": article["title"],
                        "Summary": article["summary"],
                        "Sentiment": article["sentiment"],
                        "Topics": article.get("topics", []),
                        "URL": article["url"],
                        "AudioFile": f"speech_{i}.mp3"
                    }
                    for i, article in enumerate(news_list, 1)
                ],
                "Comparative Sentiment Score": {
                    "Sentiment Distribution": sentiment_analysis["Sentiment Distribution"],
                    "Coverage Differences": sentiment_analysis["Coverage Differences"],
                    "Topic Overlap": {
                        "Common Topics": list(set.intersection(*[set(article.get("topics", [])) for article in news_list])) if len(news_list) > 1 else [],
                        "Unique Topics in Article 1": list(set(news_list[0].get("topics", [])) - set(news_list[1].get("topics", []))) if len(news_list) > 1 else [],
                        "Unique Topics in Article 2": list(set(news_list[1].get("topics", [])) - set(news_list[0].get("topics", []))) if len(news_list) > 1 else []
                    }
                },
                "Final Sentiment Analysis": f"{company}'s latest news coverage is mostly {sentiment_analysis['Majority Sentiment'].lower()}."
            }

            # -------------------- UI Rendering -------------------- #
            st.markdown(f"<h1 class='main-title'>{final_data['Company']} News Analysis</h1>", unsafe_allow_html=True)
            
            # Display Articles in Two-Column Layout
            cols = st.columns(2)
            for i, article in enumerate(final_data["Articles"]):
                # Generate the TTS file
                audio_path = f"speech_{i}.mp3"
                text_to_speech_hindi(article["Summary"], audio_path)  # Generate Hindi audio

                with cols[i % 2]:  # Alternate between two columns
                    sentiment_color = "sentiment-positive" if article["Sentiment"] == "Positive" else "sentiment-negative" if article["Sentiment"] == "Negative" else "sentiment-neutral"
                    
                    st.markdown(
                        f"""
                        <div class="news-card">
                            <h3>📰 <a href="{article['URL']}" target="_blank">{article['Title']}</a></h3>
                            <p><b>Summary:</b> {article['Summary']}</p>
                            <p><b>Sentiment:</b> <span class="{sentiment_color}">{article['Sentiment']}</span></p>
                            <p><b>Topics:</b> {', '.join(article['Topics']) if article['Topics'] else 'No topics identified'}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    

                    # ✅ Inline Play Button for Audio
                    st.audio(audio_path, format="audio/mp3")

            # -------------------- Sentiment Distribution Pie Chart (3D Effect) -------------------- #
            st.markdown("<h2 style='color:#1a1a2e;'>📊 Sentiment Distribution</h2>", unsafe_allow_html=True)
            sentiment_labels = list(final_data["Comparative Sentiment Score"]["Sentiment Distribution"].keys())
            sentiment_values = list(final_data["Comparative Sentiment Score"]["Sentiment Distribution"].values())

            fig, ax = plt.subplots(figsize=(6, 6))
            values=list(sentiment_analysis['Sentiment Distribution'].keys())
            labels=list(sentiment_analysis["Sentiment Distribution"].values())
            explode = [0.1]*len(values)  # Add 3D effect
            ax.pie(
                sentiment_values, labels=sentiment_labels, autopct="%1.1f%%",
                colors=["#1abc9c", "#e74c3c", "#f39c12"], startangle=140,
                shadow=True, explode=explode, wedgeprops={'edgecolor': 'black'}
            )
            ax.set_title("Sentiment Breakdown (3D)")
            st.pyplot(fig)

            # -------------------- Coverage Differences -------------------- #
            st.markdown("<h2 style='color:#1a1a2e;'>⚖ Coverage Differences</h2>", unsafe_allow_html=True)
            for diff in final_data["Comparative Sentiment Score"]["Coverage Differences"]:
                st.write(f"- **{diff['Comparison']}**")
                st.write(f"  - _Impact:_ {diff['Impact']}")

            # -------------------- Topic Overlap -------------------- #
            st.markdown("<h2 style='color:#1a1a2e;'>🏷 Topic Overlap</h2>", unsafe_allow_html=True)
            st.write(f"**Common Topics:** {', '.join(final_data['Comparative Sentiment Score']['Topic Overlap']['Common Topics'])}")
            st.write(f"**Unique Topics in Article 1:** {', '.join(final_data['Comparative Sentiment Score']['Topic Overlap']['Unique Topics in Article 1'])}")
            st.write(f"**Unique Topics in Article 2:** {', '.join(final_data['Comparative Sentiment Score']['Topic Overlap']['Unique Topics in Article 2'])}")

            # -------------------- Final Summary -------------------- #
            st.markdown(f"<h2 style='color:#28a745;'>📌 Final Sentiment Analysis</h2>", unsafe_allow_html=True)
            st.success(final_data["Final Sentiment Analysis"])

    except Exception as e:
        st.error(f"An error occurred: {e}")
















