from typing import Callable, Dict, Any, Awaitable
from copy import copy

from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from translator.translator_manage import t_hub
from functions.database import get_locale_user



class CheckLocaleMessageUser(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
                       event: Message,
                       data: Dict[str, Any]) -> Any:
        new_data = copy(data)
        new_data['i18n'] = t_hub.get_translator_by_locale(
            locale=await get_locale_user(tg_id=event.from_user.id)
        )

        return await handler(event, new_data)


class CheckLocaleCallbackUser(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
                       event: CallbackQuery,
                       data: Dict[str, Any]) -> Any:
        new_data = copy(data)
        new_data['i18n'] = t_hub.get_translator_by_locale(
            locale=await get_locale_user(tg_id=event.message.from_user.id)
        )

        return await handler(event, new_data)
