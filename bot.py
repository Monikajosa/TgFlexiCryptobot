import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from config import TOKEN, OWNER_ID, LOG_LEVEL
from admin.owner_admin_module import owner_menu, handle_owner_menu
from modules.moderation_module import moderation_module
from modules.welcome_module import welcome_module
from utils.helpers import is_owner
from utils.translation import translate, get_available_languages
from data.persistent_storage import init_db

# Konfiguriere das Logging
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    user_lang = context.user_data.get('language', user.language_code)
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
    user_lang = context.user_data.get('language', update.effective_user.language_code)
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
    # Speichere die ausgewählte Sprache für den Benutzer
    context.user_data['language'] = user_lang
    # Erstelle das Hauptmenü nach der Sprachwahl neu
    start(update, context)
    # Füge die Bestätigungsmeldung hinzu
    query.message.reply_text(translate('language_set', user_lang))

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    user_lang = context.user_data.get('language', query.from_user.language_code)
    if query.data == 'change_language':
        change_language(update, context)
    elif query.data == 'select_group':
        query.edit_message_text(text=translate('select_group_not_implemented', user_lang))
    elif query.data == 'owner_menu':
        owner_menu(update, context)
    elif query.data == 'back':
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
