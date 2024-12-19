import json
import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from config import OWNER_ID  # Importieren von OWNER_ID aus config.py
from admin.group_manager import get_groups  # Importieren von get_groups

SETTINGS_FILE = os.path.join(os.path.dirname(__file__), 'ad_settings.json')
module_name_key = "ad_function"

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

def ad_function_handler(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        update.callback_query.message.reply_text("You are not authorized to perform this action.")
        return

    groups = get_groups()
    keyboard = []

    for chat_id, chat_title in groups.items():
        current_status = is_ad_enabled(chat_id)
        status_label = "ON" if current_status else "OFF"
        keyboard.append([InlineKeyboardButton(f"{chat_title} ({status_label})", callback_data=f"toggle_ad_{chat_id}")])

    # Füge den Zurück-Button hinzu
    keyboard.append([InlineKeyboardButton("Zurück", callback_data='back_to_owner_menu')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text("Configure AD settings for each group/channel:", reply_markup=reply_markup)

def toggle_ad(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    chat_id = int(query.data.split('_')[-1])
    current_status = is_ad_enabled(chat_id)
    set_ad_enabled(chat_id, not current_status)

    groups = get_groups()
    keyboard = []

    for chat_id, chat_title in groups.items():
        current_status = is_ad_enabled(chat_id)
        status_label = "ON" if current_status else "OFF"
        keyboard.append([InlineKeyboardButton(f"{chat_title} ({status_label})", callback_data=f"toggle_ad_{chat_id}")])

    # Füge den Zurück-Button hinzu
    keyboard.append([InlineKeyboardButton("Zurück", callback_data='back_to_owner_menu')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Configure AD settings for each group/channel:", reply_markup=reply_markup)
