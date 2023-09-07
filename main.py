import json

from aiogram import Bot, Dispatcher, executor, types
import menu
from edamam import make_api_request
from edamam2 import recipe_api_request
from gpt import translater_data
from calc import calc_calories


from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage




#ТОКЕН СЮДА
TOKEN_API = "6389738172:AAH81VuRHz2LvTZTHvit3ybCgOla9-H2X3g"

condition = ''
bot = Bot(TOKEN_API)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
user_input_state = {}



# Клавиатура для выбора пола
gender_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="мужчина"), KeyboardButton(text="женщина")]
    ],
    resize_keyboard=True
)

# Клавиатура для выбора активности
activity_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="активный"), KeyboardButton(text="сидячий")]
    ],
    resize_keyboard=True
)


class OnboardingStates(StatesGroup):
    waiting_for_gender = State()    # Ожидание пола пользователя
    waiting_for_age = State()       # Ожидание возраста пользователя
    waiting_for_weight = State()    # Ожидание веса пользователя
    waiting_for_height = State()    # Ожидание роста пользователя
    waiting_for_activity = State()  # Ожидание активности пользователя
    waiting_for_product = State()  # Ожидание ввода продукта для анализа
    waiting_for_recipe = State()  # Ожидание ввода продукта для поиска рецепта

@dp.message_handler(commands='start')
async def command_start(message: types.Message):
    user_name = message.from_user.first_name
    await message.answer(f'{user_name}!!! Давай начнем онбординг! Укажите ваш пол:' ,  reply_markup=gender_keyboard)
    await OnboardingStates.waiting_for_gender.set()

# Обработка пола пользователя
@dp.message_handler(lambda message: message.text not in ["мужчина", "женщина"], state=OnboardingStates.waiting_for_gender)
async def process_gender_invalid(message: types.Message):
    await message.reply("Пожалуйста, выберите ваш пол с помощью кнопок.")

@dp.message_handler(lambda message: message.text in ["мужчина", "женщина"], state=OnboardingStates.waiting_for_gender)
async def process_gender(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['gender'] = message.text
        await message.reply("Отлично! Теперь введите ваш возраст:", reply_markup=ReplyKeyboardRemove())
        await OnboardingStates.next()

# Обработка возраста пользователя
@dp.message_handler(lambda message: not message.text.isdigit(), state=OnboardingStates.waiting_for_age)
async def process_age_invalid(message: types.Message):
    await message.reply("Пожалуйста, введите корректный возраст в виде числа.")

@dp.message_handler(lambda message: message.text.isdigit(), state=OnboardingStates.waiting_for_age)
async def process_age(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['age'] = int(message.text)
        await message.reply("Отлично! Теперь введите ваш вес (в килограммах):")
        await OnboardingStates.next()

# Обработка веса пользователя
@dp.message_handler(lambda message: not message.text.replace('.', '', 1).isdigit(), state=OnboardingStates.waiting_for_weight)
async def process_weight_invalid(message: types.Message):
    await message.reply("Пожалуйста, введите корректный вес в виде числа (например, 70.5).")

@dp.message_handler(lambda message: message.text.replace('.', '', 1).isdigit(), state=OnboardingStates.waiting_for_weight)
async def process_weight(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['weight'] = float(message.text)
        await message.reply("Отлично! Теперь введите ваш рост (в сантиметрах):")
        await OnboardingStates.next()

# Обработка роста пользователя
@dp.message_handler(lambda message: not message.text.isdigit(), state=OnboardingStates.waiting_for_height)
async def process_height_invalid(message: types.Message):
    await message.reply("Пожалуйста, введите корректный рост в сантиметрах (например, 175).")

@dp.message_handler(lambda message: message.text.isdigit(), state=OnboardingStates.waiting_for_height)
async def process_height(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['height'] = int(message.text)
        await message.reply("Отлично! Наконец, выберите вашу активность:", reply_markup=activity_keyboard)
        await OnboardingStates.next()

# Обработка активности пользователя
@dp.message_handler(lambda message: message.text not in ["активный", "сидячий"], state=OnboardingStates.waiting_for_activity)
async def process_activity_invalid(message: types.Message):
    await message.reply("Пожалуйста, выберите вашу активность с помощью кнопок.")

@dp.message_handler(lambda message: message.text in ["активный", "сидячий"], state=OnboardingStates.waiting_for_activity)
async def process_activity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['activity'] = message.text
        # Здесь можно выполнить дополнительную обработку данных или отправить сообщение об успешном завершении
        await message.reply("Спасибо за заполнение онбординга! Вы успешно завершили процесс.", reply_markup=types.ReplyKeyboardRemove())
        await state.finish()


@dp.message_handler(commands='use_results')
async def use_results(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        gender = data.get('gender')
        age = data.get('age')
        weight = data.get('weight')
        height = data.get('height')
        activity = data.get('activity')

        if all([gender, age, weight, height, activity]):
            results_str = (
                f"Пол: {gender}, Возраст: {age}, Вес: {weight} кг, "
                f"Рост: {height} см, Активность: {activity}"
            )
            await message.reply(f"Результаты онбординга:\n{results_str}")
        else:
            await message.reply("Результаты онбординга еще не заполнены.")




# @dp.message_handler(commands=['menu'])
# async def echo(message: types.Message):
#     await message.answer("Выберите действие:", reply_markup=menu.mainMenu)





# @dp.message_handler(lambda message: message.text == "Анализ продукта")
# async def echo(message: types.Message):
#     await message.answer("Пожалуйста, введите продукт, чтобы определить количество калорий.")
#     global condition
#     condition = 1
#
#
# @dp.message_handler(lambda message: message.text == "Рецепты")
# async def echo(message: types.Message):
#     await message.answer("Пожалуйста, введите продукт для поиска рецепта.")
#     global condition
#     condition = 2
#
#
# @dp.message_handler(lambda message: message.text == "Калькулятор")
# async def echo(message: types.Message):
#     await message.answer("Введите.")
#     global condition
#     condition = 3



@dp.message_handler(commands=['product_analysis'])
async def product_analysis(message: types.Message):
    await message.answer("Пожалуйста, введите продукт, чтобы определить количество калорий.")
    await OnboardingStates.waiting_for_product.set()


@dp.message_handler(commands=['recipe'])
async def recipe(message: types.Message):
    await message.answer("Пожалуйста, введите продукт для поиска рецепта.")
    await OnboardingStates.waiting_for_recipe.set()


@dp.message_handler(state=OnboardingStates.waiting_for_product)
async def product_analysis_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product'] = message.text
    user_input = data['product']
    await message.answer(f"Ваш продукт: {user_input}")
    data = make_api_request(user_input)
    await message.answer(f"Количество калорий: {data['calories']},\nБелки: {data['totalNutrients']['PROCNT']['quantity']} {data['totalNutrients']['PROCNT']['unit']},\nЖиры: {data['totalNutrients']['FAT']['quantity']} {data['totalNutrients']['FAT']['unit']},\nУглеводы: {data['totalNutrients']['CHOCDF']['quantity']} {data['totalNutrients']['CHOCDF']['unit']}")
    await state.finish()

@dp.message_handler(state=OnboardingStates.waiting_for_recipe)
async def recipe_handler(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product'] = message.text
        user_input = data['product']
        data = recipe_api_request(user_input)
        new_data = translater_data(data['hits'][0]['recipe']['ingredientLines'])
        await message.answer_photo(photo=types.InputFile.from_url(data['hits'][0]['recipe']['image']))
        await message.answer(f"{data['hits'][0]['recipe']['label']}\nКалории: {data['hits'][0]['recipe']['calories']},\nБелки: {data['hits'][0]['recipe']['totalNutrients']['PROCNT']['quantity']} {data['hits'][0]['recipe']['totalNutrients']['PROCNT']['unit']},\nЖиры: {data['hits'][0]['recipe']['totalNutrients']['FAT']['quantity']} {data['hits'][0]['recipe']['totalNutrients']['FAT']['unit']},\nУглеводы: {data['hits'][0]['recipe']['totalNutrients']['CHOCDF']['quantity']} {data['hits'][0]['recipe']['totalNutrients']['CHOCDF']['unit']},\nРецепт: {new_data}")
        await state.finish()  # Завершение состояния


# @dp.message_handler(lambda message: message.text != "Анализ продукта" and condition==1)
# async def echo(message: types.Message):
#     ##
#     global user_input_state
#     user_input_state[message.from_user.id] = message.text
#     ##
#     user_input = get_user_input(message.from_user.id)
#     await message.answer(f"Ваш продукт: {user_input}")
#     ##
#     data = make_api_request(user_input)
#     await message.answer(f"Количество калорий: {data['calories']},\nБелки: {data['totalNutrients']['PROCNT']['quantity']} {data['totalNutrients']['PROCNT']['unit']},\nЖиры: {data['totalNutrients']['FAT']['quantity']} {data['totalNutrients']['FAT']['unit']},\nУглеводы: {data['totalNutrients']['CHOCDF']['quantity']} {data['totalNutrients']['CHOCDF']['unit']}")
#
#
# @dp.message_handler(lambda message: message.text != "Рецепты" and condition==2)
# async def echo(message: types.Message):
#     ##
#     global user_input_state
#     user_input_state[message.from_user.id] = message.text
#     ##
#     user_input = get_user_input(message.from_user.id)
#     ##
#     data = recipe_api_request(user_input)
#     new_data = translater_data(data['hits'][0]['recipe']['ingredientLines'])
#     await message.answer_photo(photo=types.InputFile.from_url(data['hits'][0]['recipe']['image']))
#     await message.answer(f"{data['hits'][0]['recipe']['label']}\nКалории: {data['hits'][0]['recipe']['calories']},\nБелки: {data['hits'][0]['recipe']['totalNutrients']['PROCNT']['quantity']} {data['hits'][0]['recipe']['totalNutrients']['PROCNT']['unit']},\nЖиры: {data['hits'][0]['recipe']['totalNutrients']['FAT']['quantity']} {data['hits'][0]['recipe']['totalNutrients']['FAT']['unit']},\nУглеводы: {data['hits'][0]['recipe']['totalNutrients']['CHOCDF']['quantity']} {data['hits'][0]['recipe']['totalNutrients']['CHOCDF']['unit']},\nРецепт: {new_data}")


# @dp.message_handler(lambda message: message.text != "Калькулятор" and condition==3)
# async def echo(message: types.Message, state: FSMContext):
#     global user_input_state
#     user_input_state[message.from_user.id] = message.text
#     user_input = get_user_input(message.from_user.id)
#
#     try:
#         result_data = calc_calories(user_input)
#         await message.reply(f"Ваша базовая норма калорий в день: {result_data['bmr']}")
#         await message.answer(f"Белки - {result_data['proteins']} г, {result_data['proteins_cal']} ккал \n"
#                              f"Жиры - {result_data['fats']} г, {result_data['fats_cal']} ккал \n"
#                              f"Углеводы {result_data['carbohydrates']} г, {result_data['carbohydrates_cal']} ккал")
#     except IndexError:
#         await message.reply("Ошибка: неверный формат ввода данных.")
#     except ValueError:
#         await message.reply("Ошибка: некорректные числовые значения.")

@dp.message_handler(commands=['calc'])
async def start_calculator(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        gender = data.get('gender')
        age = data.get('age')
        weight = data.get('weight')
        height = data.get('height')
        activity = data.get('activity')

    if None in (gender, age, weight, height, activity):
        await message.reply("Ошибка: Не все данные для расчета калорий заполнены.")
        return

    user_input = f"{gender}, {age}, {weight}, {height}, {activity}"
    try:
        result_data = calc_calories(user_input)
        await message.reply(f"Ваша базовая норма калорий в день: {result_data['bmr']}")
        await message.answer(f"Белки - {result_data['proteins']} г, {result_data['proteins_cal']} ккал \n"
                                      f"Жиры - {result_data['fats']} г, {result_data['fats_cal']} ккал \n"
                                      f"Углеводы {result_data['carbohydrates']} г, {result_data['carbohydrates_cal']} ккал")
    except IndexError:
        await message.reply("Ошибка: Неверный формат ввода данных.")
    except ValueError:
        await message.reply("Ошибка: Некорректные числовые значения.")











def get_user_input(user_id):
    user_input = user_input_state.get(user_id, "")
    return user_input





if __name__ == '__main__':
    executor.start_polling(dp)

