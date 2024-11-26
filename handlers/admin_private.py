from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from fluentogram import TranslatorRunner

from functions.database import add_user, get_status_user, update_status_user, update_lang_user
from functions.call_fabric import ChoiceLanguage
import functions.keyboard as kb


admin = Router()


@admin.message(CommandStart())
async def start_message(message: Message, i18n: TranslatorRunner) -> None:
    await add_user(tg_id=message.from_user.id)
    result = await get_status_user(tg_id=message.from_user.id)

    if not result:
        await message.answer(text='Выбери язык', reply_markup=kb.choice_language())
    else:
        await message.answer(i18n.hello())


@admin.message(Command('help'))
async def help_message(message: Message, i18n: TranslatorRunner) -> None:
    await message.answer(i18n.help())


@admin.callback_query(ChoiceLanguage.filter())
async def update_locale_user(callback: CallbackQuery,
                             callback_data: ChoiceLanguage,
                             i18n: TranslatorRunner) -> None:
    await callback.message.delete()

    if callback_data.lang == 'ru':
        await update_status_user(tg_id=callback.from_user.id)
        await callback.message.answer(text=i18n.restart())
    elif callback_data.lang == 'en':
        await update_status_user(tg_id=callback.from_user.id)
        await update_lang_user(tg_id=callback.from_user.id, lang='en')
        await callback.message.answer(text=i18n.restart())

    await callback.answer()
