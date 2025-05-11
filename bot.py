import os
import telebot
import requests
from flask import Flask, request

# Переменные окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("AI_TOKEN")

# Настройки
MODEL = 'openai/gpt-3.5-turbo'
OPENROUTER_API_URL = 'https://openrouter.ai/api/v1/chat/completions'

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

# Установить webhook при запуске (делается один раз)
WEBHOOK_URL = f"https://tolikaibot.onrender.com/{BOT_TOKEN}"

# Удаляем старые вебхуки и устанавливаем новый
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

# Главная страница (для проверки)
@app.route("/", methods=["GET"])
def index():
    return "Бот работает!"

# Webhook обработчик
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    json_data = request.get_json()
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "ok", 200

# Команда /start
@bot.message_handler(commands=['start'])
def send_start(message):
    bot.reply_to(message, "Здравствуйте, это ИИ-бот от @tolik_scripter. Чем я могу вам помочь?")

# Команда /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Напишите любой вопрос или текст — и я постараюсь вам ответить с помощью искусственного интеллекта!")

# Ответ на обычные сообщения
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    prompt = message.text
    response = get_openrouter_response(prompt)
    bot.reply_to(message, response)

# Функция для получения ответа от OpenRouter
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
        res = requests.post(OPENROUTER_API_URL, headers=headers, json=data)
        res.raise_for_status()
        return res.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Ошибка: {e}"

# Запуск приложения
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
