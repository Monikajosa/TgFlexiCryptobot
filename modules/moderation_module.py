from telegram import Update
from telegram.ext import CallbackContext

def moderation_module(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Moderationsmodul ist aktiv.')
    # Hier kannst du die Logik für das Moderationsmodul hinzufügen
