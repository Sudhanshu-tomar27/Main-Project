from deep_translator import GoogleTranslator
import os
import google.generativeai as genai


def translate_text(text, target):
    if not text or not text.strip():
        return text

    target_clean = str(target).strip().lower()

    if target_clean in ["mix", "hinglish", "hindi_english_mix"]:
        api_key = os.getenv("GEMINI_API_KEY")
        if api_key:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.5-flash")
                prompt = (
                    "Translate the following text into natural, easy-to-understand "
                    "Hinglish (a modern blend of Hindi and English as commonly spoken in India). "
                    "Keep tech and professional words in English script/words while using natural Hindi structure:\n\n"
                    f"{text}"
                )
                response = model.generate_content(prompt)
                if response and response.text:
                    return response.text.strip()
            except Exception as e:
                print("Gemini Mix translation notice:", e)

        try:
            hi_text = GoogleTranslator(source="auto", target="hi").translate(text)
            return hi_text
        except Exception:
            return text

    lang_map = {
        "en": "en",
        "hi": "hi",
        "hindi": "hi",
        "english": "en"
    }
    target_code = lang_map.get(target_clean, target_clean)

    try:
        # Split text into chunks if too long for GoogleTranslator
        if len(text) > 4500:
            chunks = [text[i:i+4000] for i in range(0, len(text), 4000)]
            translated_chunks = []
            for chunk in chunks:
                translated_chunks.append(
                    GoogleTranslator(source="auto", target=target_code).translate(chunk)
                )
            return "\n".join(translated_chunks)
        else:
            return GoogleTranslator(source="auto", target=target_code).translate(text)
    except Exception as e:
        print("Translation notice:", e)
        return text