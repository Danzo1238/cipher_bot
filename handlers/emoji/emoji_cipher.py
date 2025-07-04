from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import CallbackQuery


from handlers.keyboards import my_inline_keyboard

router = Router()

class EmojiStates(StatesGroup):
    text = State()


def combine_emoji():
        cyrillic_to_emoji = {
    'а': '😀',   'А': '😁',
    'б': '😂',   'Б': '🤓',
    'в': '😎',   'В': '😍',
    'г': '🥰',   'Г': '🤖',
    'д': '😺',   'Д': '🙀',
    'е': '👹',   'Е': '👺',
    'ё': '🙈',   'Ё': '🙉',
    'ж': '🙊',   'Ж': '🐵',
    'з': '🐸',   'З': '🤩',
    'и': '🥳',   'И': '🤠',
    'й': '🧐',   'Й': '😇',
    'к': '😈',   'К': '🤡',
    'л': '👻',   'Л': '👽',
    'м': '💀',   'М': '👾',
    'н': '🦝',   'Н': '🦄',
    'о': '🐱',   'О': '🐶',
    'п': '🦊',   'П': '🐉',
    'р': '🦋',   'Р': '🐠',
    'с': '🦚',   'С': '🦜',
    'т': '🐲',   'Т': '🦖',
    'у': '🦕',   'У': '🐊',
    'ф': '🐢',   'Ф': '🐍',
    'х': '🦎',   'Х': '🦂',
    'ц': '🦀',   'Ц': '🦞',
    'ч': '🦐',   'Ч': '🦑',
    'ш': '🐙',   'Ш': '🦈',
    'щ': '🐬',   'Щ': '🐳',
    'ъ': '🐋',   'Ъ': '🦭',
    'ы': '🦦',   'Ы': '🦫',
    'ь': '🐿️',   'Ь': '🦔',
    'э': '🦇',   'Э': '🦉',
    'ю': '🦢',   'Ю': '🦩',
    'я': '🦚',   'Я': '🦜',
}

        latin_to_emoji = {
    'a': '🍏',   'A': '🍎',
    'b': '🍐',   'B': '🍊',
    'c': '🍋',   'C': '🍌',
    'd': '🍉',   'D': '🍇',
    'e': '🍓',   'E': '🍈',
    'f': '🍒',   'F': '🍑',
    'g': '🥭',   'G': '🍍',
    'h': '🥥',   'H': '🥝',
    'i': '🍅',   'I': '🍆',
    'j': '🥑',   'J': '🥦',
    'k': '🥬',   'K': '🥒',
    'l': '🌽',   'L': '🥕',
    'm': '🧄',   'M': '🧅',
    'n': '🥔',   'N': '🍠',
    'o': '🥐',   'O': '🥨',
    'p': '🥯',   'P': '🍞',
    'q': '🥖',   'Q': '🧀',
    'r': '🥚',   'R': '🍳',
    's': '🧇',   'S': '🥞',
    't': '🧈',   'T': '🍤',
    'u': '🥮',   'U': '🍢',
    'v': '🥟',   'V': '🍥',
    'w': '🍡',   'W': '🍦',
    'x': '🍧',   'X': '🍨',
    'y': '🥧',   'Y': '🍰',
    'z': '🎂',   'Z': '🧁',
}
    
        digits_to_emoji = {
    '0': '0️⃣',
    '1': '1️⃣',
    '2': '2️⃣',
    '3': '3️⃣',
    '4': '4️⃣',
    '5': '5️⃣',
    '6': '6️⃣',
    '7': '7️⃣',
    '8': '8️⃣',
    '9': '9️⃣',
}
    
        combine_dict = {**cyrillic_to_emoji, **latin_to_emoji, **digits_to_emoji}
        return combine_dict

@router.callback_query(lambda c: c.data == 'emoji')
async def emoji_handler(callback: CallbackQuery, state: FSMContext):
        await state.set_state(EmojiStates.text)
        await callback.message.answer('🧠 *CRYPTOAI ONLINE*\n' \
                                      '📥 *Введите исходный текст для шифрования с помощью эмодзи.*\n')
        await callback.message.answer('_Ожидаю текстовый ввод..._')

        await callback.answer()

@router.message(EmojiStates.text)
async def emoji_text_handler(message: Message, state: FSMContext):
    text = message.text.strip()

    if not text:
        await message.answer('🚫 *Пожалуйста, введите текст для шифрования.*')
        return
    
    emoji_dict = combine_emoji()

    encrypted_text = ''.join(emoji_dict.get(char, char) for char in text)
    await message.answer('✅ *Шифрование завершено.*')
    await message.answer(f'🔐 *Зашифрованный текст:\n{encrypted_text}')

    await state.clear()
    await message.answer(
        "📡 *Возврат в главное меню.*\nГотов к следующей операции.",
        reply_markup=my_inline_keyboard
)