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
    return translations.get(key, key)
