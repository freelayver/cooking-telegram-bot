import requests
from gpt import translater


# Установите ваш API-ключ
api_key = '9cd251c9a183f1d1d2726e244892f61b'

# URL-адрес и параметры запроса
url = 'https://api.edamam.com/api/recipes/v2'

params = {
    'type': 'public',
    'q': '',  # Замените KEYWORD на ваше ключевое слово
    'app_id': '77926405',  # Замените YOUR_APP_ID на ваш идентификатор приложения
    'app_key': api_key } # Используйте ваш API-ключ в качестве app_key

response = requests.get(url, params=params)


def recipe_api_request(user_input):
    global params
    params['q'] = translater(user_input)
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print('Произошла ошибка при запросе:', response.status_code)
        return None


#
# if response.status_code == 200:
#     data = response.json()
#     print(data['hits'][0])
#     print(data['hits'][0]['recipe']['label'])
#     print(data['hits'][0]['recipe']['image'])
# #     print('Калории:',data['hits'][0]['recipe']['calories'])
# #     print('Белки:', data['hits'][0]['recipe']['totalNutrients']['PROCNT']['quantity'], data['hits'][0]['recipe']['totalNutrients']['PROCNT']['unit'])
# #     print('Жиры:', data['hits'][0]['recipe']['totalNutrients']['FAT']['quantity'], data['hits'][0]['recipe']['totalNutrients']['FAT']['unit'])
# #     print('Углеводы:', data['hits'][0]['recipe']['totalNutrients']['CHOCDF']['quantity'], data['hits'][0]['recipe']['totalNutrients']['CHOCDF']['unit'])
# #     print(data['hits'][0]['recipe']['ingredientLines'])
#
#
# #Белки: {data['hits'][0]['recipe']['totalNutrients']['PROCNT']['quantity']} {data['hits'][0]['recipe']['totalNutrients']['PROCNT']['unit']},\nЖиры: {data['hits'][0]['recipe']['totalNutrients']['FAT']['quantity']} {data['hits'][0]['recipe']['totalNutrients']['FAT']['unit']},\nУглеводы: {data['hits'][0]['recipe']['totalNutrients']['CHOCDF']['quantity']} {data['hits'][0]['recipe']['totalNutrients']['CHOCDF']['unit']}
# else:
#     print('Произошла ошибка при запросе:', response.status_code)