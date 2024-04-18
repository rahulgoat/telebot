from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN: Final ='7093953981:AAHjsCBSLaeyj6Xhg2bZDpJbsFEHBbZqkJA'
BOT_USERNAME: Final ='@boostdappabot'

# Dictionary to store wallet information by Telegram user ID
wallets = {}

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hey BoostDappa here!')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Im gilli the bot<3, Please type smthg2 so that I can respond!')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command!')

async def get_id_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    await update.message.reply_text(f'Your Telegram ID is: {user_id}')

async def wallet_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

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

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Errors
    app.add_error_handler(error)

    # Polls the bot
    print('Polling!')
    app.run_polling(poll_interval=10)  # Polling interval set to 10 seconds
