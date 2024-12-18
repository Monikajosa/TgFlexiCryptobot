from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from utils.translation import translate

def owner_menu(update: Update, context: CallbackContext) -> None:
    keyboard = [
        [InlineKeyboardButton(translate('ad_function', update.effective_user.language_code), callback_data='ad_function')],
        [InlineKeyboardButton(translate('module_management', update.effective_user.language_code), callback_data='module_management')],
        [InlineKeyboardButton(translate('bot_status', update.effective_user.language_code), callback_data='bot_status')],
        [InlineKeyboardButton(translate('back', update.effective_user.language_code), callback_data='back')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(translate('owner_menu', update.effective_user.language_code), reply_markup=reply_markup)

def handle_owner_menu(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    if query.data == 'ad_function':
        query.edit_message_text(text=translate('ad_function_not_implemented', update.effective_user.language_code))
    elif query.data == 'module_management':
        query.edit_message_text(text=translate('module_management_not_implemented', update.effective_user.language_code))
    elif query.data == 'bot_status':
        query.edit_message_text(text=translate('bot_status_not_implemented', update.effective_user.language_code))
    elif query.data == 'back':
        start(update, context)
