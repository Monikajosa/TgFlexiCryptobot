import json

def load_translation(language_code):
    with open(f'locales/{language_code}.json', 'r') as file:
        return json.load(file)

def translate(key, language_code='en'):
    translations = load_translation(language_code)
    return translations.get(key, key)
