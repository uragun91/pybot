import random

from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import requests

WEATHER_MAP_KEY = 'c13cf6b1f039dd343050cb65dbb36e47'


def get_weather_in_ny():
    url = f"http://api.openweathermap.org/data/2.5/weather?q=New York&appid={WEATHER_MAP_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()

    if data.get("cod") != 200:
        return f"Не удалось получить данные о погоде.{data}"

    weather = data["weather"][0]["description"]
    temp = data["main"]["temp"]
    return f"Погода в Нью-Йорке: {weather}, температура: {temp}°C /n {data}"


def get_random_photo():
    # Используем Unsplash для получения случайного фото
    random_param = random.randint(1, 100)
    print(random_param)
    return  f"https://source.unsplash.com/random?{random_param}"

def get_random_fact():
    # Используем API для получения случайного факта
    response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
    data = response.json()
    return data["text"]

async def start(update: Update, context: CallbackContext):
    # Создаем клавиатуру с 4 кнопками
    keyboard = [
        ['Погода в Нью-Йорке', 'Повторить текст'],
        ['Получить фото', 'Случайный факт']
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Выберите действие:", reply_markup=reply_markup)


# Обработчик текстовых сообщений
async def handle_message(update: Update, context: CallbackContext):
    text = update.message.text

    if text == 'Погода в Нью-Йорке':
        weather = get_weather_in_ny()
        await update.message.reply_text(weather)
    elif text == 'Повторить текст':
        await update.message.reply_text("Вы нажали на вторую кнопку!")
    elif text == 'Получить фото':
        photo_url = get_random_photo()
        await update.message.reply_photo(photo_url)
    elif text == 'Случайный факт':
        fact = get_random_fact()
        await update.message.reply_text(fact)
    else:
        await update.message.reply_text(f"Вы написали ")

token = '8059138708:AAGabHJATgKBGbtxtV9d5OYleiQNX6M6HpE'
# Основная функция
def main():
    application = Application.builder().token(token).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
