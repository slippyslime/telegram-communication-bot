from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = 'Введите токен своего бота'
ADMIN_ID = 123456788 #Введите свой admin_id

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Отправь мне сообщение, и я передам его администратору.")

async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    user_id = update.message.from_user.id

    await context.bot.send_message(chat_id=ADMIN_ID, text=f"Сообщение от {user_id}:\n{user_message}")
    await update.message.reply_text("Сообщение отправлено администратору!")

async def reply_to_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = int(context.args[0])
        reply_text = " ".join(context.args[1])

        await context.bot.send_message(chat_id=user_id, text=f"Ответ от администратора:\n{reply_text}")
        await update.message.reply_text("Ответ отправлен пользователю!")
    except (IndexError, ValueError):
        await update.message.reply_text("Использование: /reply <ID пользователя> <сообщение>")

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_admin))
    application.add_handler(CommandHandler("reply", reply_to_user, filters=filters.User(user_id=ADMIN_ID)))

    application.run_polling()

if __name__ == "__main__":
    main()