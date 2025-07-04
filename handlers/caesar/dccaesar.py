from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from handlers.caesar.caesar_cipher import caesar_cipher
from handlers.keyboards import my_inline_keyboard

router = Router()

class DcCaesar(StatesGroup):
    text = State()
    shift = State()

@router.callback_query(lambda c: c.data == 'dccaesar')
async def process_callback_dc(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'dccaesar':
        await state.set_state(DcCaesar.text)
        await callback.message.answer('🧠 *CRYPTOAI ONLINE*\n' \
        '📥 *Введите исходный текст для дешифрования.*\n')

        await callback.message.answer('_Ожидаю текстовый ввод..._')

    await callback.answer()

@router.message(DcCaesar.text)
async def dccaesar (message: Message, state: FSMContext):
    user_text = message.text.strip()

    if not user_text:
        await message.answer('🚫 *Пожалуйста, введите текст для дешифрования Цезаря.*')
        return
    
    if user_text.isdigit():
        await message.answer('🚫 *Текст не должен состоять только из цифр. Пожалуйста, введите корректный текст.*')
        return
    
    # Сохраняем текст в состоянии

    await state.update_data(text=message.text)
    await state.set_state(DcCaesar.shift)
    await message.answer('⚙️ *Параметры операции:*\n' \
    '*Введите сдвиг шифра Цезаря (число от 1 до 25):\n')

    await message.answer('_Пример: 3, 17, 24..._')

@router.message(DcCaesar.shift)
async def caesar_get_shift(message: Message, state: FSMContext):
    user_shift = message.text.strip()

    if not user_shift.isdigit():
        await message.answer('🚫 *Пожалуйста, введите целое число от 1 до 25.*')
        return
    
    shift = int(user_shift)
    if shift < 1 or shift > 25:
        await message.answer('🚫 *Сдвиг должен быть числом от 1 до 25. Попробуйте еще раз.*')
        return
    
    data = await state.get_data()
    text = data.get('text')

    encrypted = caesar_cipher(text, -shift)
    await message.answer('✅ *Дешифрование завершено.*')
    await message.answer(f'🔐 *Дешифрованный текст:\n{encrypted}')
    await state.clear()

    await message.answer(
        "📡 *Возврат в главное меню.*\nГотов к следующей операции.",
        reply_markup=my_inline_keyboard
)

