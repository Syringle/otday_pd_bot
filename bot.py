import telebot
from config import TOKEN
from handlers import start_handler, name_handler, help_command, info_command, delete_user_command
from database import init_db, user_exists

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
def delete_command_handler(message):
    delete_user_command(message, bot)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if not user_exists(message.chat.id):  # Проверка на регистрацию
        name_handler(message, bot)

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    pass  # Обработку номера вызывает name_handler()

@bot.message_handler(content_types=['location'])
def handle_location(message):
    pass  # Обработку локации вызывает contact_handler()

if __name__ == "__main__":
    bot.polling(none_stop=True)
