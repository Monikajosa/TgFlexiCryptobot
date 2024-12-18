from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from utils.translation import translate

def owner_menu(update: Update, context: CallbackContext) -> None:
    user_lang = update.effective_user.language_code
    keyboard = [
        [InlineKeyboardButton(translate('ad_function', user_lang), callback_data='ad_function')],
        [InlineKeyboardButton(translate('module_management', user_lang), callback_data='module_management')],
        [InlineKeyboardButton(translate('bot_status', user_lang), callback_data='bot_status')],
        [InlineKeyboardButton(translate('back', user_lang), callback_data='back')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Überprüfe, ob update.message vorhanden ist, und verwende es, andernfalls verwende update.callback_query.message
    if update.message:
        update.message.reply_text(translate('owner_menu', user_lang), reply_markup=reply_markup)
    elif update.callback_query:
        update.callback_query.message.reply_text(translate('owner_menu', user_lang), reply_markup=reply_markup)

def handle_owner_menu(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    user_lang = query.from_user.language_code
    if query.data == 'ad_function':
        query.edit_message_text(text=translate('ad_function_not_implemented', user_lang))
    elif query.data == 'module_management':
        query.edit_message_text(text=translate('module_management_not_implemented', user_lang))
    elif query.data == 'bot_status':
        query.edit_message_text(text=translate('bot_status_not_implemented', user_lang))
    elif query.data == 'back':
        from bot import start
        start(update, context)
