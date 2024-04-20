from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler, CallbackContext

TOKEN: Final ='7093953981:AAHjsCBSLaeyj6Xhg2bZDpJbsFEHBbZqk'
BOT_USERNAME: Final ='@boostdappabot'

# Dictionary to store wallet information by Telegram user ID
wallets = {}

# Conversation states for /attest command
ATTENTION_ID, FROM_ADDRESS, TO_ADDRESS, BODY = range(4)

# Variables to store information for /attest command
attest_id = None
from_address_id = None
to_address_id = None
body = None

# Variable to store the Telegram user ID
tele_id = None

# Dictionary to store whether the user has started and executed the wallet command
started_users = {}
wallet_executed = {}

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    started_users[user_id] = True
    await update.message.reply_text('Hey BoostDappa here!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Im BoostDappa and im here to attest your transcations into ETHSign with just Prompts!')

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

    if user_id not in started_users or not started_users[user_id]:
        await update.message.reply_text('Please start the bot first using /start command.')
        return

    if user_id in wallets:
        wallet_address = wallets[user_id]['address']
        balance = wallets[user_id]['balance']
        await update.message.reply_text(f'Your Wallet Address: {wallet_address}\nYour Balance: {balance}')
    else:
        # Simulate creating a wallet for demonstration
        new_wallet_address = "generated_wallet_address"
        new_balance = 0.0
        wallets[user_id] = {'address': new_wallet_address, 'balance': new_balance}
        await update.message.reply_text(f'Wallet created!\nWallet Address: {new_wallet_address}\nBalance: {new_balance}')

    wallet_executed[user_id] = True

# /attest command
async def attest_command(update: Update, context: CallbackContext): # i have assigned each variable to each parameters like attestaion id and more.
    user_id = update.message.from_user.id

    if user_id not in wallet_executed or not wallet_executed[user_id]:
        await update.message.reply_text('Please execute /wallet command first.')
        return

    global attest_id
    attest_id = None  # Initialize the variable here
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
    await update.message.reply_text('Succesfully attested in ETHSign!')

    # Print the saved information
    print(f'Attestation ID: {attest_id}')
    print(f'From Address: {from_address_id}')
    print(f'To Address: {to_address_id}')
    print(f'Body: {body}')




    return ConversationHandler.END

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

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))
    app.add_handler(CommandHandler('idn', get_id_command))  # Add this line for the /idn command
    app.add_handler(CommandHandler('wallet', wallet_command))  # Add this line for the /wallet command

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

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling!')
    app.run_polling(poll_interval=10)  # Polling interval set to 10 seconds
