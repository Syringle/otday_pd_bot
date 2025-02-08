import telebot
from telebot import types
from database import add_user, user_exists, delete_user


def start_handler(message, bot):
    """Обрабатывает команду /start"""
    chat_id = message.chat.id
    user_name = message.from_user.first_name

    if user_exists(chat_id):
        # Если пользователь уже зарегистрирован, выводим кнопки
        keyboard = get_command_keyboard()
        bot.send_message(chat_id, f"Привет, {user_name}! Ты уже зарегистрирован.", reply_markup=keyboard)
    else:
        # Если не зарегистрирован, запрашиваем имя
        bot.send_message(chat_id, f"Привет, {user_name}! Давай зарегистрируемся. Введи свое имя:")


def name_handler(message, bot):
    """Обрабатывает ввод имени пользователя"""
    chat_id = message.chat.id
    user_name = message.text

    # Запрашиваем номер телефона
    bot.send_message(chat_id, "Отлично! Введи свой номер телефона:", reply_markup=get_contact_keyboard())

    # Сохраняем имя пользователя
    bot.register_next_step_handler(message, lambda msg: phone_handler(msg, bot, user_name))


def phone_handler(message, bot, user_name):
    """Обрабатывает ввод номера телефона"""
    chat_id = message.chat.id

    if message.contact:
        phone = message.contact.phone_number
    else:
        phone = message.text  # Если номер не был отправлен как контакт

    # Запрашиваем любимый цвет
    bot.send_message(chat_id, "Какой твой любимый цвет?", reply_markup=get_color_keyboard())

    # Сохраняем имя пользователя и номер телефона
    bot.register_next_step_handler(message, lambda msg: color_handler(msg, bot, user_name, phone))


def color_handler(message, bot, user_name, phone):
    """Обрабатывает выбор цвета"""
    chat_id = message.chat.id
    favorite_color = message.text

    # Сохраняем данные о пользователе в базе данных
    add_user(chat_id, user_name, phone, None, None, favorite_color)

    # Подтверждение о сохранении данных
    bot.send_message(chat_id, "Ваши данные успешно сохранены!")

    # Сообщаем пользователю о завершении регистрации
    bot.send_message(chat_id, f"Регистрация завершена! Твой любимый цвет: {favorite_color}.")

    # Отправляем кнопки с командами
    keyboard = get_command_keyboard()
    bot.send_message(chat_id, "Вот команды, которые ты можешь использовать:", reply_markup=keyboard)


def get_command_keyboard():
    """Создает клавиатуру с командами"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("/help"))
    keyboard.add(types.KeyboardButton("/info"))
    keyboard.add(types.KeyboardButton("/delete"))  # Кнопка для удаления пользователя
    return keyboard


def get_color_keyboard():
    """Создает клавиатуру с цветами"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    colors = ["🔴 Красный", "🟠 Оранжевый", "🟡 Желтый", "🟢 Зеленый", "🔵 Синий", "🟣 Фиолетовый", "⚫ Черный"]
    keyboard.add(*colors)
    return keyboard


def get_contact_keyboard():
    """Создает клавиатуру для отправки контакта"""
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_contact = types.KeyboardButton("Поделиться номером", request_contact=True)
    keyboard.add(button_contact)
    return keyboard


def help_command(message, bot):
    """Обрабатывает команду /help"""
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     "Это простой Телеграм бот. Вы можете взаимодействовать с ним, используя доступные команды.")


def info_command(message, bot):
    """Обрабатывает команду /info"""
    chat_id = message.chat.id
    bot.send_message(chat_id,
                     "Информация о боте: здесь вы можете зарегистрироваться и получать информацию о своем любимом цвете!")


def delete_user_command(message, bot):
    """Обрабатывает команду удаления пользователя"""
    chat_id = message.chat.id

    if user_exists(chat_id):
        delete_user(chat_id)
        bot.send_message(chat_id, "Вы успешно удалены из базы данных. Вы можете зарегистрироваться заново.")

        # Отправляем кнопку "Старт"
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start_button = types.KeyboardButton("/start")
        keyboard.add(start_button)
        bot.send_message(chat_id, "Нажмите кнопку ниже, чтобы начать регистрацию:", reply_markup=keyboard)
    else:
        bot.send_message(chat_id, "Вы не зарегистрированы.")
