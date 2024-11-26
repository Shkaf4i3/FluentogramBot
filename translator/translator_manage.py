from fluentogram import TranslatorHub
from fluentogram import FluentTranslator
from fluent_compiler.bundle import FluentBundle

from locales.path_dir import WORKDIR


ru_ftl = [WORKDIR / 'ru.ftl']
en_ftl = [WORKDIR / 'en.ftl']


t_hub = TranslatorHub(
    locales_map={
        "ru": ("ru", "en"),
        "en": ("en"),
    },
    translators=[
        FluentTranslator(
            locale='ru',
            translator=FluentBundle.from_files(locale='ru-RU', filenames=ru_ftl)
        ),
        FluentTranslator(
            locale='en',
            translator=FluentBundle.from_files(locale='en-US', filenames=en_ftl)
        ),
    ],
    root_locale='en'
)
