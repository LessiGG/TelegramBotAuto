from typing import Final, List
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InputMediaPhoto
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes, ConversationHandler, CallbackContext
from telegram.helpers import escape_markdown, mention_html
from telegram.constants import ParseMode
from datetime import datetime, timedelta

# Константы
TOKEN: Final = "7323246272:AAGjN9bG8oJ7k4pmpwEkuMvkG45w1hckg1I"
BOT_USERNAME: Final = "@prodetailing_bot"
GROUP_URL: Final = "https://t.me/+wOmoL3yiNecwNzcy"
AVITO_URL: Final = "https://www.avito.ru/user/9b2d77e21273b8fa19878c426d0536a0/profile?src=sharing"
OWNER_CHAT_ID: Final = "771810696"

# Клавиатуры
MAIN_MENU_KEYBOARD = [
    [InlineKeyboardButton("🛠 Выбор услуги", callback_data='services')],
    [InlineKeyboardButton("🛒 Авито", url=AVITO_URL)],
    [InlineKeyboardButton("⭐ Отзывы клиентов", url=GROUP_URL)],
    [InlineKeyboardButton("🔍 Информация о Нас", callback_data='info')],
    [InlineKeyboardButton("📞 Контакты", callback_data='contacts')]
]

SERVICES_KEYBOARD = [
    [KeyboardButton("🚘 Автосвет"), KeyboardButton("🥷 Оклеивание авто")],
    [KeyboardButton("🧽 Химчистка авто")],
    [KeyboardButton("👨‍💻 Консультация")],
    [KeyboardButton("↩️ Назад")]
]

BACK_KEYBOARD = [
    [KeyboardButton("↩️ Назад")]
]

# Словари с данными о светодиодных линзах
AUTO_LIGHTS = {
    "D9": "Светодиодные линзы Criline D9 Refractor",
    "D6": "Светодиодные линзы Criline D6 Inventor",
    "D5": "Светодиодные линзы Criline D5 Everbright",
    "D4": "Светодиодные линзы Criline D4 Night Ranger",
    "DK": "Светодиодные линзы Dragon Knight Double Direct",
    "H4B": "Мини Светодиодные линзы Criline H4 Premium Bright",
    "H4P": "Светодиодные линзы Criline H4 Premium Bright"
}

YOUTUBE_LINKS = {
    "D9": "https://www.youtube.com/watch?v=link_for_D9",
    "D6": "https://www.youtube.com/watch?v=link_for_D6",
    "D5": "https://www.youtube.com/watch?v=link_for_D5",
    "D4": "https://www.youtube.com/watch?v=link_for_D4",
    "DK": "https://www.youtube.com/watch?v=link_for_DK",
    "H4B": "https://www.youtube.com/watch?v=link_for_H4B",
    "H4P": "https://www.youtube.com/watch?v=link_for_H4P"
}

IMAGE_URLS = {
    "D9": ["https://express-china.ru/upload/iblock/091/uYAAAgJdAuA_960.jpg"],
    "D6": ["https://cdn2.criline.ru/assets/cache_image/products/11049/d6-01_800x800_bd3.png", "https://www.criline.ru/assets/images/products/11049/dop-d6-1.jpg"],
    "D5": ["https://express-china.ru/upload/iblock/091/uYAAAgJdAuA_960.jpg"],
    "D4": ["https://express-china.ru/upload/iblock/091/uYAAAgJdAuA_960.jpg"],
    "DK": ["https://express-china.ru/upload/iblock/091/uYAAAgJdAuA_960.jpg"],
    "H4B": ["https://express-china.ru/upload/iblock/091/uYAAAgJdAuA_960.jpg"],
    "H4P": ["https://express-china.ru/upload/iblock/091/uYAAAgJdAuA_960.jpg"]
}

BI_LED_MODULES = {
    "B1": "Bi-LED модуль Criline B1",
    "B2": "Bi-LED модуль Criline B2",
    "B3": "Bi-LED модуль Criline B3",
}

BI_LED_YOUTUBE_LINKS = {
    "B1": "https://www.youtube.com/watch?v=link_for_B1",
    "B2": "https://www.youtube.com/watch?v=link_for_B2",
    "B3": "https://www.youtube.com/watch?v=link_for_B3",
}

# Отображение названий услуг
SERVICE_NAMES = {
    'biled': 'Установка Bi-LED модулей',
    'glass_replacement': 'Замена стёкол',
    'polishing': 'Полировка и оклейка бронеплёнкой',
    'dehumidification': 'Устранение запотеваний',
    'led_modification': 'Доработка светодиодных фар',
    'okleivanie': 'Оклеивание авто',
    'chemclean': 'Химчистка авто'
}

# Состояния
SERVICE_SELECTION, GET_CAR_INFO, SCHEDULE_APPOINTMENT = range(3)

# Список игнорируемых команд
IGNORED_COMMANDS = {
    "🔍 Информация о Нас",
    "↩️ Назад",
    "🛠 Выбор услуги",
    "⭐ Отзывы клиентов",
    "🛒 Авито",
    "👨‍💻 Консультация",
    "🚘 Автосвет",
    "🥷 Оклеивание авто",
    "🧽 Химчистка авто"
}

def get_start_message() -> str:
    # Возвращает текст приветствия для стартового экрана.
    return (
        "Приветствую, дорогой покупатель!\n"
        "Через данного бота Вы сможете выбрать интересующий Вас раздел и записаться на услугу.\n\n"
        "Нажмите на кнопку ниже для управления ботом👇"
    )

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Получаем id чата
    user_id = update.message.from_user.id
    await update.message.reply_text(f"Ваш ID чата: {user_id}")

    # Обрабатывает команду /start
    welcome_text = get_start_message()
    reply_markup = InlineKeyboardMarkup(MAIN_MENU_KEYBOARD)
    await update.message.reply_text(welcome_text, reply_markup=reply_markup)

async def hide_keyboard(update: Update):
    # Скрывает стандартную клавиатуру.
    await update.message.reply_text(
        text="Возвращаемся назад.",
        reply_markup=ReplyKeyboardRemove()
    )

async def ask_for_car_info(update: Update, context: ContextTypes.DEFAULT_TYPE, service_name: str) -> int:
    # Просит ввести информацию о машине и номер телефона.
    message = update.callback_query.message if update.callback_query else update.message
    response = f"Введите марку вашей машины и номер телефона."
    context.user_data['service'] = service_name
    await message.reply_text(response)
    return GET_CAR_INFO

async def show_installation_dates(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Показывает доступные даты и время для записи на установку
    now = datetime.now()
    # Начинаем с завтрашнего дня
    start_date = now + timedelta(days=1)
    dates = [(start_date + timedelta(days=i)).strftime('%d-%m-%Y') for i in range(3)]
    times = ['12:00', '20:00']

    inline_keyboard = [
        [InlineKeyboardButton(f"{date} - {time}", callback_data=f"appointment_{date}_{time}")] 
        for date in dates for time in times
    ]
    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    
    message = update.message if update.message else update.callback_query.message
    await message.reply_text("Выберите удобное время для установки:", reply_markup=reply_markup)
    return SCHEDULE_APPOINTMENT

async def handle_appointment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # Обрабатывает выбор даты и времени для записи на установку
    query = update.callback_query
    await query.answer()

    appointment_details = query.data.split('_')[1:]  # Получаем дату и время из callback_data
    appointment_date, appointment_time = appointment_details
    
    user_info = context.user_data.get('car_info', 'Информация не предоставлена')
    service = context.user_data.get('service', 'Не указана услуга')

    response_message = (
        f"{mention_html(update.callback_query.from_user.id, update.callback_query.from_user.full_name)} выбрал время для установки:\n"
        f"Дата: {appointment_date}\n"
        f"Время: {appointment_time}\n\n"
        f"Информация о машине и номере телефона: {user_info}\n"
    )
    
    # Отправляем информацию главному
    await context.bot.send_message(chat_id=OWNER_CHAT_ID, text=response_message, parse_mode=ParseMode.HTML)
    
    # Подтверждаем пользователю
    await query.message.reply_text(f"Вы записаны на установку:\nДата: {appointment_date}\nВремя: {appointment_time}")
    
    return ConversationHandler.END

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Обрабатывает нажатия на инлайн-кнопки.
    query = update.callback_query
    await query.answer()
    
    callback_data = query.data
    response = ""
    reply_markup = None

    if callback_data == 'info':
        response = get_start_message()
        reply_markup = InlineKeyboardMarkup(MAIN_MENU_KEYBOARD)
        await query.message.reply_text(text=response, reply_markup=reply_markup)
    elif callback_data == 'services':
        response = "Выбор услуги:"
        reply_markup = ReplyKeyboardMarkup(SERVICES_KEYBOARD, resize_keyboard=True)
        await query.message.reply_text(text=response, reply_markup=reply_markup)
    elif callback_data == 'contacts':
        response = "Связь с нами:\n+7 (960) 706-94-08 \n (Ссылка на телеграм) \n (Ссылка на WhatsUp)"
        await query.message.reply_text(text=response, reply_markup=reply_markup)
        await query.message.reply_text("Нажмите '↩️ Назад' для возврата", reply_markup=ReplyKeyboardMarkup(BACK_KEYBOARD, resize_keyboard=True))
    elif callback_data == 'led_lenses':
        response = "Выбор установочного комплекта светодиодных линз:"
        inline_keyboard = [
            [InlineKeyboardButton(AUTO_LIGHTS[key], callback_data=key)] for key in AUTO_LIGHTS
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await query.message.reply_text(response, reply_markup=reply_markup)
    elif callback_data == 'biled':
        response = "Выбор установочного комплекта Bi-LED модулей:"
        inline_keyboard = [
            [InlineKeyboardButton(BI_LED_MODULES[key], callback_data=f"biled_{key}")] for key in BI_LED_MODULES
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await query.message.reply_text(response, reply_markup=reply_markup)
    elif callback_data.startswith('biled_'):
        module_key = callback_data.split('_')[1]
        response = f"Вы выбрали {BI_LED_MODULES[module_key]}"
        link = BI_LED_YOUTUBE_LINKS.get(module_key, "Ссылка не найдена")
        response += f"\nСсылка на видео: {link}"
        await query.message.reply_text(text=response)
        images = IMAGE_URLS.get(module_key, [])
        media_group = [InputMediaPhoto(media=url) for url in images]
        if media_group:
            await query.message.reply_media_group(media=media_group)
        return await ask_for_car_info(update, context, BI_LED_MODULES[module_key])
    elif callback_data in AUTO_LIGHTS:
        response = f"Вы выбрали {AUTO_LIGHTS[callback_data]}"
        link = YOUTUBE_LINKS.get(callback_data, "Ссылка не найдена")
        response += f"\nСсылка на видео: {link}"
        await query.message.reply_text(text=response)
        images = IMAGE_URLS.get(callback_data, [])
        media_group = [InputMediaPhoto(media=url) for url in images]
        if media_group:
            await query.message.reply_media_group(media=media_group)
        return await ask_for_car_info(update, context, 'Светодиодные линзы')
    elif callback_data == 'schedule_appointment':
        return await show_installation_dates(update, context)
    elif callback_data in SERVICE_NAMES:
        return await ask_for_car_info(update, context, SERVICE_NAMES[callback_data])
    else:
        response = "Вы выбрали услугу."
        reply_markup = ReplyKeyboardMarkup(SERVICES_KEYBOARD, resize_keyboard=True)
        await query.message.reply_text(text=response, reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text: str = update.message.text

    if 'service' in context.user_data:
        service = context.user_data.pop('service')
        car_info = escape_markdown(text)
        
        # Проверяем, что текст не совпадает с игнорируемыми командами
        if text in IGNORED_COMMANDS:
            await update.message.reply_text("Пожалуйста, введите марку вашей машины и номер телефона.")
            return
        
        context.user_data['car_info'] = car_info  # Сохраняем информацию о машине

        # Отправляем информацию владельцу
        response_message = (
            f"Марка машины и номер телефона:\n{car_info}\n\n"
            f"Услуга: {service}\n\n"
            f"Пользователь: {mention_html(update.message.from_user.id, update.message.from_user.first_name)}"
        )
        await context.bot.send_message(chat_id=OWNER_CHAT_ID, text=response_message, parse_mode=ParseMode.HTML)
        
        # Отправляем пользователю сообщение и кнопку записи на установку
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Записаться на установку", callback_data='schedule_appointment')]])
        await update.message.reply_text("Информация отправлена. Мы свяжемся с вами в ближайшее время. Нажмите на кнопку ниже, чтобы выбрать время для установки.", reply_markup=reply_markup)
        
        return ConversationHandler.END

    if text == "🔍 Информация о Нас":
        response = get_start_message()
        reply_markup = InlineKeyboardMarkup(MAIN_MENU_KEYBOARD)
        await update.message.reply_text(response, reply_markup=reply_markup)

    elif text == "↩️ Назад":
        await hide_keyboard(update)
        response = get_start_message()
        inline_keyboard = InlineKeyboardMarkup(MAIN_MENU_KEYBOARD)
        await update.message.reply_text(response, reply_markup=inline_keyboard)

    elif text == "🛠 Выбор услуги":
        response = "Выбор услуги:"
        reply_markup = ReplyKeyboardMarkup(SERVICES_KEYBOARD, resize_keyboard=True)
        await update.message.reply_text(response, reply_markup=reply_markup)

    elif text == "⭐ Отзывы клиентов":
        response = "Перейдите в наш канал: " + GROUP_URL
        await update.message.reply_text(response)

    elif text == "🛒 Авито":
        response = "Перейдите на наш профиль Авито: " + AVITO_URL
        await update.message.reply_text(response)

    elif text == "👨‍💻 Консультация":
        response = "За консультацией обратитесь к @Subarist_69"
        await update.message.reply_text(response)

    elif text == "🚘 Автосвет":
        response = "Выберите опцию автосвета:"
        inline_keyboard = [
            [InlineKeyboardButton("Светодиодные линзы", callback_data='led_lenses')],
            [InlineKeyboardButton("Установка Bi-LED модулей", callback_data='biled')],
            [InlineKeyboardButton("Замена стёкол", callback_data='glass_replacement')],
            [InlineKeyboardButton("Полировка и оклейка бронеплёнкой", callback_data='polishing')],
            [InlineKeyboardButton("Устранение запотеваний", callback_data='dehumidification')],
            [InlineKeyboardButton("Кастомизация фар", callback_data='led_modification')],
        ]
        reply_markup = InlineKeyboardMarkup(inline_keyboard)
        await update.message.reply_text(response, reply_markup=reply_markup)
    elif text == "🥷 Оклеивание авто":
        response = "Вы выбрали услугу оклеивания авто."
        context.user_data['service'] = SERVICE_NAMES['okleivanie']
        return await ask_for_car_info(update, context, SERVICE_NAMES['okleivanie'])
    elif text == "🧽 Химчистка авто":
        response = "Вы выбрали услугу химчистки авто."
        context.user_data['service'] = SERVICE_NAMES['chemclean']
        return await ask_for_car_info(update, context, SERVICE_NAMES['chemclean'])
    else:
        response = "Неизвестная команда, пожалуйста, выберите опцию."
        await update.message.reply_text(response)

def main():
    # Запуск бота.
    app = Application.builder().token(TOKEN).build()

    conversation_handler = ConversationHandler(
        entry_points=[
            CallbackQueryHandler(button_callback),
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
        ],
        states={
            GET_CAR_INFO: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message),
            ],
            SCHEDULE_APPOINTMENT: [
                CallbackQueryHandler(handle_appointment)
            ]
        },
        fallbacks=[],
    )

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(conversation_handler)

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
