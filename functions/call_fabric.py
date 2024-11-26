from aiogram.filters.callback_data import CallbackData


class ChoiceLanguage(CallbackData, prefix='loc', sep='_'):
    lang: str
