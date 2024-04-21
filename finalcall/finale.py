from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import telegram
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackContext,CallbackQueryHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from reportlab.lib.pagesizes import letter
from telegram import Update
from reportlab.pdfgen import canvas
import io
import datetime





from typing import Final
TOKEN: Final ='6908617554:AAGgsfvFZeZxtQtzm8_tYyjptkRxfmgx9nE'
BOT_USERNAME: Final ='@ghillithebot'

# Dictionary to store wallet information by Telegram user ID
wallets = {}

# Conversation states for /attest command
ATTENTION_ID, FROM_ADDRESS, TO_ADDRESS, BODY = range(4)

# Conversation states for /schema command
SCHE_NAME, SCHE_DESP,FIELD_NAME = range(3)

FIELD_TYPE, FIELD_VALUE = range(2, 4)


# Variables to store information for /attest command
attest_id = None
from_address_id = None
to_address_id = None
body = None

# Variables to store information for /schema command
schema_name = None
schema_desp = None
field_name=None


field_type = None# Variable to store the selected field type
field_value=None


# Variable to store the Telegram user ID
tele_id = None

start_datetime = None

# Dictionary to store whether the user has started and executed the wallet command
started_users = {}
wallet_executed = {}

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    started_users[user_id] = True
    await update.message.reply_text('Hey Im Ghilli here! Click /wallet or type wallet to view and check the balance of you wallet! ')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text( 'Im Ghilli and im here to attest your transcations into ETHSign with just Prompts! The Commands:\n/start- To start the bot\n/wallet- To view and check the balance of the wallet\n/attest- To attest the details\n/schema- To enter the schema details\n/viewall- To view all the transaction details\n/sticker- A free perk sticker')


async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command!')

async def get_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global tele_id
    tele_id = update.message.from_user.id
    await update.message.reply_text(f'Your Telegram ID is: {tele_id}')
    print( f'Telegram ID stored in variable: {tele_id}')  # Gabriel ,the telegram's id is store in the variable - "tele_id"


# /wallet command

async def wallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE): #Gabriel, this is summa temp wallet using python. Pass your original wallet here.
    user_id = update.message.from_user.id



    if user_id in wallets:
        wallet_address = wallets[user_id]['address']
        balance = wallets[user_id]['balance']
        await update.message.reply_text(f'Your Wallet Address: {wallet_address}\nYour Balance: {balance}')
        await update.message.reply_text( 'Now , Click /attest or type attest to view and check the balance of you wallet! ')

    else:
        # Simulate creating a wallet for demonstration
        new_wallet_address = "generated_wallet_address"
        new_balance = 0.0
        wallets[user_id] = {'address': new_wallet_address, 'balance': new_balance}
        await update.message.reply_text(f'Wallet created!\nWallet Address: {new_wallet_address}\nBalance: {new_balance}')
        await update.message.reply_text( 'Now , Click /attest or type attest to view and check the balance of you wallet! ')


    wallet_executed[user_id] = True

# /attest command
async def attest_command(update: Update, context: CallbackContext): # i have assigned each variable to each parameters like attestaion id and more.

    global start_datetime

    user_id = update.message.from_user.id
    global attest_id
    attest_id = None  # Initialize the variable here

    start_datetime = datetime.datetime.now()

    await update.message.reply_text('Please enter the Attestation ID:')
    return ATTENTION_ID

async def receive_attestation_id(update: Update, context: CallbackContext):
    global attest_id
    attest_id = update.message.text
    await update.message.reply_text('Enter From Address for the attestation:')
    return FROM_ADDRESS

async def receive_from_address(update: Update, context: CallbackContext):
    global from_address_id
    from_address_id = update.message.text
    await update.message.reply_text('Enter To Address for the attestation:')
    return TO_ADDRESS

async def receive_to_address(update: Update, context: CallbackContext):
    global to_address_id
    to_address_id = update.message.text
    await update.message.reply_text('Enter body:')
    return BODY

async def receive_body(update: Update, context: CallbackContext):
    global body
    body = update.message.text
    await update.message.reply_text('You have successfully entered your primary details. Click /schema or type schema to enter your schema details!')

    # Print the saved information
    print(f'Attestation ID: {attest_id}')
    print(f'From Address: {from_address_id}')
    print(f'To Address: {to_address_id}')
    print(f'Body: {body}')
    print(f'Time: {start_datetime}')




    return ConversationHandler.END

async def schema_command(update: Update, context: CallbackContext): # i have assigned each variable to each parameters like attestaion id and more.
    user_id = update.message.from_user.id
    global schema_name
    schema_name = None  # Initialize the variable here
    await update.message.reply_text('Please enter the Schema Name:')
    return SCHE_NAME

async def recieve_schema_name(update: Update, context: CallbackContext):
    global schema_name
    schema_name = update.message.text
    await update.message.reply_text('Please Enter Schema Decrpription:')
    return SCHE_DESP



async def recieve_schema_descp(update: Update, context: CallbackContext):
    global schema_desp
    schema_desp = update.message.text
    await update.message.reply_text('Enter Field Name:')
    return FIELD_NAME


async def recieve_field_name(update: Update, context: CallbackContext):
    global field_name
    field_name = update.message.text
    await update.message.reply_text('You have successfully entered the details. Click /viewall or type viewall to view your all details!')

async def viewall_command(update: Update, context: CallbackContext):  # i have assigned each variable to each parameters like attestaion id and more.
    user_id = update.message.from_user.id

    await update.message.reply_text('Transacation Details:')
    await update.message.reply_text(f'Attestation ID: {attest_id}')
    await update.message.reply_text(f'From Address: {from_address_id}')
    await update.message.reply_text(f'To Address: {to_address_id}')
    await update.message.reply_text(f'Schema Name: {schema_name}')
    await update.message.reply_text(f'Schema Descrption: {schema_desp}')
    await update.message.reply_text(f'Field Name: {field_name}')



    print(f'Schema Name: {schema_name}')
    print(f'Schema Description: {schema_desp}')
    print(f'Field Name: {field_name}')
    await generate_certificate(attest_id,from_address_id,to_address_id, schema_name,schema_desp, update.message.chat_id, context.bot)


async def generate_certificate(attest_id,from_address_id,to_address_id, schema_name,schema_desp, chat_id, bot):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    # Add background image
    background_path = 'ethsign.png'  # Replace with the path to your background image
    c.drawImage(background_path, 0, 0, width=letter[0], height=letter[1])

    # Add attestation and schema name to the certificate

    c.setFont("Helvetica", 18)
    c.setFillColorRGB(1, 0.5, 0)
    c.drawString(227, 540, f"{attest_id}")


    c.setFont("Helvetica", 18)
    c.setFillColorRGB(1, 1, 1)
    c.drawString(227, 475, f"{start_datetime}")

    # Add attestation and schema name to the certificate
    c.setFont("Helvetica", 18)
    c.setFillColorRGB(1, 1, 1)
    c.drawString(227, 400, f'{from_address_id}')

    # Add attestation and schema name to the certificate
    c.setFont("Helvetica", 18)
    c.setFillColorRGB(1, 1, 1)
    c.drawString(227, 330, f'{to_address_id}')


    c.setFont("Helvetica", 18)
    c.setFillColorRGB(1, 1, 1)
    c.drawString(227, 250, f"{schema_name}")

    c.setFont("Helvetica", 18)
    c.setFillColorRGB(1, 1, 1)
    c.drawString(227, 85, f"{schema_desp}")

    c.save()
    buffer.seek(0)
    await bot.send_document(chat_id=chat_id, document=buffer, filename="attestation_certificate.pdf")
    await bot.send_message(chat_id=chat_id, text="Thank you for attesting ETHSign! Click /sticker or type sticker for a perk sticker!")

async def sticker_command(update: Update, context: CallbackContext):
    # Send a photo in response to the /sticker command
    await update.message.reply_photo(photo=open('perksticker.png', 'rb'))



# Message handling
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}" ')

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = 'I do not understand what you wrote'
        else:
            return
    else:
        response: str = 'I do not understand what you wrote'


    print('Bot:', response)
    await update.message.reply_text(response)

async def error(update: Update, context: telegram.ext.CallbackContext):
    print(f'Update {update} caused error {context.error}')





if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('idn', get_id_command))  # Add this line for the /idn command
    app.add_handler(CommandHandler('wallet', wallet_command))
    app.add_handler(CommandHandler('viewall',viewall_command))# Add this line for the /wallet command
    app.add_handler(CommandHandler('gen', start_command))
    app.add_handler(CommandHandler('sticker', sticker_command))

    # Conversation handler for /attest command
    attest_handler = ConversationHandler(
        entry_points=[CommandHandler('attest', attest_command)],
        states={
            ATTENTION_ID: [MessageHandler(filters.TEXT, receive_attestation_id)],
            FROM_ADDRESS: [MessageHandler(filters.TEXT, receive_from_address)],
            TO_ADDRESS: [MessageHandler(filters.TEXT, receive_to_address)],
            BODY: [MessageHandler(filters.TEXT, receive_body)],
        },
        fallbacks=[],
    )
    app.add_handler(attest_handler)

    # Conversation handler for /schema command
    schema_handler = ConversationHandler(
        entry_points=[CommandHandler('schema', schema_command)],
        states={
            SCHE_NAME: [MessageHandler(filters.TEXT, recieve_schema_name)],
            SCHE_DESP: [MessageHandler(filters.TEXT, recieve_schema_descp)],
            FIELD_NAME: [MessageHandler(filters.TEXT, recieve_field_name)],


        },
        fallbacks=[],

    )
    app.add_handler(schema_handler)



    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling!')
    app.run_polling(poll_interval=10)