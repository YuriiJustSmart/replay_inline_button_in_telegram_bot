import telebot
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

TOKEN = "8074901019:AAGm-JK-34rHJAb66WqlcDWXlQ7nSi0ztns"
bot = telebot.TeleBot(TOKEN)

# --- ФАКТИ ---

planets_facts = [
    "Юпітер вміщує понад 1300 Земель.",
    "На Венері день довший за рік.",
    "Марс має вулкан Олімп — найбільший у системі.",
    "Сатурн міг би плавати у воді.",
    "Уран обертається на боці.",
    "Нептун має найсильніші вітри.",
    "Меркурій не має атмосфери.",
    "Земля — єдина відома планета з життям.",
    "На Марсі були річки.",
    "Юпітер має гігантський шторм.",
    "Сатурн має кільця.",
    "Нептун відкрили математично.",
    "Венера дуже гаряча.",
    "Марс має 2 супутники.",
    "Юпітер має понад 90 супутників.",
    "Титан має атмосферу.",
    "Уран холодний.",
    "Меркурій має різкі температури.",
    "Земля має Місяць.",
    "Плутон більше не планета."
]

stars_facts = [
    "Сонце — 99,86% маси системи.",
    "Зірки народжуються в туманностях.",
    "Найближча — Проксима Центавра.",
    "Є зірки більші за Сонце.",
    "Живуть мільярди років.",
    "Колір = температура.",
    "Червоні холодніші.",
    "Сонце — жовтий карлик.",
    "Наднові — вибухи.",
    "Пульсари обертаються швидко.",
    "Є подвійні зірки.",
    "Нейтронні дуже щільні.",
    "Світло йде роками.",
    "Бачимо минуле.",
    "З водню.",
    "Сонце росте.",
    "Зірки вмирають.",
    "Білі карлики — залишки.",
    "Є гіганти.",
    "Є гіпергіганти."
]

black_holes_facts = [
    "Світло не виходить.",
    "Виникають після смерті зірок.",
    "Є в центрі галактики.",
    "Горизонт подій — межа.",
    "Ростуть.",
    "Зливаються.",
    "Час сповільнюється.",
    "Можуть бути мікро.",
    "Є диск навколо.",
    "Викривляють простір.",
    "Їх не видно.",
    "Знаходимо по ефекту.",
    "Є надмасивні.",
    "В центрах галактик.",
    "Можуть випаровуватись.",
    "Випромінювання Гокінга.",
    "Сильна гравітація.",
    "Поглинають зірки.",
    "Спагеттіфікація.",
    "Дуже загадкові."
]

# --- КЛАВІАТУРИ ---

def main_keyboard():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("🌌 Вибрати тему")
    keyboard.add("ℹ️ Інфо", "❓ Хелп")
    return keyboard


def topics_keyboard():
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🪐 Планети", callback_data="planets"),
        InlineKeyboardButton("⭐ Зорі", callback_data="stars"),
        InlineKeyboardButton("🕳 Чорні діри", callback_data="black_holes")
    )
    return keyboard


# --- START ---

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привіт! Обери дію 👇", reply_markup=main_keyboard())


# --- REPLY КНОПКИ ---

@bot.message_handler(func=lambda message: True)
def handle_buttons(message):

    if message.text == "🌌 Вибрати тему":
        bot.send_message(message.chat.id, "Обери тему:", reply_markup=topics_keyboard())

    elif message.text == "ℹ️ Інфо":
        bot.send_message(message.chat.id, "Бот про космос 🌌 Створений на уроці ❤️", reply_markup=main_keyboard())

    elif message.text == "❓ Хелп":
        bot.send_message(message.chat.id, "Натисни 'Вибрати тему', щоб отримати факт 🚀", reply_markup=main_keyboard())
    else:
        bot.send_message(
            message.chat.id,
            "Я не зрозумів 😅 Обери кнопку 👇",
            reply_markup=main_keyboard()
        )

# --- INLINE КНОПКИ + "ЩЕ ФАКТ" ---

@bot.callback_query_handler(func=lambda call: True)
def handle_topics(call):

    bot.answer_callback_query(call.id)

    # визначаємо тему
    if call.data in ["planets", "more_planets"]:
        fact = random.choice(planets_facts)
        topic = "planets"

    elif call.data in ["stars", "more_stars"]:
        fact = random.choice(stars_facts)
        topic = "stars"

    elif call.data in ["black_holes", "more_black_holes"]:
        fact = random.choice(black_holes_facts)
        topic = "black_holes"

    # кнопка "ще факт"
    keyboard = InlineKeyboardMarkup()
    keyboard.add(
        InlineKeyboardButton("🔁 Ще факт", callback_data=f"more_{topic}")
    )

    # редагуємо повідомлення
    topic_names = {
    "planets": "🪐 Планети",
    "stars": "⭐ Зорі",
    "black_holes": "🕳 Чорні діри"
    }

    try:
        bot.edit_message_text(
            f"{topic_names[topic]}\n\n🌠 {fact}",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=keyboard
        )
    except:
        pass


# --- ЗАПУСК ---

bot.polling()