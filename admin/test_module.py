from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from utils.translation import translate
from utils.persistence import get_user_language

module_name_key = "test_module"

def test_module_menu(update: Update, context: CallbackContext):
    """This function creates the test menu with a single button."""
    user_lang = get_user_language(update.effective_user.id)

    keyboard = [[InlineKeyboardButton("X", callback_data="test_X")]]

    keyboard.append([InlineKeyboardButton(translate('back', user_lang), callback_data='back_to_owner_menu')])

    reply_markup = InlineKeyboardMarkup(keyboard)
    update.callback_query.message.reply_text("Test Menu", reply_markup=reply_markup)

def handle_button(update: Update, context: CallbackContext):
    """This function handles the button press and outputs 'Y'."""
    query = update.callback_query
    query.answer()
    query.message.reply_text("Y")
