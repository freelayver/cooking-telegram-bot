import requests
from gpt import translater



# Установите ваш API-ключ
api_key = '18b94f32bc0c7d07eab2b11cef8009f5'

# URL-адрес и параметры запроса
url = 'https://api.edamam.com/api/nutrition-data'

params = {
    'ingr': '',  # Замените KEYWORD на ваше ключевое слово
    'app_id': '19160ba2',  # Замените YOUR_APP_ID на ваш идентификатор приложения
    'app_key': api_key  # Используйте ваш API-ключ в качестве app_key
}


# Отправьте GET-запрос
response = requests.get(url, params=params)

# # Проверка статуса ответа
# if response.status_code == 200:
#     # Обработка успешного ответа
#     data = response.json()
#     # Ваши дальнейшие действия с полученными данными
#     print(data)
# else:
#     # Обработка ошибки
#     print('Произошла ошибка при запросе:', response.status_code)


def make_api_request(user_input):
    global params
    params['ingr'] = translater(user_input)
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print('Произошла ошибка при запросе:', response.status_code)
        return None