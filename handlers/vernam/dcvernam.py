from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router

from handlers.keyboards import my_inline_keyboard

router = Router()

class DcVernam(StatesGroup):
    cipher_text = State()
    key = State()

@router.callback_query(lambda c: c.data == 'dcvernam')
async def process_callback_dcvr (callback: CallbackQuery, state: FSMContext):
    if callback.data == 'dcvernam':
        await state.set_state(DcVernam.cipher_text)
        await callback.message.answer('🧠 *CRYPTOAI ONLINE*\n' \
        '📥 *Введите зашифрованное сообщение (hex-строку).*\n')

        await callback.message.answer('_Ожидаю текстовый ввод..._')

    await callback.answer()

@router.message(DcVernam.cipher_text)
async def dcvernam_get_text (message: Message, state: FSMContext):
    user_text = message.text.strip()

    if not user_text:
        await message.answer('🚫 *Пожалуйста, введите текст для дешифрования.*')
        return
    
    await state.update_data(cipher_text=user_text)
    await state.set_state(DcVernam.key)
    await message.answer('⚙️ *Параметры операции:*\n' \
    '*Введите ключ для дешифрования. Длина ключа должна быть равна длине шифротекста:*\n')

@router.message(DcVernam.key)
async def dcvernam_get_key(message: Message, state: FSMContext):
    user_key = message.text.strip()

    if not user_key:
        await message.answer('🚫 *Пожалуйста, введите текст для дешифрования.*')
        return
    
    data = await state.get_data()
    cipher_text = data.get('cipher_text')

    try:
        cipher_bytes = bytes.fromhex(cipher_text)
    except Exception:
        await message.answer('🚫 *Некорректный формат шифротекста (ожидается hex-строка).*')
        return
    
    key_bytes = user_key.encode('utf-8')

    if len(cipher_bytes) != len(key_bytes):
        await message.answer('🚫 *Ключ должен быть той же длины в байтах, что и шифротекст!*')
        return

    # Дешифруем (XOR)
    decrypted_bytes = bytes([b ^ k for b, k in zip(cipher_bytes, key_bytes)])
    try:
        decrypted = decrypted_bytes.decode('utf-8')
    except UnicodeDecodeError:
        await message.answer('🚫 *Ошибка декодирования. Проверьте правильность ключа и шифротекста*')
        return

    await message.answer(f'✅ *Дешифрование завершено.*\n🔓 *Результат:*\n{decrypted}')
    await state.clear()

    await message.answer(
        "📡 *Возврат в главное меню.*\nГотов к следующей операции.",
        reply_markup=my_inline_keyboard
    )