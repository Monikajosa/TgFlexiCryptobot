from telegram import Update
from telegram.ext import CallbackContext

def welcome_module(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Willkommen im Begrüßungsmodul!')
    # Hier kannst du die Logik für das Begrüßungsmodul hinzufügen
