import os
import importlib
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from utils.translation import translate
from utils.persistence import get_user_language

def get_admin_modules():
    modules = []
    admin_path = os.path.dirname(__file__)
    for filename in os.listdir(admin_path):
        if filename.endswith(".py") and filename != "__init__.py" and filename != "ad_module.py":
            module_name = filename[:-3]
            module = importlib.import_module(f"admin.{module_name}")
            if hasattr(module, "module_name_key"):
                modules.append({
                    "name_key": getattr(module, "module_name_key"),
                    "callback_data": module_name
                })
    return modules

def owner_menu(update: Update, context: CallbackContext) -> None:
    user_lang = get_user_language(update.effective_user.id)
    admin_modules = get_admin_modules()

    # Dynamisch generierte Buttons für Module
    keyboard = [
        [InlineKeyboardButton(translate(module['name_key'], user_lang), callback_data=module['callback_data'])]
        for module in admin_modules
    ]

    # Füge den AD Function Button separat hinzu
    ad_button = InlineKeyboardButton(translate('ad_function', user_lang), callback_data='ad_function')
    keyboard.append([ad_button])
    
    keyboard.append([InlineKeyboardButton(translate('back', user_lang), callback_data='back_to_main_menu')])

    reply_markup = InlineKeyboardMarkup(keyboard)

    if update.message:
        update.message.reply_text(translate('owner_menu', user_lang), reply_markup=reply_markup)
    elif update.callback_query:
        update.callback_query.message.edit_text(translate('owner_menu', user_lang), reply_markup=reply_markup)
