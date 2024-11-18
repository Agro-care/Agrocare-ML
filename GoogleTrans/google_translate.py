from deep_translator import GoogleTranslator
import json


def translate_text(text, dest):
    return GoogleTranslator(source='auto', target=dest).translate(text)


def get_dest(json_data):
    try:
        data = json.loads(json_data)
    except json.JSONDecodeError:
        raise ValueError("Invalid JSON data.(translate)")
    
    return data.get('dest', 'en')
