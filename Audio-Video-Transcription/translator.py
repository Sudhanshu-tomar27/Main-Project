from deep_translator import GoogleTranslator


def translate_text(text, target):

    return GoogleTranslator(
        source="auto",
        target=target
    ).translate(text)