from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from handlers.keyboards import my_inline_keyboard

router = Router()

class Vernam(StatesGroup):
    text = State()
    key = State()

def vernam_cipher(text: str, key: str) -> bytes:
    text_bytes = text.encode('utf-8')
    key_bytes = key.encode('utf-8')

    if len(text_bytes) != len(key_bytes):
        raise ValueError("Длина ключа в байтах должна быть равна длине текста")

    encrypted = bytes([t ^ k for t, k in zip(text_bytes, key_bytes)])
    return encrypted


@router.callback_query(lambda c: c.data == 'vernam')
async def process_callback_vr (callback: CallbackQuery, state: FSMContext):
    if callback.data == 'vernam':
        await state.set_state(Vernam.text)
        await callback.message.answer('🧠 *CRYPTOAI ONLINE*\n' \
        '📥 *Введите исходный текст для шифрования.*\n')

        await callback.message.answer('_Ожидаю текстовый ввод..._')

    await callback.answer()

@router.message(Vernam.text)
async def vernam_get_text(message: Message, state: FSMContext):
    user_text = message.text.strip()

    if not user_text:
        await message.answer('🚫 *Пожалуйста, введите текст для шифрования.*')
        return
    
    await state.update_data(text=user_text)
    await state.set_state(Vernam.key)
    await message.answer('⚙️ *Параметры операции:*\n' \
    '*Введите ключ для шифрования (любые символы). Длина ключа должна быть равна длине шифруемого текста:\n')

@router.message(Vernam.key)
async def vernam_get_key (message: Message, state: FSMContext):
    user_key = message.text.strip()

    if not user_key:
        await message.answer('🚫 *Пожалуйста, введите текст для шифрования.*')
        return
    
    data = await state.get_data()
    text = data.get('text')

    if len(user_key.encode('utf-8')) != len(text.encode('utf-8')):
        await message.answer('🚫 *Ключ должен быть той же длины что и текст*')
        return
    
    encrypted = vernam_cipher(text, user_key)
    await message.answer(f'✅ *Шифрование завершено.*\n🔐 *Результат (hex):*\n{encrypted.hex()}')
    await state.clear()

    await message.answer(
        "📡 *Возврат в главное меню.*\nГотов к следующей операции.",
        reply_markup=my_inline_keyboard
    )

