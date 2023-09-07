from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Кнопка 1")],
            [KeyboardButton(text="Кнопка 2")],
            # Добавьте остальные кнопки
            [KeyboardButton(text="Команды")]  # Добавляем кнопку для открытия меню с командами
        ],
        resize_keyboard=True
    )
    return keyboard

def get_commands_menu():
    commands_menu = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton("Команда 1", callback_data="command1"),
                InlineKeyboardButton("Команда 2", callback_data="command2"),
                # Добавьте остальные команды
            ]
        ]
    )
    return commands_menu