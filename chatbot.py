import telegram
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
import logging

# Встановлюємо рівень логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

# Будемо зберігати інформацію про користувачів у словнику
users = {}


# Функція для додавання користувача
def add_user(update, context):
    user = update.message.from_user
    if user.id not in users:
        users[user.id] = {'name': user.first_name, 'is_blocked': False}
        update.message.reply_text(f"{user.first_name}, Ви успішно зареєстровані.")
    else:
        update.message.reply_text("Ви вже зареєстровані.")


# Функція для блокування користувача
def block_user(update, context):
    user_id = int(context.args[0])
    if user_id in users:
        users[user_id]['is_blocked'] = True
        update.message.reply_text(f"{users[user_id]['name']} успішно заблокований.")
    else:
        update.message.reply_text("Користувача не знайдено.")


# Фунція для видалення користувача
def remove_user(update, context):
    user_id = int(context.args[0])
    if user_id in users:
        del users[user_id]
        update.message.reply_text("Користувача успішно видалено.")
    else:
        update.message.reply_text("Користувача не знайдено.")


# Функція для закріплення повідомлення
def pin_message(update, context):
    message_id = update.message.reply_to_message.message_id
    context.bot.pin_chat_message(chat_id=update.effective_chat.id, message_id=message_id)


# Функція для видалення повідомлення
def delete_message(update, context):
    message_id = update.message.reply_to_message.message_id
    context.bot.delete_message(chat_id=update.effective_chat.id, message_id=message_id)


# Функція для отримання id користувача
def get_user_id(update, context):
    user = update.message.from_user
    update.message.reply_text(f"Ваш id: {user.id}")


# Функція для обробки текстових повідомлень
def handle_text(update, context):
    user_id = update.message.from_user.id
    if user_id in users and not users[user_id]['is_blocked']:
        # Якщо користувач зареєстрований і не заблокований, то можна обробити повідомлення
        text = update.message.text
        # TODO: Обробити текстове повідомлення
        pass
    else:
        update.message.reply_text("Ви не можете користуватись ботом.")


# Функція-обробник для команди /start
def start(update, context):
    update.message.reply_text('Вітаю! Це чат-бот, який допоможе Вам контролювати користувачів.')


# Функція-обробник для команди /help
def help(update, context):
    update.message.reply_text('Список команд:\n'
                              '/add_user - зареєструвати користувача\n'
                              '/block_user  - заблокувати користувача\n'
                              '/remove_user  - видалити користувача\n'
                              '/pin_message - закріпити повідомлення\n'
                              '/delete_message - видалити повідомлення, що закріплене\n'
                              '/get_user_id - дізнатись Ваш id')


# Функція main, яка запускає бота
def main():
    # Зчитуємо токен бота з файлу
    with open("token.txt", "r") as f:
        token = f.read().strip()

    # Створюємо екземпляр бота
    bot = telegram.Bot(token=token)

    # Створюємо екземпляр для спілкування з серверами Telegram
    updater = Updater(token, use_context=True)

    # Створюємо обробник повідомлень типу текст
    text_handler = MessageHandler(Filters.text & (~Filters.command), handle_text)

    # Додаємо обробник для команди /add_user
    updater.dispatcher.add_handler(CommandHandler('add_user', add_user))
    
    # Додаємо обробник для команди /block_user
    updater.dispatcher.add_handler(CommandHandler('block_user', block_user, pass_args=True))

    # Додаємо обробник для команди /remove_user
    updater.dispatcher.add_handler(CommandHandler('remove_user', remove_user, pass_args=True))

    # Додаємо обробник для команди /pin_message
    updater.dispatcher.add_handler(CommandHandler('pin_message', pin_message))

    # Додаємо обробник для команди /delete_message
    updater.dispatcher.add_handler(CommandHandler('delete_message', delete_message))

    # Додаємо обробник для команди /get_user_id
    updater.dispatcher.add_handler(CommandHandler('get_user_id', get_user_id))

    # Додаємо обробник для команди /start
    updater.dispatcher.add_handler(CommandHandler('start', start))

    # Додаємо обробник для команди /help
    updater.dispatcher.add_handler(CommandHandler('help', help))

    # Додаємо обробник повідомлень типу текст
    updater.dispatcher.add_handler(text_handler)

    # Запустимо бота
    updater.start_polling()

    # Щоб бот не зупинявся, він буде працювати, поки не натиснути Ctrl-C
    updater.idle()


if __name__ == '__main__':
    main()
