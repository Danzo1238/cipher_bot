from aiogram import Router
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.types import CallbackQuery

from handlers.keyboards import my_inline_keyboard
from handlers.emoji.emoji_cipher import combine_emoji


router = Router()

class DcEmojiStates(StatesGroup):
    text = State()

def decode_emoji_text(text: str):
    emoji_dict = combine_emoji()
    decode_dict = {v: k for k, v in emoji_dict.items()}

    result = ''
    i = 0
    while i < len(text):
        matched = False
        for emoji in sorted(decode_dict, key=len, reverse=True):
            if text.startswith(emoji, i):
                result += decode_dict[emoji]
                i += len(emoji)
                matched = True
                break
        if not matched:
            result += text[i]
            i += 1
    return result



@router.callback_query(lambda c: c.data == 'dcemoji')
async def dc_emoji_handler (callback: CallbackQuery, state: FSMContext):
        await state.set_state(DcEmojiStates.text)
        await callback.message.answer('🧠 *CRYPTOAI ONLINE*\n' \
                                      '📥 *Введите исходный текст для дешифрования с помощью эмодзи.*\n')
        await callback.message.answer('_Ожидаю текстовый ввод..._')

        await callback.answer()

@router.message(DcEmojiStates.text)
async def dc_emoji (message: Message, state: FSMContext):
    text = message.text.strip()

    if not text:
        await message.answer('🚫 *Пожалуйста, введите текст для дешифрования.*')
        return
    
    
    
    emoji_dict = combine_emoji()
    decoded_text = decode_emoji_text(text)


    await message.answer(f'🔓 *Дешифрованный текст:*\n{decoded_text}')
    await state.clear()

    await message.answer(
        "📡 *Возврат в главное меню.*\nГотов к следующей операции.",
        reply_markup=my_inline_keyboard
)