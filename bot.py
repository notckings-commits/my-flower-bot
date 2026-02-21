import os
import logging
from flask import Flask
from threading import Thread
import telebot
from telebot import types

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")

TELEGRAM_TOKEN = "8367948448:AAFyOWDd5_ha-9iztPCuBCJiKkVXyS3BLko"

bot = telebot.TeleBot(TELEGRAM_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("🌷 Цветы")
    btn2 = types.KeyboardButton("🍰 Кондитерские изделия")
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, 
                     "Здравствуйте! Что вас интересует?", 
                     reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "🌷 Цветы")
def flowers(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("💰 Средняя стоимость")
    btn2 = types.KeyboardButton("📸 Отзывы")
    btn3 = types.KeyboardButton("🌸 Заказать букет")
    btn4 = types.KeyboardButton("🔙 В начало")
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(message.chat.id, 
                     "Вы выбрали цветы. Что хотите узнать?", 
                     reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "💰 Средняя стоимость")
def price(message):
    bot.send_message(message.chat.id, 
                     "💰 Цены:\n"
                     "Маленький букет - 1500₽\n"
                     "Средний букет - 2500₽\n"
                     "Большой букет - 3500₽")

@bot.message_handler(func=lambda message: message.text == "📸 Отзывы")
def reviews(message):
    bot.send_message(message.chat.id, "Скоро здесь будут фото отзывов")

@bot.message_handler(func=lambda message: message.text == "🌸 Заказать букет")
def order(message):
    bot.send_message(message.chat.id, 
                     "Для заказа напишите флористу: @florist_username")

@bot.message_handler(func=lambda message: message.text == "🔙 В начало")
def back_to_start(message):
    start(message)

app = Flask(__name__)

@app.route('/')
def home():
    return "Бот работает!"

@app.route('/health')
def health():
    return "OK"

def run_flask():
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 8080)))

if __name__ == "__main__":
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    logging.info("Бот запущен и работает на Render!")
    bot.infinity_polling()
