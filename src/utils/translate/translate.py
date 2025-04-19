from googletrans import Translator

async def translate_text(text, dest_language='ru', src_language='auto'):
    try:
        translator = Translator()
        translation = await translator.translate(text, dest=dest_language, src=src_language)
        return translation.text
    except Exception as e:
        return f"Ошибка перевода: {str(e)}"


