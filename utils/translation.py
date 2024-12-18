import os
import json

def load_translation(language_code):
    try:
        with open(f'locales/{language_code}.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        with open('locales/en.json', 'r', encoding='utf-8') as file:
            return json.load(file)

def translate(key, language_code='en'):
    translations = load_translation(language_code)
    print(f"Translating key: {key} using language: {language_code}")  # Debugging-Ausgabe
    return translations.get(key, key)

def get_available_languages():
    languages = {}
    locales_path = 'locales'
    for filename in os.listdir(locales_path):
        if filename.endswith('.json'):
            language_code = filename[:-5]  # Remove the '.json' extension
            translations = load_translation(language_code)
            language_name = translations.get('language_name', language_code)
            languages[language_code] = language_name
    return languages
