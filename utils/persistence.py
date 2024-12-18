import json
import os

PERSISTENCE_FILE = 'user_data.json'

def load_user_data():
    if os.path.exists(PERSISTENCE_FILE):
        with open(PERSISTENCE_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def save_user_data(data):
    with open(PERSISTENCE_FILE, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def get_user_language(user_id):
    user_data = load_user_data()
    return user_data.get(str(user_id), {}).get('language', 'en')

def set_user_language(user_id, language_code):
    user_data = load_user_data()
    if str(user_id) not in user_data:
        user_data[str(user_id)] = {}
    user_data[str(user_id)]['language'] = language_code
    save_user_data(user_data)
