import telebot
from telebot import types
from database import get_user_info, delete_user, update_user_color, user_exists, add_user, update_user_language, get_user_language

LANGUAGES = {
    'ru': {
        'greeting': "Привет! Давай зарегистрируемся. Введи свое имя:",
        'confirm_registration': "Ваши данные успешно сохранены!",
        'choose_color': "Какой твой любимый цвет?",
        'help_text': "Команды: /start - начать регистрацию, /delete - удалить пользователя.",
        'info_text': "Информация о вас:",
        'user_info': "Ваши данные:\nИмя: {}\nТелефон: {}\nЦвет: {}",
        'start_over': "Вы успешно удалены. Зарегистрируйтесь заново.",
        'change_color': "Выберите новый цвет:",
        'change_color_success': "Цвет успешно изменен!",
        'choose_language': "Выберите язык:\n🇷🇺 Русский\n🇺🇿 O'zbek"
    },
    'uz': {
        'greeting': "Salom! Ro'yxatdan o'tamiz. Ismingizni kiriting:",
        'confirm_registration': "Ma'lumotlaringiz muvaffaqiyatli saqlandi!",
        'choose_color': "Sevimli rangingizni tanlang:",
        'help_text': "Buyruqlar: /start - ro'yxatdan o'tish, /delete - foydalanuvchini o'chirish.",
        'info_text': "Siz haqingizda ma'lumot:",
        'user_info': "Sizning ma'lumotlaringiz:\nIsm: {}\nTelefon: {}\nRang: {}",
        'start_over': "Siz muvaffaqiyatli o'chirildingiz. Yangi ro'yxatdan o'ting.",
        'change_color': "Yangi rangni tanlang:",
        'change_color_success': "Rang muvaffaqiyatli o'zgartirildi!",
        'choose_language': "Tilni tanlang:\n🇷🇺 Русский\n🇺🇿 O'zbek"
    }
}

def language_handler(message, bot):
    chat_id = message.chat.id
    selected_language = 'ru' if message.text == "🇷🇺 Русский" else 'uz'
    update_user_language(chat_id, selected_language)
    bot.send_message(chat_id, LANGUAGES[selected_language]['greeting'])
    bot.register_next_step_handler(message, lambda msg: name_handler(msg, bot, selected_language))

def start_handler(message, bot):
    chat_id = message.chat.id
    bot.send_message(chat_id, LANGUAGES['ru']['choose_language'], reply_markup=get_language_keyboard())

def name_handler(message, bot, language):
    chat_id = message.chat.id
    user_name = message.text
    bot.send_message(chat_id, "Введите номер телефона:", reply_markup=get_contact_keyboard())
    bot.register_next_step_handler(message, lambda msg: phone_handler(msg, bot, user_name, language))

def phone_handler(message, bot, user_name, language):
    chat_id = message.chat.id
    phone = message.contact.phone_number if message.contact else message.text
    bot.send_message(chat_id, LANGUAGES[language]['choose_color'], reply_markup=get_color_keyboard())
    bot.register_next_step_handler(message, lambda msg: color_handler(msg, bot, user_name, phone, language))

def color_handler(message, bot, user_name, phone, language):
    chat_id = message.chat.id
    favorite_color = message.text
    add_user(chat_id, user_name, phone, favorite_color, language)
    bot.send_message(chat_id, LANGUAGES[language]['confirm_registration'], reply_markup=get_command_keyboard(language))

def get_command_keyboard(language='ru'):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("infoℹ", "help🆘", "delete🗑", "change_color✨")
    return keyboard

def get_language_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("🇷🇺 Русский", "🇺🇿 O'zbek")
    return keyboard

def get_color_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    colors = ["🔴 Красный", "🟠 Оранжевый", "🟡 Желтый", "🟢 Зеленый", "🔵 Синий", "🟣 Фиолетовый", "⚫ Черный"]
    keyboard.add(*[types.KeyboardButton(color) for color in colors])
    return keyboard

def get_contact_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("Поделиться номером", request_contact=True))
    return keyboard

def help_command(message, bot):
    chat_id = message.chat.id
    language = get_user_language(chat_id)
    bot.send_message(chat_id, LANGUAGES[language]['help_text'], reply_markup=get_command_keyboard(language))

def info_command(message, bot):
    chat_id = message.chat.id
    language = get_user_language(chat_id)
    user_data = get_user_info(chat_id)
    if user_data:
        bot.send_message(
            chat_id,
            LANGUAGES[language]['user_info'].format(user_data[0], user_data[1], user_data[2]),
            reply_markup=get_command_keyboard(language)
        )
    else:
        bot.send_message(chat_id, "Вы не зарегистрированы.", reply_markup=get_command_keyboard(language))

def delete_user_command(message, bot):
    chat_id = message.chat.id
    language = get_user_language(chat_id)
    if user_exists(chat_id):
        delete_user(chat_id)
        bot.send_message(chat_id, LANGUAGES[language]['start_over'], reply_markup=get_command_keyboard(language))
    else:
        bot.send_message(chat_id, "Вы не зарегистрированы.", reply_markup=get_command_keyboard(language))

def change_color_command(message, bot):
    chat_id = message.chat.id
    language = get_user_language(chat_id)
    if user_exists(chat_id):
        bot.send_message(chat_id, LANGUAGES[language]['change_color'], reply_markup=get_color_keyboard())
        bot.register_next_step_handler(message, lambda msg: update_color(msg, bot, chat_id, language))
    else:
        bot.send_message(chat_id, "Вы не зарегистрированы.", reply_markup=get_command_keyboard(language))

def update_color(message, bot, chat_id, language):
    update_user_color(chat_id, message.text)
    bot.send_message(chat_id, LANGUAGES[language]['change_color_success'], reply_markup=get_command_keyboard(language))
