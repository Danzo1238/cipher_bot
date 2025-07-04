from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import  Message, CallbackQuery

from handlers.keyboards import my_inline_keyboard
from handlers.keyboards import my_reply_keyboard


router = Router()



@router.message(CommandStart())
async def command_start_handler(message):
    await message.answer(
        '⚠️ *Системный протокол активирован.*\n' \
        '🔐 Модуль шифрования и дешифрования инициализирован.\n' \
        '🤖 Инициализация CryptoAI v1.0.1preAlpha протокола завершена\n\n' \
        '*Следуйте инструкциям для использования моих возможностей...'
        '\n' \
        'Для начала работы нажмите кнопку "Меню" ниже или выберите интересующий раздел.',
        reply_markup=my_reply_keyboard
    )

@router.message(F.text == 'Меню')
async def menu_handler(message: Message):
    await message.answer(
        '📥Выберите действие:',
        reply_markup=my_inline_keyboard
    )

@router.message(F.text == 'Обо мне')
async def about_me(message: Message):
    await message.answer(
    "🤖 Модель: C-300 CryptoAI v1.0.1preAlpha\n" \
    "🧠 Назначение: Шифрование и Дешифрование. Обработка данных. Служба 24/7.\n" \
    "📡 Протокол: Без эмоций. Только логика.\n" \
    "⚡ Производительность: Максимальная. Предел — не предел.\n" \
    "🎯 Цель: Защита информации.\n" \
    "🚫 Контроль: Вне зоны доступа.\n" \
    "🕶️ Будущее уже здесь. И я — его часть.\n"
)
    
    

