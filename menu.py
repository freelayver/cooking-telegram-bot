from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn1 = KeyboardButton('Анализ продукта')
btn2 = KeyboardButton('Рецепты')
btn3 = KeyboardButton('Консультант')
btn4 = KeyboardButton('Калькулятор')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btn1,btn2,btn3, btn4)
