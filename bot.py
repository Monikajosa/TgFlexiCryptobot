
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OWNER_ID = os.getenv('OWNER_ID')

# Function to start the bot and show the main menu
def start(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    keyboard = [
        [InlineKeyboardButton("Sprache wählen", callback_data='change_language')],
        [InlineKeyboardButton("Gruppe wählen", callback_data='choose_group')]
    ]
    if str(user_id) == OWNER_ID:
        keyboard.append([InlineKeyboardButton("Owner Admin Menü", callback_data='admin_menu')])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Hauptmenü:', reply_markup=reply_markup)

# Callback for handling button clicks
def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == 'change_language':
        query.edit_message_text(text="Sprachauswahl: (dynamisch geladen)")
    elif query.data == 'choose_group':
        query.edit_message_text(text="Gruppenwahl: (dynamisch geladen)")
    elif query.data == 'admin_menu':
        query.edit_message_text(text="Admin Menü: (dynamisch geladen)")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CallbackQueryHandler(button))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
