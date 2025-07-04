from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton


my_inline_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='🏛️ Шифр Цезаря', callback_data='caesar'),
            InlineKeyboardButton(text='🔐 Расшифровка Цезаря', callback_data='dccaesar')
        ],
        [
            InlineKeyboardButton(text='🛡️ Шифр Вернама', callback_data='vernam'),
            InlineKeyboardButton(text='🗝️ Расшифровка Вернама', callback_data='dcvernam')
        ],
        [
            InlineKeyboardButton(text='🌞 Эмодзи шифр', callback_data='emoji'),
            InlineKeyboardButton(text='🔍 Расшифровка эмодзи', callback_data='dcemoji')
        ]
    ])


my_reply_keyboard = ReplyKeyboardMarkup(keyboard=[[
    KeyboardButton(text='Меню', callback_data='Меню'),
    KeyboardButton(text='Обо мне', callback_data='Обо мне')
]], resize_keyboard=True)
