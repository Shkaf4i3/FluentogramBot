from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

from functions.call_fabric import ChoiceLanguage


def choice_language() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    keyboard.button(text='Русский 🇷🇺', callback_data=ChoiceLanguage(lang='ru'))
    keyboard.button(text='Английский 🇬🇧', callback_data=ChoiceLanguage(lang='en'))
    return keyboard.as_markup()
