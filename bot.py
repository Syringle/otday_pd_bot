import telebot
from telebot import types
from config import TOKEN
from handlers import start_handler, help_command, info_command, delete_user_command, change_color_command, language_handler
from database import init_db

bot = telebot.TeleBot(TOKEN)

# Создаем БД при запуске
init_db()

@bot.message_handler(commands=['start'])
def start(message):
    start_handler(message, bot)

@bot.message_handler(commands=['help'])
def help_command_handler(message):
    help_command(message, bot)

@bot.message_handler(commands=['info'])
def info_command_handler(message):
    info_command(message, bot)

@bot.message_handler(commands=['delete'])
def delete_user_handler(message):
    delete_user_command(message, bot)

@bot.message_handler(commands=['change_color'])
def change_color_handler(message):
    change_color_command(message, bot)

# Обработчик выбора языка
@bot.message_handler(func=lambda message: message.text in ["🇷🇺 Русский", "🇺🇿 O'zbek"])
def language_selection_handler(message):
    language_handler(message, bot)

# Обработчики кнопок
@bot.message_handler(func=lambda message: message.text.lower() in ['infoℹ', 'info'])
def info_button_handler(message):
    info_command(message, bot)

@bot.message_handler(func=lambda message: message.text.lower() in ['help🆘', 'help'])
def help_button_handler(message):
    help_command(message, bot)

@bot.message_handler(func=lambda message: message.text.lower() in ['delete🗑', 'delete'])
def delete_button_handler(message):
    delete_user_command(message, bot)

@bot.message_handler(func=lambda message: message.text.lower() in ['change_color✨', 'change_color'])
def change_color_button_handler(message):
    change_color_command(message, bot)

if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(none_stop=True)