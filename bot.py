import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from config import TOKEN, OWNER_ID, LOG_LEVEL
from admin.owner_admin_module import owner_menu, handle_owner_menu
from modules.moderation_module import moderation_module
from modules.welcome_module import welcome_module
from utils.helpers import is_owner
from utils.translation import translate, get_available_languages
from utils.persistence import get_user_language, set_user_language
from data.persistent_storage import init_db

# Konfiguriere das Logging
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    user_lang = get_user_language(user.id)
    if is_owner(user.id, OWNER_ID):
        keyboard = [
            [InlineKeyboardButton(translate('change_language', user_lang), callback_data='change_language')],
            [InlineKeyboardButton(translate('select_group', user_lang), callback_data='select_group')],
            [InlineKeyboardButton(translate('owner_menu', user_lang), callback_data='owner_menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # Überprüfe, ob update.message vorhanden ist, andernfalls verwende update.callback_query.message
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
    keyboard.append([InlineKeyboardButton(translate('back', user_lang), callback_data='back')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=translate('choose_language', user_lang), reply_markup=reply_markup)

def set_language(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    user_lang = query.data.split('_')[-1]
    set_user_language(query.from_user.id, user_lang)
    
    # Erstelle das Hauptmenü nach der Sprachwahl neu
    start(update, context)
    
    # Füge die Bestätigungsmeldung hinzu
    keyboard = [[InlineKeyboardButton(translate('back_to_main_menu', user_lang), callback_data='back_to_main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.message.reply_text(translate('language_set', user_lang), reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    user_lang = get_user_language(query.from_user.id)
    if query.data == 'change_language':
        change_language(update, context)
    elif query.data == 'select_group':
        query.edit_message_text(text=translate('select_group_not_implemented', user_lang))
    elif query.data == 'owner_menu':
        owner_menu(update, context)
    elif query.data == 'back':
        start(update, context)
    elif query.data == 'back_to_main_menu':
        start(update, context)
    elif query.data.startswith('set_language_'):
        set_language(update, context)

def main() -> None:
    # Initialisiere die Datenbank
    init_db()
    
    # Bot initialisieren und starten
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
