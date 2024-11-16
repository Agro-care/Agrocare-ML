from deep_translator import GoogleTranslator


def translate_text(text, dest):
    return GoogleTranslator(source='auto', target=dest).translate(text)
