import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from config import TOKEN, OWNER_ID, LOG_LEVEL
from admin.owner_admin_module import owner_menu, handle_owner_menu
from modules.moderation_module import moderation_module
from modules.welcome_module import welcome_module
from utils.helpers import is_owner
from data.persistent_storage import init_db

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    if is_owner(user.id, OWNER_ID):
        keyboard = [
            [InlineKeyboardButton("Sprache ändern", callback_data='change_language')],
            [InlineKeyboardButton("Gruppe wählen", callback_data='select_group')],
            [InlineKeyboardButton("Owner Admin Menü", callback_data='owner_menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        update.message.reply_text('Willkommen! Bitte wähle eine Option:', reply_markup=reply_markup)
    else:
        update.message.reply_text('Willkommen! Du hast keine Berechtigung, um auf das Admin-Menü zuzugreifen.')

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'change_language':
        query.edit_message_text(text="Sprache ändern ist derzeit nicht implementiert.")
    elif query.data == 'select_group':
        query.edit_message_text(text="Gruppe wählen ist derzeit nicht implementiert.")
    elif query.data == 'owner_menu':
        owner_menu(update, context)

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
