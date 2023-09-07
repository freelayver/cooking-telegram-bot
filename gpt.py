import os
import openai
import openai

# Replace YOUR_API_KEY with your OpenAI API key
openai.api_key = "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"



def translater(user_input):
    # задаем модель и промпт
    model_engine = "text-davinci-003"
    prompt = f"Переведи на английский, без дополнительных коментариев: {user_input}"

    # задаем макс кол-во слов
    max_tokens = 128

    # генерируем ответ
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    # выводим ответ
    return completion.choices[0].text




def translater_data(data):
    # задаем модель и промпт
    model_engine = "text-davinci-003"
    prompt = f"Переведи на русский, без дополнительных коментариев и ответ дай в таком же формате: {data}"

    # задаем макс кол-во слов
    max_tokens = 128

    # генерируем ответ
    completion = openai.Completion.create(
        engine=model_engine,
        prompt=prompt,
        max_tokens=1024,
        temperature=0.5,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    # выводим ответ
    return completion.choices[0].text

