from telegram import Update
from telegram.ext import CallbackContext
from utils.translation import translate

def welcome_module(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(translate('welcome_module_active', update.effective_user.language_code))
    # Hier kannst du die Logik für das Begrüßungsmodul hinzufügen
