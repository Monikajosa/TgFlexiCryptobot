import importlib
import pkgutil
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from utils.translation import translate
from utils.persistence import get_user_language

def get_admin_modules():
    admin_modules = []
    package = 'admin'
    for _, module_name, _ in pkgutil.iter_modules([package]):
        module = importlib.import_module(f'{package}.{module_name}')
        if hasattr(module, 'module_name_key'):
            admin_modules.append({
                'name_key': module.module_name_key,  # Der Schlüssel für die Übersetzung des Modulnamens
                'callback_data': module_name  # Der Modulname für die callback_data
            })
    return admin_modules

def owner_menu(update: Update, context: CallbackContext):
    user_lang = get_user_language(update.effective_user.id)
    admin_modules = get_admin_modules()

    keyboard = [
        [InlineKeyboardButton(translate(module['name_key'], user_lang), callback_data=f'module:{module["callback_data"]}')]
        for module in admin_modules
    ]

    keyboard.append([InlineKeyboardButton(translate('back_to_main_menu', user_lang), callback_data='back_to_main_menu')])

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        update.message.reply_text(translate('owner_menu', user_lang), reply_markup=reply_markup)
    elif update.callback_query:
        update.callback_query.message.edit_text(translate('owner_menu', user_lang), reply_markup=reply_markup)
