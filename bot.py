import logging
import importlib
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, Filters, MessageHandler
from config import TOKEN, OWNER_ID, LOG_LEVEL
from admin.owner_admin_module import owner_menu, get_admin_modules
from modules.moderation_module import moderation_module
from modules.welcome_module import welcome_module
from utils.helpers import is_owner
from utils.translation import translate, get_available_languages
from utils.persistence import get_user_language, set_user_language
from admin.ad_settings import is_ad_enabled, set_ad_enabled, get_ad_button_label
from admin.group_manager import add_group, remove_group, get_groups
from data.persistent_storage import init_db

# Konfiguriere das Logging
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

def is_group_registered(chat_id):
    groups = get_groups()
    return str(chat_id) in groups

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    chat = update.effective_chat

    if chat.type in ['group', 'supergroup', 'channel']:
        if not is_group_registered(chat.id):
            add_group(chat.id, chat.title)  # Gruppe/Kanal registrieren
            update.message.reply_text(translate('group_registered', get_user_language(user.id)).format(chat_title=chat.title))
    else:
        user_lang = get_user_language(user.id)
        if is_owner(user.id, OWNER_ID):
            keyboard = [
                [InlineKeyboardButton(translate('change_language', user_lang), callback_data='change_language')],
                [InlineKeyboardButton(translate('select_group', user_lang), callback_data='select_group')],
                [InlineKeyboardButton(translate('owner_menu', user_lang), callback_data='owner_menu')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            if update.message:
                update.message.reply_text(translate('welcome', user_lang), reply_markup=reply_markup)
            elif update.callback_query:
                update.callback_query.message.edit_text(translate('welcome', user_lang), reply_markup=reply_markup)
        else:
            if update.message:
                update.message.reply_text(translate('welcome', user_lang))
            elif update.callback_query:
                update.callback_query.message.edit_text(translate('welcome', user_lang))

def change_language(update: Update, context: CallbackContext) -> None:
    user_lang = get_user_language(update.effective_user.id)
    languages = get_available_languages()
    keyboard = [
        [InlineKeyboardButton(language_name, callback_data=f'set_language_{code}')]
        for code, language_name in languages.items()
    ]
    keyboard.append([InlineKeyboardButton(translate('back', user_lang), callback_data='back_to_main_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=translate('choose_language', user_lang), reply_markup=reply_markup)

def set_language(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    user_lang = query.data.split('_')[-1]
    set_user_language(query.from_user.id, user_lang)
    print(f"Set user {query.from_user.id} language to {user_lang}")  # Debugging-Ausgabe

    keyboard = [[InlineKeyboardButton(translate('back_to_main_menu', user_lang), callback_data='back_to_main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=translate('language_set', user_lang), reply_markup=reply_markup)

def ad_config(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id != OWNER_ID:
        update.message.reply_text("You are not authorized to perform this action.")
        return

    groups = get_groups()
    keyboard = []

    for chat_id, chat_title in groups.items():
        button_label = get_ad_button_label(chat_id, chat_title)
        current_status = is_ad_enabled(chat_id)
        status_label = "Enabled" if current_status else "Disabled"
        keyboard.append([InlineKeyboardButton(f"{chat_title} ({status_label})", callback_data=f"toggle_ad_{chat_id}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Configure AD settings for each group/channel:", reply_markup=reply_markup)

def toggle_ad(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    chat_id = int(query.data.split('_')[-1])
    current_status = is_ad_enabled(chat_id)
    set_ad_enabled(chat_id, not current_status)

    groups = get_groups()
    keyboard = []

    for chat_id, chat_title in groups.items():
        button_label = get_ad_button_label(chat_id, chat_title)
        current_status = is_ad_enabled(chat_id)
        status_label = "Enabled" if current_status else "Disabled"
        keyboard.append([InlineKeyboardButton(f"{chat_title} ({status_label})", callback_data=f"toggle_ad_{chat_id}")])

    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text("Configure AD settings for each group/channel:", reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    user_lang = get_user_language(query.from_user.id)
    if query.data == 'change_language':
        change_language(update, context)
    elif query.data == 'select_group':
        query.edit_message_text(translate('select_group_not_implemented', user_lang))
    elif query.data == 'owner_menu':
        owner_menu(update, context)
    elif query.data == 'back':
        start(update, context)
    elif query.data == 'back_to_main_menu':
        start(update, context)
    elif query.data.startswith('set_language_'):
        set_language(update, context)
    elif query.data.startswith('toggle_ad_'):
        toggle_ad(update, context)
    else:
        module = importlib.import_module(f"admin.{query.data}")
        if hasattr(module, f"{query.data}_handler"):
            getattr(module, f"{query.data}_handler")(update, context)

def main() -> None:
    init_db()
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Handler für den /start Befehl
    dispatcher.add_handler(CommandHandler("start", start))

    # Beispiel für einen spezifischen Befehl in einem Modul
    dispatcher.add_handler(CommandHandler("specific_command", specific_command, Filters.chat_type.groups))

    # CallbackQueryHandler für Buttons
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Filtern von Nachrichten, die keine Befehle sind, um keine Antwort zu senden
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), lambda update, context: None))

    updater.start_polling()
    updater.idle()

def specific_command(update: Update, context: CallbackContext) -> None:
    # Beispiel für einen spezifischen Befehl in einem Modul
    update.message.reply_text("Dies ist ein spezifischer Befehl, der in Gruppen/Kanälen funktioniert.")

if __name__ == '__main__':
    main()
