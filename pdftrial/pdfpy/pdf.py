import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from reportlab.lib.pagesizes import letter
from telegram import Update
from reportlab.pdfgen import canvas
import io

TOKEN = '7093953981:AAHjsCBSLaeyj6Xhg2bZDpJbsFEHBbZqkJA'


async def start_command(update: Update, context: telegram.ext.CallbackContext):
    await update.message.reply_text('Hello! Im boost dappa like paal dappa. Please enter the attestation.')


async def handle_attestation(update: Update, context: telegram.ext.CallbackContext):
    context.user_data['attestation'] = update.message.text
    await update.message.reply_text('Please enter the transaction ID.')


async def handle_transaction_id(update: Update, context: telegram.ext.CallbackContext):
    attestation = context.user_data.get('attestation')
    transaction_id = update.message.text
    if attestation:
        await generate_certificate(attestation, transaction_id, update.message.chat_id, context.bot)
    else:
        await update.message.reply_text('Please enter the attestation first.')


async def generate_certificate(attestation, transaction_id, chat_id, bot):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Add background image
    background_path = 'ghilli.png'  # Replace with the path to your background image
    c.drawImage(background_path, 0, 0, width=letter[0], height=letter[1])

    # Add attestation to the certificate
    c.setFont("Helvetica", 18)
    c.drawString(100, 750, f"Attestation: {attestation}")

    # Add transaction ID to the certificate
    c.setFont("Helvetica", 18)
    c.drawString(100, 720, f"Transaction ID: {transaction_id}")

    c.save()
    buffer.seek(0)
    await bot.send_document(chat_id=chat_id, document=buffer, filename="attestation_bill.pdf")


async def error(update: Update, context: telegram.ext.CallbackContext):
    print(f'Update {update} caused error {context.error}')


if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(MessageHandler(filters.Regex(r'^[a-zA-Z ]+$'), handle_attestation))
    app.add_handler(MessageHandler(filters.Regex(r'^[a-zA-Z0-9]+$'), handle_transaction_id))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling!')
    app.run_polling(poll_interval=10)  # Adjust the polling interval as needed.
