from pyrogram import Client, filters
import sqlite3
import os

api_id = "YOU_API_ID"
api_hash = "YOU_API_HASH"
bot_token = "YOU_BOT_TOKEN"
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_name = os.path.join(BASE_DIR, 'data.db')
conn = sqlite3.connect(db_name, check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT, chat_id INTEGER)''')
conn.commit()

def save_user_info(name, chat_id):
    cursor.execute('INSERT INTO users(name, chat_id) VALUES(?, ?)', (name, chat_id))
    conn.commit()


@app.on_message(filters.command("start"))
def send_welcome(client, message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    chat_id = message.chat.id
    save_user_info(user_name, chat_id)

    welcome_text = (
        "Просто укажите номер телефона или ник нейм, в ответ получите ID Telegram. "
        "Формат телефона любой, ник с символа @. Пример +77778087076 или @exuser.\n"
        "Администратор\n"
        "Xabber: bufonidae@jabber.ru\n"
        "Email: sizam1@protonmail.com\n"
        f"Кстати, Ваш TG ID {user_id}"
    )
    message.reply_text(welcome_text)


@app.on_message(filters.text)
def get_user_id(client, message):
    input_data = message.text
    if input_data.startswith('@') or input_data.startswith('https://t.me/'):
        if input_data.startswith('@'):
            username = input_data[1:]
        elif input_data.startswith('https://t.me/'):
            username = input_data.split('/')[-1]

        try:
            user = client.get_users(username)
            message.reply_text(f"ID пользователя: {user.id}")
        except Exception as e:
            message.reply_text(f"Не удалось получить ID для {username}. Ошибка: {e}")

    else:
        message.reply_text("Пожалуйста, укажите правильный номер телефона или ник нейм.")


app.run()
