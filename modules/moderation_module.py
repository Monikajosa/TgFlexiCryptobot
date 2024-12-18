from telegram import Update
from telegram.ext import CallbackContext
from utils.translation import translate

module_name_key = "moderation_module"

def moderation_module_handler(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(translate('moderation_module_active', update.effective_user.language_code))
    # Hier kannst du die Logik für das Moderationsmodul hinzufügen
