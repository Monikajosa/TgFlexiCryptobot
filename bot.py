import logging
import importlib
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext, Filters, MessageHandler
from config import TOKEN, OWNER_ID, LOG_LEVEL
from admin.owner_admin_module import owner_menu, get_admin_modules
from utils.helpers import is_owner
from utils.translation import translate, get_available_languages
from utils.persistence import get_user_language, set_user_language
from admin.ad_module import ad_function_handler, toggle_ad
from admin.group_manager import add_group, remove_group, get_groups
from admin.module_manager import get_module_function, get_module_names, is_module_enabled, set_module_enabled, get_module_display_name
from data.persistent_storage import init_db

# Konfiguriere das Logging
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
            add_group(chat.id, chat.title)  # Gruppe/Kanal registrieren
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
    keyboard.append([InlineKeyboardButton(translate('back', user_lang), callback_data='back_to_main_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=translate('choose_language', user_lang), reply_markup=reply_markup)

def set_language(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    user_lang = query.data.split('_')[-1]
    set_user_language(query.from_user.id, user_lang)
    print(f"Set user {query.from_user.id} language to {user_lang}")  # Debugging-Ausgabe

    keyboard = [[InlineKeyboardButton(translate('back_to_main_menu', user_lang), callback_data='back_to_main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text=translate('language_set', user_lang), reply_markup=reply_markup)

def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    user_lang = get_user_language(query.from_user.id)
    
    if query.data == 'change_language':
        change_language(update, context)
    elif query.data == 'select_group':
        query.edit_message_text(translate('select_group_not_implemented', user_lang))
    elif query.data == 'owner_menu':
        owner_menu(update, context)
    elif query.data.startswith('module:'):
        module_name = query.data.split(':')[1]
        module_menu(update, context, module_name)
    elif query.data == 'back':
        start(update, context)
    elif query.data == 'back_to_main_menu':
        start(update, context)
    elif query.data.startswith('set_language_'):
        set_language(update, context)
    elif query.data.startswith('toggle_ad_'):
        toggle_ad(update, context)
    elif query.data == 'ad_function':
        ad_function_handler(update, context)
    elif query.data == 'module_management':  # Fügen Sie diese Zeile hinzu
        module_manager_menu(update, context)  # Fügen Sie diese Zeile hinzu
    elif query.data == 'back_to_owner_menu':
        owner_menu(update, context)  # Zurück zum Owner-Menü
    else:
        parts = query.data.split(':')
        if len(parts) == 2:
            module_name, function_name = parts
            module_function = get_module_function(module_name, function_name)
            if module_function:
                module_function(update, context)
            else:
                query.edit_message_text(translate('unknown_command', user_lang))
        else:
            query.edit_message_text(translate('unknown_command', user_lang))

def owner_menu(update: Update, context: CallbackContext) -> None:
    user_lang = get_user_language(update.effective_user.id)
    admin_modules = get_admin_modules()

    # Dynamisch generierte Buttons für Module
    module_buttons = [
        [InlineKeyboardButton(get_module_display_name(module, user_lang), callback_data=f'module:{module}')]
        for module in get_module_names()
    ]
    
    # Zusätzliche Admin-Module
    admin_module_buttons = [
        [InlineKeyboardButton(translate(module['name_key'], user_lang), callback_data=module['callback_data'])]
        for module in admin_modules
    ]

    # Button für AD Function
    ad_button = InlineKeyboardButton(translate('ad_function', user_lang), callback_data='ad_function')

    # Button für Module Management
    module_manager_button = InlineKeyboardButton(translate('module_manager', user_lang), callback_data='module_management')  # Fügen Sie diese Zeile hinzu

    # Kombinieren Sie alle Buttons in einer Liste und stellen Sie sicher, dass keine Liste leer ist
    keyboard = module_buttons + admin_module_buttons + [[ad_button], [module_manager_button]]  # Passen Sie diese Zeile an
    keyboard.append([InlineKeyboardButton(translate('back_to_main_menu', user_lang), callback_data='back_to_main_menu')])

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        update.message.reply_text(translate('owner_menu', user_lang), reply_markup=reply_markup)
    elif update.callback_query:
        update.callback_query.message.edit_text(translate('owner_menu', user_lang), reply_markup=reply_markup)

def module_menu(update: Update, context: CallbackContext, module_name: str) -> None:
    user_lang = get_user_language(update.effective_user.id)
    module_functions = [func for func in dir(importlib.import_module(f'admin.{module_name}')) if callable(getattr(importlib.import_module(f'admin.{module_name}'), func))]

    keyboard = [
        [InlineKeyboardButton(func, callback_data=f'{module_name}:{func}')]
        for func in module_functions
    ]

    keyboard.append([InlineKeyboardButton(translate('back', user_lang), callback_data='owner_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        update.message.reply_text(translate(f'{module_name}_functions', user_lang), reply_markup=reply_markup)
    elif update.callback_query:
        update.callback_query.message.edit_text(translate(f'{module_name}_functions', user_lang), reply_markup=reply_markup)

def module_manager_menu(update: Update, context: CallbackContext) -> None:
    user_lang = get_user_language(update.effective_user.id)
    module_names = get_module_names()

    keyboard = [
        [InlineKeyboardButton(get_module_display_name(module, user_lang), callback_data=f'toggle_module:{module}')]
        for module in module_names
    ]

    keyboard.append([InlineKeyboardButton(translate('back', user_lang), callback_data='owner_menu')])
    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        update.message.reply_text(translate('module_manager', user_lang), reply_markup=reply_markup)
    elif update.callback_query:
        update.callback_query.message.edit_text(translate('module_manager', user_lang), reply_markup=reply_markup)

def main() -> None:
    init_db()
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    # Handler für den /start Befehl
    dispatcher.add_handler(CommandHandler("start", start))

    # CallbackQueryHandler für Buttons
    dispatcher.add_handler(CallbackQueryHandler(button))

    # Filtern von Nachrichten, die keine Befehle sind, um keine Antwort zu senden
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), lambda update, context: None))

    updater.start_polling()
    updater.idle()

def specific_command(update: Update, context: CallbackContext) -> None:
    # Beispiel für einen spezifischen Befehl in einem Modul
    update.message.reply_text("Dies ist ein spezifischer Befehl, der in Gruppen/Kanälen funktioniert.")

if __name__ == '__main__':
    main()
