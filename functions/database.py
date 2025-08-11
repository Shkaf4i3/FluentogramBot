from asyncio import sleep

from psqlpy import ConnectionPool, QueryResult
from psqlpy.extra_types import BigInt

from functions.config_reader import config


db_pool = ConnectionPool(
    dsn=config.dsn,
    max_db_pool_size=5,
)


async def create_table() -> None:
    cursor = await db_pool.connection()

    await cursor.execute(querystring="""CREATE TABLE IF NOT EXISTS Users(
                         id SERIAL,
                         tg_id BIGINT,
                         status BOOLEAN DEFAULT False,
                         lang TEXT NOT NULL DEFAULT 'ru')""")


async def add_user(tg_id: int) -> None:
    connection = await db_pool.connection()
    cursor = connection.transaction()
    await cursor.begin()

    data: QueryResult = await cursor.fetch(
        querystring='SELECT * FROM Users WHERE tg_id = ($1)',
        parameters=[BigInt(tg_id)]
    )
    result = data.result()

    if not result:
        await cursor.execute(
            querystring='INSERT INTO Users (tg_id) VALUES ($1)',
            parameters=[BigInt(tg_id)]
        )
        await cursor.commit()


async def update_status_user(tg_id: int) -> None:
    connection = await db_pool.connection()
    cursor = connection.transaction()
    await cursor.begin()

    await cursor.execute(
        querystring='UPDATE Users SET status = True WHERE tg_id = ($1)',
        parameters=[BigInt(tg_id)]
    )
    await cursor.commit()


async def update_lang_user(tg_id: int, lang: str) -> None:
    connection = await db_pool.connection()
    cursor = connection.transaction()
    await cursor.begin()

    await cursor.execute(
        querystring='UPDATE Users SET lang = ($1) WHERE tg_id = ($2)',
        parameters=[lang, BigInt(tg_id)]
    )
    await cursor.commit()


async def get_locale_user(tg_id: int) -> str:
    cursor = await db_pool.connection()
    data: QueryResult = await cursor.fetch(
        querystring='SELECT * FROM Users WHERE tg_id = ($1)',
        parameters=[BigInt(tg_id)]
    )

    result = data.result()
    return result[0]['lang'] if result else await sleep(1)


async def get_status_user(tg_id: int) -> str:
    cursor = await db_pool.connection()
    data: QueryResult = await cursor.fetch(
        querystring='SELECT * FROM Users WHERE tg_id = ($1)',
        parameters=[BigInt(tg_id)]
    )

    result = data.result()
    if result[0]['status']:
        return True
    else:
        return False
