from aiogram import Bot, Dispatcher, executor, types

TEXT_MENU = """
<b>/калькулятор</b> - <em>Калькулятор каллорий</em>.
"""

TEXT_CALC = """
Привет! Напишите мне:

— ваш пол (М/Ж), 
— возраст, 
— вес, 
— рост 
— активность (сидячий/активный)

В формате: М, 25, 70, 180, активный

Один из способов расчета нормы калорий - формула Харриса-Бенедикта. 

С ее помощью можно рассчитать базальную скорость метаболизма, 
а именно количество калорий (энергии), 
необходимых для правильного функционирования организма.
"""

TEXT_CALC_ERROR = """
<em>Ошибка в вводе данных. Пожалуйста, введите данные в формате:</em> <b>М, 25, 70, 180, активный</b>
"""

TEXT_SITE = """
<em>Тут будет ссылка.</em>
"""




# async def send_calc(message: types.Message):
#     await message.answer(text=TEXT_CALC)
#     await message.delete()

go = "М, 25, 70, 180, активный"

def calc_calories(user_input):
    data = user_input.split(', ')
    gender = data[0]
    age = int(data[1])
    weight = float(data[2])
    height = int(data[3])
    activ = data[4]
    bjugender = 0
    proteins = 0
    fats = 0
    carbohydrates = 0
    bmr = 0

    if activ.lower() == 'сидячий':
        activ = 1.2
    elif activ.lower() == 'активный':
        activ = 1.4

    if gender.lower() == 'мужчина':
        bmr = round((88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)) * activ)
        bjugender = 1
    elif gender.lower() == 'женщина':
        bmr = round((447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)) * activ)
        bjugender = 2

    if activ == 1.2 and bjugender == 1:
        proteins = round(1.5 * weight)
        fats = round(1 * weight)
        carbohydrates = round(2.6 * weight)
    elif activ == 1.4 and bjugender == 1:
        proteins = round(1.5 * weight)
        fats = round(1 * weight)
        carbohydrates = round(3.6 * weight)

    if activ == 1.2 and bjugender == 2:
        proteins = round(1.5 * weight)
        fats = round(1 * weight)
        carbohydrates = round(1.8 * weight)
    elif activ == 1.4 and bjugender == 2:
        proteins = round(1.5 * weight)
        fats = round(1 * weight)
        carbohydrates = round(2.7 * weight)

    proteins_cal = round(proteins * 4)
    fats_cal = round(fats * 9)
    carbohydrates_cal = round(carbohydrates * 4)

    result = {
        'bmr': bmr,
        'proteins': proteins,
        'proteins_cal': proteins_cal,
        'fats': fats,
        'fats_cal': fats_cal,
        'carbohydrates': carbohydrates,
        'carbohydrates_cal': carbohydrates_cal
    }
    return result



            # await message.reply(f"Ваша базовая норма калорий в день: {bmr}")
            # await message.answer(f"Белки - {proteins} г, {proteins_cal} ккал \n"
            #                      f"Жиры - {fats} г, {fats_cal} ккал \n"
            #                      f"Углеводы {carbohydrates} г, {carbohydrates_cal} ккал")



result_data = calc_calories(go)



# def register_calc_command(dp : Dispatcher):
#     dp.register_message_handler(send_calc, commands=['калькулятор'])




