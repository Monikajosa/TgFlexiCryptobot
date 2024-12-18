import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from config import TOKEN, OWNER_ID, LOG_LEVEL
from admin.owner_admin_module import owner_menu, handle_owner_menu
from modules.moderation_module import moderation_module
from modules.welcome_module import welcome_module
from utils.helpers import is_owner
from utils.translation import translate
from data.persistent_storage import init_db

# Konfiguriere das Logging
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    user_lang = user.language_code
    if is_owner(user.id, OWNER_ID):
        keyboard = [
            [InlineKeyboardButton(translate('change_language', user_lang), callback_data='change_language')],
            [InlineKeyboardButton(translate('select_group', user_lang), callback_data='select_group')],
            [InlineKeyboardButton(translate('owner_menu', user_lang), callback_data='owner_menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text(translate('welcome', user_lang), reply_markup=reply_markup)
    else:
        update.message.reply_text(translate('welcome', user_lang))

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    user_lang = query.from_user.language_code
    if query.data == 'change_language':
        query.edit_message_text(text=translate('change_language_not_implemented', user_lang))
    elif query.data == 'select_group':
        query.edit_message_text(text=translate('select_group_not_implemented', user_lang))
    elif query.data == 'owner_menu':
        owner_menu(update, context)
    elif query.data == 'back':
        start(update, context)

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
