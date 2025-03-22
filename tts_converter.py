from gtts import gTTS
from deep_translator import GoogleTranslator


def text_to_speech_hindi(text: str, filename: str = "output.mp3") -> None:
    """
    Converts English text to Hindi speech and saves it as an audio file.
    
    Args:
        text (str): The text to convert to speech.
        filename (str): The output filename for the generated speech (default is "output.mp3").
    
    Returns:
        None
    """
    if not text:
        print("⚠ No text provided for TTS conversion.")
        return

    try:
        # 🔹 Translate English text to Hindi
        translated_text = GoogleTranslator(source="auto", target="hi").translate(text)

        # 🔹 Generate Hindi speech
        tts = gTTS(text=translated_text, lang="hi")

        # 🔹 Save the file
        tts.save(filename)
        print(f"✅ Speech saved as {filename}")

    except Exception as e:
        print(f"❌ Error in TTS conversion: {e}")


