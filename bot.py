import telebot
import requests

# Токен твоего Telegram-бота
TELEGRAM_TOKEN = '7645148498:AAEwd7wAm4uWVfwdqCi3Fl7_-rSoBikUNWU'
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# Настройки OpenRouter API
OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions'
OPENROUTER_API_KEY = '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'

# Модель по умолчанию
MODEL = 'openai/gpt-3.5-turbo'

# Ответ на /start
@bot.message_handler(commands=['start'])
def send_start(message):
    bot.reply_to(message, "Здравствуйте, это ИИ-бот от @tolik_scripter. Чем я могу вам помочь?")

# Ответ на /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Напишите любой вопрос или текст — и я постараюсь вам ответить с помощью искусственного интеллекта!")

# Обработка всех остальных сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text
    response = get_openrouter_response(user_input)
    bot.reply_to(message, response)

# Получение ответа от OpenRouter
def get_openrouter_response(prompt):
    headers = {
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"Ошибка при запросе: {e}"

# Запуск бота
bot.polling()
