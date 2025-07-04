from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


from handlers.keyboards import my_inline_keyboard

router = Router()


class Caesar(StatesGroup):
    text = State()  # Состояние для ввода текста для шифрования Цезаря
    shift = State()  # Состояние для ввода сдвига шифра Цезаря



def caesar_cipher(text: str, shift: int):
    # Определяем язык текста: русский или английский
    def is_cyrillic(s):
        return any('а' <= c.lower() <= 'я' for c in s if c.isalpha())

    result = []
    if is_cyrillic(text):
        # Русский алфавит
        alphabet_lower = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
        alphabet_upper = alphabet_lower.upper()
        n = len(alphabet_lower)
        for char in text:
            if char in alphabet_lower:
                idx = alphabet_lower.index(char)
                result.append(alphabet_lower[(idx + shift) % n])
            elif char in alphabet_upper:
                idx = alphabet_upper.index(char)
                result.append(alphabet_upper[(idx + shift) % n])
            else:
                result.append(char)
    else:
        # Английский алфавит
        for char in text:
            if char.isalpha():
                shift_base = ord('A') if char.isupper() else ord('a')
                shifted_char = chr((ord(char) - shift_base + shift) % 26 + shift_base)
                result.append(shifted_char)
            else:
                result.append(char)
    return ''.join(result)





@router.callback_query(lambda c: c.data == 'caesar')
async def process_callback_ch(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'caesar':
        await state.set_state(Caesar.text)
        await callback.message.answer('🧠 *CRYPTOAI ONLINE*\n' \
        '📥 *Введите исходный текст для шифрования.*\n')

        await callback.message.answer('_Ожидаю текстовый ввод..._')

    await callback.answer()

@router.message(Caesar.text)
async def caesar_get_text(message: Message, state: FSMContext):
    user_text = message.text.strip()

    if not user_text:
        await message.answer('🚫 *Пожалуйста, введите текст для шифрования.*')
        return
    
    if user_text.isdigit():
        await message.answer('🚫 *Текст не должен состоять только из цифр. Пожалуйста, введите корректный текст.*')
        return
    
    # Сохраняем текст в состоянии



    await state.update_data(text=message.text)
    await state.set_state(Caesar.shift)
    await message.answer('⚙️ *Параметры операции:*\n' \
    '*Введите сдвиг шифра Цезаря (число от 1 до 25):\n')

    await message.answer('_Пример: 3, 17, 24..._')

@router.message(Caesar.shift)
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

    encrypted = caesar_cipher(text, shift)
    await message.answer('✅ *Шифрование завершено.*')
    await message.answer(f'🔐 *Зашифрованный текст:\n{encrypted}')
    await state.clear()

    await message.answer(
        "📡 *Возврат в главное меню.*\nГотов к следующей операции.",
        reply_markup=my_inline_keyboard
)
    


    


