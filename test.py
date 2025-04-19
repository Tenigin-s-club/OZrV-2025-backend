import asyncio

from googletrans import Translator, LANGUAGES


async def translate_text(text, dest_language='ru', src_language='auto'):
    try:
        translator = Translator()
        translation = await translator.translate(text, dest=dest_language, src=src_language)
        return translation.text
    except Exception as e:
        return f"Ошибка перевода: {str(e)}"





if __name__ == "__main__":
    asyncio.run(main())