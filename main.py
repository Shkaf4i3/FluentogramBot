from asyncio import run
from logging import basicConfig, INFO

from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode

from functions.config_reader import config
from functions.database import create_table
from translator.translator_middleware import CheckLocaleMessageUser, CheckLocaleCallbackUser
from handlers.admin_private import admin


async def main() -> None:
    await create_table()

    bot = Bot(token=config.bot_token.get_secret_value(),
              default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router=admin)
    dp.message.middleware(CheckLocaleMessageUser())
    dp.callback_query.middleware(CheckLocaleCallbackUser())

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    basicConfig(
        level=INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s",
        )

    try:
        run(main(), loop_factory=None)
    except KeyboardInterrupt:
        print('Exit')
