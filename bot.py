import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, Filters, MessageHandler
from config import TOKEN, OWNER_ID, LOG_LEVEL
from admin.owner_admin_module import owner_menu
from utils.helpers import is_owner
from utils.translation import translate, get_available_languages
from utils.persistence import get_user_language, set_user_language
from admin.group_manager import add_group, remove_group, get_groups
from data.persistent_storage import init_db
from zentrale_module import MODULES  # Importiere die zentrale Module-Liste

logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

def is_group_registered(chat_id):
    groups = get_groups()
    return str(chat_id) in groups

def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    chat = update.effective_chat

    if chat.type in ['group', 'supergroup', 'channel']:
        if not is_group_registered(chat.id):
            add_group(chat.id, chat.title)
            update.message.reply_text(translate('group_registered', get_user_language(user.id)).format(chat_title=chat.title))
    else:
        user_lang = get_user_language(user.id)
        if is_owner(user.id, OWNER_ID):
            keyboard = [
                [InlineKeyboardButton(translate('change_language', user_lang), callback_data='change_language')],
                [InlineKeyboardButton(translate('select_group', user_lang), callback_data='select_group')],
                [InlineKeyboardButton(translate('owner_menu', user_lang), callback_data='owner_menu')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

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
    user_lang = get_user_language(update.effective_user.id)
    languages = get_available_languages()
    keyboard = [
        [InlineKeyboardButton(language_name, callback_data=f'set_language_{code}')]
        for code, language_name in languages.items()
    ]
    keyboard.append([InlineKeyboardButton(translate('back', user_lang), callback_data='owner_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=translate('choose_language', user_lang), reply_markup=reply_markup)

def set_language(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    user_lang = query.data.split('_')[-1]
    set_user_language(query.from_user.id, user_lang)
    print(f"Set user {query.from_user.id} language to {user_lang}")

    keyboard = [[InlineKeyboardButton(translate('back_to_main_menu', user_lang), callback_data='owner_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=translate('language_set', user_lang), reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    user_lang = get_user_language(query.from_user.id)

    logger.debug(f"Callback data received: {query.data}")

    if query.data == 'change_language':
        change_language(update, context)
    elif query.data == 'select_group':
        query.edit_message_text(translate('select_group_not_implemented', user_lang))
    elif query.data == 'owner_menu' or query.data == 'back_to_owner_menu':
        owner_menu(update, context)
    elif query.data == 'back':
        start(update, context)
    elif query.data == 'back_to_main_menu':
        start(update, context)
    elif query.data.startswith('set_language_'):
        set_language(update, context)
    else:
        parts = query.data.split(':')
        logger.debug(f"Parsed parts: {parts}")
        if len(parts) == 3:
            _, module_name, function_name = parts
            logger.debug(f"Module: {module_name}, Function: {function_name}")
            if module_name in MODULES and function_name == 'menu':
                menu_function = MODULES[module_name]
                logger.debug(f"Calling menu function for module: {module_name}")
                menu_function(update, context)
            else:
                logger.debug(f"Menu function not found for module: {module_name}")
                query.edit_message_text(translate('unknown_modulee', user_lang))
        else:
            logger.debug(f"Invalid callback data format: {query.data}")
            query.edit_message_text(translate('unknown_command', user_lang))

def main() -> None:
    init_db()
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), lambda update, context: None))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
