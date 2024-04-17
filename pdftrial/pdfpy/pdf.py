import telegram
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

TOKEN = '7093953981:AAHjsCBSLaeyj6Xhg2bZDpJbsFEHBbZqkJA'

async def start_command(update: Update, context: telegram.ext.CallbackContext):
    await update.message.reply_text('Hello! Welcome to the certificate generator bot. Please enter your name.')

async def handle_name(update: Update, context: telegram.ext.CallbackContext):
    name = update.message.text
    await generate_certificate(name, update.message.chat_id, context.bot)

async def generate_certificate(name, chat_id, bot):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica", 24)
    c.drawString(100, 750, "Certificate of Achievement")
    c.setFont("Helvetica", 18)
    c.drawString(100, 700, f"This certificate is awarded to:")
    c.setFont("Helvetica-Bold", 36)
    c.drawString(100, 650, name)
    c.save()
    buffer.seek(0)
    await bot.send_document(chat_id=chat_id, document=buffer, filename=f"{name}_certificate.pdf")

async def error(update: Update, context: telegram.ext.CallbackContext):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(MessageHandler(filters. Regex(r'^[a-zA-Z ]+$'), handle_name))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling!')
    app.run_polling(poll_interval=10)  # Adjust the polling interval as needed.
