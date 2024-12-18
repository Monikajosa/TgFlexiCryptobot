import json
import os

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'ad_settings.json')

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as file:
            return json.load(file)
    return {}

def save_settings(settings):
    with open(SETTINGS_FILE, 'w', encoding='utf-8') as file:
        json.dump(settings, file, ensure_ascii=False, indent=4)

def is_ad_enabled(chat_id):
    settings = load_settings()
    return settings.get(str(chat_id), {}).get('ad_enabled', False)

def set_ad_enabled(chat_id, enabled):
    settings = load_settings()
    if str(chat_id) not in settings:
        settings[str(chat_id)] = {}
    settings[str(chat_id)]['ad_enabled'] = enabled
    save_settings(settings)

def get_ad_button_label(chat_id, chat_title):
    ad_status = "ON" if is_ad_enabled(chat_id) else "OFF"
    return f"{chat_title} ({ad_status})"

module_name_key = "ad_function"

def ad_function_handler(update, context):
    # Implementierung der Funktionalität
    pass
