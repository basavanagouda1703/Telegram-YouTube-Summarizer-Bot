from telegram.ext import ApplicationBuilder, MessageHandler, filters, CommandHandler
from config import BOT_TOKEN
from handlers.message_handler import (
    handle_message,
    handle_summary_command,
    handle_deepdive_command,
)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("summary", handle_summary_command))
app.add_handler(CommandHandler("deepdive", handle_deepdive_command))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()