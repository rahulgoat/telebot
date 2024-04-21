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

from dotenv import load_dotenv

import os
from web3 import Web3, constants
from supabase import create_client
import json


load_dotenv()

abi=[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"address","name":"target","type":"address"}],"name":"AddressEmptyCode","type":"error"},{"inputs":[],"name":"AttestationAlreadyRevoked","type":"error"},{"inputs":[],"name":"AttestationInvalidDuration","type":"error"},{"inputs":[],"name":"AttestationIrrevocable","type":"error"},{"inputs":[],"name":"AttestationNonexistent","type":"error"},{"inputs":[],"name":"AttestationWrongAttester","type":"error"},{"inputs":[{"internalType":"address","name":"implementation","type":"address"}],"name":"ERC1967InvalidImplementation","type":"error"},{"inputs":[],"name":"ERC1967NonPayable","type":"error"},{"inputs":[],"name":"FailedInnerCall","type":"error"},{"inputs":[],"name":"InvalidDelegateSignature","type":"error"},{"inputs":[],"name":"InvalidInitialization","type":"error"},{"inputs":[],"name":"LegacySPRequired","type":"error"},{"inputs":[],"name":"NotInitializing","type":"error"},{"inputs":[],"name":"OffchainAttestationAlreadyRevoked","type":"error"},{"inputs":[],"name":"OffchainAttestationExists","type":"error"},{"inputs":[],"name":"OffchainAttestationNonexistent","type":"error"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"OwnableInvalidOwner","type":"error"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"OwnableUnauthorizedAccount","type":"error"},{"inputs":[],"name":"Paused","type":"error"},{"inputs":[],"name":"SchemaNonexistent","type":"error"},{"inputs":[],"name":"SchemaWrongRegistrant","type":"error"},{"inputs":[],"name":"UUPSUnauthorizedCallContext","type":"error"},{"inputs":[{"internalType":"bytes32","name":"slot","type":"bytes32"}],"name":"UUPSUnsupportedProxiableUUID","type":"error"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint64","name":"attestationId","type":"uint64"},{"indexed":False,"internalType":"string","name":"indexingKey","type":"string"}],"name":"AttestationMade","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint64","name":"attestationId","type":"uint64"},{"indexed":False,"internalType":"string","name":"reason","type":"string"}],"name":"AttestationRevoked","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint64","name":"version","type":"uint64"}],"name":"Initialized","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"string","name":"attestationId","type":"string"}],"name":"OffchainAttestationMade","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"string","name":"attestationId","type":"string"},{"indexed":False,"internalType":"string","name":"reason","type":"string"}],"name":"OffchainAttestationRevoked","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":True,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":False,"inputs":[{"indexed":False,"internalType":"uint64","name":"schemaId","type":"uint64"}],"name":"SchemaRegistered","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"implementation","type":"address"}],"name":"Upgraded","type":"event"},{"inputs":[],"name":"UPGRADE_INTERFACE_VERSION","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"uint64","name":"schemaId","type":"uint64"},{"internalType":"uint64","name":"linkedAttestationId","type":"uint64"},{"internalType":"uint64","name":"attestTimestamp","type":"uint64"},{"internalType":"uint64","name":"revokeTimestamp","type":"uint64"},{"internalType":"address","name":"attester","type":"address"},{"internalType":"uint64","name":"validUntil","type":"uint64"},{"internalType":"enum DataLocation","name":"dataLocation","type":"uint8"},{"internalType":"bool","name":"revoked","type":"bool"},{"internalType":"bytes[]","name":"recipients","type":"bytes[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct Attestation","name":"attestation","type":"tuple"},{"internalType":"contract IERC20","name":"resolverFeesERC20Token","type":"address"},{"internalType":"uint256","name":"resolverFeesERC20Amount","type":"uint256"},{"internalType":"string","name":"indexingKey","type":"string"},{"internalType":"bytes","name":"delegateSignature","type":"bytes"},{"internalType":"bytes","name":"extraData","type":"bytes"}],"name":"attest","outputs":[{"internalType":"uint64","name":"","type":"uint64"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint64","name":"schemaId","type":"uint64"},{"internalType":"uint64","name":"linkedAttestationId","type":"uint64"},{"internalType":"uint64","name":"attestTimestamp","type":"uint64"},{"internalType":"uint64","name":"revokeTimestamp","type":"uint64"},{"internalType":"address","name":"attester","type":"address"},{"internalType":"uint64","name":"validUntil","type":"uint64"},{"internalType":"enum DataLocation","name":"dataLocation","type":"uint8"},{"internalType":"bool","name":"revoked","type":"bool"},{"internalType":"bytes[]","name":"recipients","type":"bytes[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct Attestation","name":"attestation","type":"tuple"},{"internalType":"string","name":"indexingKey","type":"string"},{"internalType":"bytes","name":"delegateSignature","type":"bytes"},{"internalType":"bytes","name":"extraData","type":"bytes"}],"name":"attest","outputs":[{"internalType":"uint64","name":"","type":"uint64"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint64","name":"schemaId","type":"uint64"},{"internalType":"uint64","name":"linkedAttestationId","type":"uint64"},{"internalType":"uint64","name":"attestTimestamp","type":"uint64"},{"internalType":"uint64","name":"revokeTimestamp","type":"uint64"},{"internalType":"address","name":"attester","type":"address"},{"internalType":"uint64","name":"validUntil","type":"uint64"},{"internalType":"enum DataLocation","name":"dataLocation","type":"uint8"},{"internalType":"bool","name":"revoked","type":"bool"},{"internalType":"bytes[]","name":"recipients","type":"bytes[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct Attestation","name":"attestation","type":"tuple"},{"internalType":"uint256","name":"resolverFeesETH","type":"uint256"},{"internalType":"string","name":"indexingKey","type":"string"},{"internalType":"bytes","name":"delegateSignature","type":"bytes"},{"internalType":"bytes","name":"extraData","type":"bytes"}],"name":"attest","outputs":[{"internalType":"uint64","name":"","type":"uint64"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"uint64","name":"schemaId","type":"uint64"},{"internalType":"uint64","name":"linkedAttestationId","type":"uint64"},{"internalType":"uint64","name":"attestTimestamp","type":"uint64"},{"internalType":"uint64","name":"revokeTimestamp","type":"uint64"},{"internalType":"address","name":"attester","type":"address"},{"internalType":"uint64","name":"validUntil","type":"uint64"},{"internalType":"enum DataLocation","name":"dataLocation","type":"uint8"},{"internalType":"bool","name":"revoked","type":"bool"},{"internalType":"bytes[]","name":"recipients","type":"bytes[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct Attestation[]","name":"attestations","type":"tuple[]"},{"internalType":"uint256[]","name":"resolverFeesETH","type":"uint256[]"},{"internalType":"string[]","name":"indexingKeys","type":"string[]"},{"internalType":"bytes","name":"delegateSignature","type":"bytes"},{"internalType":"bytes","name":"extraData","type":"bytes"}],"name":"attestBatch","outputs":[{"internalType":"uint64[]","name":"attestationIds","type":"uint64[]"}],"stateMutability":"payable","type":"function"},{"inputs":[{"components":[{"internalType":"uint64","name":"schemaId","type":"uint64"},{"internalType":"uint64","name":"linkedAttestationId","type":"uint64"},{"internalType":"uint64","name":"attestTimestamp","type":"uint64"},{"internalType":"uint64","name":"revokeTimestamp","type":"uint64"},{"internalType":"address","name":"attester","type":"address"},{"internalType":"uint64","name":"validUntil","type":"uint64"},{"internalType":"enum DataLocation","name":"dataLocation","type":"uint8"},{"internalType":"bool","name":"revoked","type":"bool"},{"internalType":"bytes[]","name":"recipients","type":"bytes[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct Attestation[]","name":"attestations","type":"tuple[]"},{"internalType":"contract IERC20[]","name":"resolverFeesERC20Tokens","type":"address[]"},{"internalType":"uint256[]","name":"resolverFeesERC20Amount","type":"uint256[]"},{"internalType":"string[]","name":"indexingKeys","type":"string[]"},{"internalType":"bytes","name":"delegateSignature","type":"bytes"},{"internalType":"bytes","name":"extraData","type":"bytes"}],"name":"attestBatch","outputs":[{"internalType":"uint64[]","name":"attestationIds","type":"uint64[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"uint64","name":"schemaId","type":"uint64"},{"internalType":"uint64","name":"linkedAttestationId","type":"uint64"},{"internalType":"uint64","name":"attestTimestamp","type":"uint64"},{"internalType":"uint64","name":"revokeTimestamp","type":"uint64"},{"internalType":"address","name":"attester","type":"address"},{"internalType":"uint64","name":"validUntil","type":"uint64"},{"internalType":"enum DataLocation","name":"dataLocation","type":"uint8"},{"internalType":"bool","name":"revoked","type":"bool"},{"internalType":"bytes[]","name":"recipients","type":"bytes[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct Attestation[]","name":"attestations","type":"tuple[]"},{"internalType":"string[]","name":"indexingKeys","type":"string[]"},{"internalType":"bytes","name":"delegateSignature","type":"bytes"},{"internalType":"bytes","name":"extraData","type":"bytes"}],"name":"attestBatch","outputs":[{"internalType":"uint64[]","name":"attestationIds","type":"uint64[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"offchainAttestationId","type":"string"},{"internalType":"address","name":"delegateAttester","type":"address"},{"internalType":"bytes","name":"delegateSignature","type":"bytes"}],"name":"attestOffchain","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string[]","name":"attestationIds","type":"string[]"},{"internalType":"address","name":"delegateAttester","type":"address"},{"internalType":"bytes","name":"delegateSignature","type":"bytes"}],"name":"attestOffchainBatch","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"attestationCounter","outputs":[{"internalType":"uint64","name":"","type":"uint64"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint64","name":"attestationId","type":"uint64"}],"name":"getAttestation","outputs":[{"components":[{"internalType":"uint64","name":"schemaId","type":"uint64"},{"internalType":"uint64","name":"linkedAttestationId","type":"uint64"},{"internalType":"uint64","name":"attestTimestamp","type":"uint64"},{"internalType":"uint64","name":"revokeTimestamp","type":"uint64"},{"internalType":"address","name":"attester","type":"address"},{"internalType":"uint64","name":"validUntil","type":"uint64"},{"internalType":"enum DataLocation","name":"dataLocation","type":"uint8"},{"internalType":"bool","name":"revoked","type":"bool"},{"internalType":"bytes[]","name":"recipients","type":"bytes[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct Attestation","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"uint64","name":"schemaId","type":"uint64"},{"internalType":"uint64","name":"linkedAttestationId","type":"uint64"},{"internalType":"uint64","name":"attestTimestamp","type":"uint64"},{"internalType":"uint64","name":"revokeTimestamp","type":"uint64"},{"internalType":"address","name":"attester","type":"address"},{"internalType":"uint64","name":"validUntil","type":"uint64"},{"internalType":"enum DataLocation","name":"dataLocation","type":"uint8"},{"internalType":"bool","name":"revoked","type":"bool"},{"internalType":"bytes[]","name":"recipients","type":"bytes[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct Attestation[]","name":"attestations","type":"tuple[]"}],"name":"getDelegatedAttestBatchHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"components":[{"internalType":"uint64","name":"schemaId","type":"uint64"},{"internalType":"uint64","name":"linkedAttestationId","type":"uint64"},{"internalType":"uint64","name":"attestTimestamp","type":"uint64"},{"internalType":"uint64","name":"revokeTimestamp","type":"uint64"},{"internalType":"address","name":"attester","type":"address"},{"internalType":"uint64","name":"validUntil","type":"uint64"},{"internalType":"enum DataLocation","name":"dataLocation","type":"uint8"},{"internalType":"bool","name":"revoked","type":"bool"},{"internalType":"bytes[]","name":"recipients","type":"bytes[]"},{"internalType":"bytes","name":"data","type":"bytes"}],"internalType":"struct Attestation","name":"attestation","type":"tuple"}],"name":"getDelegatedAttestHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"string[]","name":"offchainAttestationIds","type":"string[]"}],"name":"getDelegatedOffchainAttestBatchHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"string","name":"offchainAttestationId","type":"string"}],"name":"getDelegatedOffchainAttestHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"string[]","name":"offchainAttestationIds","type":"string[]"},{"internalType":"string[]","name":"reasons","type":"string[]"}],"name":"getDelegatedOffchainRevokeBatchHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"string","name":"offchainAttestationId","type":"string"},{"internalType":"string","name":"reason","type":"string"}],"name":"getDelegatedOffchainRevokeHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"registrant","type":"address"},{"internalType":"bool","name":"revocable","type":"bool"},{"internalType":"enum DataLocation","name":"dataLocation","type":"uint8"},{"internalType":"uint64","name":"maxValidFor","type":"uint64"},{"internalType":"contract ISPHook","name":"hook","type":"address"},{"internalType":"uint64","name":"timestamp","type":"uint64"},{"internalType":"string","name":"data","type":"string"}],"internalType":"struct Schema[]","name":"schemas","type":"tuple[]"}],"name":"getDelegatedRegisterBatchHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"registrant","type":"address"},{"internalType":"bool","name":"revocable","type":"bool"},{"internalType":"enum DataLocation","name":"dataLocation","type":"uint8"},{"internalType":"uint64","name":"maxValidFor","type":"uint64"},{"internalType":"contract ISPHook","name":"hook","type":"address"},{"internalType":"uint64","name":"timestamp","type":"uint64"},{"internalType":"string","name":"data","type":"string"}],"internalType":"struct Schema","name":"schema","type":"tuple"}],"name":"getDelegatedRegisterHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint64[]","name":"attestationIds","type":"uint64[]"},{"internalType":"string[]","name":"reasons","type":"string[]"}],"name":"getDelegatedRevokeBatchHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"uint64","name":"attestationId","type":"uint64"},{"internalType":"string","name":"reason","type":"string"}],"name":"getDelegatedRevokeHash","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"pure","type":"function"},{"inputs":[{"internalType":"string","name":"offchainAttestationId","type":"string"}],"name":"getOffchainAttestation","outputs":[{"components":[{"internalType":"address","name":"attester","type":"address"},{"internalType":"uint64","name":"timestamp","type":"uint64"}],"internalType":"struct OffchainAttestation","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint64","name":"schemaId","type":"uint64"}],"name":"getSchema","outputs":[{"components":[{"internalType":"address","name":"registrant","type":"address"},{"internalType":"bool","name":"revocable","type":"bool"},{"internalType":"enum DataLocation","name":"dataLocation","type":"uint8"},{"internalType":"uint64","name":"maxValidFor","type":"uint64"},{"internalType":"contract ISPHook","name":"hook","type":"address"},{"internalType":"uint64","name":"timestamp","type":"uint64"},{"internalType":"string","name":"data","type":"string"}],"internalType":"struct Schema","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint64","name":"schemaCounter_","type":"uint64"},{"internalType":"uint64","name":"attestationCounter_","type":"uint64"}],"name":"initialize","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"proxiableUUID","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"registrant","type":"address"},{"internalType":"bool","name":"revocable","type":"bool"},{"internalType":"enum DataLocation","name":"dataLocation","type":"uint8"},{"internalType":"uint64","name":"maxValidFor","type":"uint64"},{"internalType":"contract ISPHook","name":"hook","type":"address"},{"internalType":"uint64","name":"timestamp","type":"uint64"},{"internalType":"string","name":"data","type":"string"}],"internalType":"struct Schema","name":"schema","type":"tuple"},{"internalType":"bytes","name":"delegateSignature","type":"bytes"}],"name":"register","outputs":[{"internalType":"uint64","name":"schemaId","type":"uint64"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"components":[{"internalType":"address","name":"registrant","type":"address"},{"internalType":"bool","name":"revocable","type":"bool"},{"internalType":"enum DataLocation","name":"dataLocation","type":"uint8"},{"internalType":"uint64","name":"maxValidFor","type":"uint64"},{"internalType":"contract ISPHook","name":"hook","type":"address"},{"internalType":"uint64","name":"timestamp","type":"uint64"},{"internalType":"string","name":"data","type":"string"}],"internalType":"struct Schema[]","name":"schemas","type":"tuple[]"},{"internalType":"bytes","name":"delegateSignature","type":"bytes"}],"name":"registerBatch","outputs":[{"internalType":"uint64[]","name":"schemaIds","type":"uint64[]"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint64","name":"attestationId","type":"uint64"},{"internalType":"string","name":"reason","type":"string"},{"internalType":"bytes","name":"delegateSignature","type":"bytes"},{"internalType":"bytes","name":"extraData","type":"bytes"}],"name":"revoke","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint64","name":"attestationId","type":"uint64"},{"internalType":"string","name":"reason","type":"string"},{"internalType":"contract IERC20","name":"resolverFeesERC20Token","type":"address"},{"internalType":"uint256","name":"resolverFeesERC20Amount","type":"uint256"},{"internalType":"bytes","name":"delegateSignature","type":"bytes"},{"internalType":"bytes","name":"extraData","type":"bytes"}],"name":"revoke","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint64","name":"attestationId","type":"uint64"},{"internalType":"string","name":"reason","type":"string"},{"internalType":"uint256","name":"resolverFeesETH","type":"uint256"},{"internalType":"bytes","name":"delegateSignature","type":"bytes"},{"internalType":"bytes","name":"extraData","type":"bytes"}],"name":"revoke","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint64[]","name":"attestationIds","type":"uint64[]"},{"internalType":"string[]","name":"reasons","type":"string[]"},{"internalType":"bytes","name":"delegateSignature","type":"bytes"},{"internalType":"bytes","name":"extraData","type":"bytes"}],"name":"revokeBatch","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint64[]","name":"attestationIds","type":"uint64[]"},{"internalType":"string[]","name":"reasons","type":"string[]"},{"internalType":"uint256[]","name":"resolverFeesETH","type":"uint256[]"},{"internalType":"bytes","name":"delegateSignature","type":"bytes"},{"internalType":"bytes","name":"extraData","type":"bytes"}],"name":"revokeBatch","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint64[]","name":"attestationIds","type":"uint64[]"},{"internalType":"string[]","name":"reasons","type":"string[]"},{"internalType":"contract IERC20[]","name":"resolverFeesERC20Tokens","type":"address[]"},{"internalType":"uint256[]","name":"resolverFeesERC20Amount","type":"uint256[]"},{"internalType":"bytes","name":"delegateSignature","type":"bytes"},{"internalType":"bytes","name":"extraData","type":"bytes"}],"name":"revokeBatch","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string","name":"offchainAttestationId","type":"string"},{"internalType":"string","name":"reason","type":"string"},{"internalType":"bytes","name":"delegateSignature","type":"bytes"}],"name":"revokeOffchain","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"string[]","name":"offchainAttestationIds","type":"string[]"},{"internalType":"string[]","name":"reasons","type":"string[]"},{"internalType":"bytes","name":"delegateSignature","type":"bytes"}],"name":"revokeOffchainBatch","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"schemaCounter","outputs":[{"internalType":"uint64","name":"","type":"uint64"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"hook","type":"address"}],"name":"setGlobalHook","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"bool","name":"paused","type":"bool"}],"name":"setPause","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newImplementation","type":"address"},{"internalType":"bytes","name":"data","type":"bytes"}],"name":"upgradeToAndCall","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"version","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"pure","type":"function"}]

# INPUT




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
ip_data={
    "name": "",
    "description": "",
    "data": []
}


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
    await update.message.reply_text('Hey Im Ghilli here! Click /wallet or type wallet to start your transaction! ')

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

    def wallet1(tele_id):
        url = os.environ.get('SUPABASE_URL')
        key = os.environ.get('SUPABASE_KEY')
        alchemy_arb_url = os.environ.get('ALCHEMY_ARB_URL')

        supabase = create_client(url, key)
        web3 = Web3(Web3.HTTPProvider(alchemy_arb_url))

        # Fetch wallet public key from backend
        try:
            data = supabase.table('wallets').select('pub_key').eq('tel_id', tele_id).execute()
            address = data.data[0]['pub_key']
            print(f"Wallet address: {address}")
            try:
                balance_wei = web3.eth.get_balance(address)
                print(f"Wallet balance: {balance_wei / constants.WEI_PER_ETHER} ETH")
                return [False,address,balance_wei / constants.WEI_PER_ETHER]
            except Exception as e:
                print(f'Error getting balance: {e}')

        except:
            print('Wallet not found')
            keypair = web3.eth.account.create()
            print(f"Public Key: {keypair.address}")
            print(f"Private Key: {keypair._private_key.hex()}")
            data = supabase.table('wallets').insert(
                [{'tel_id': tele_id, 'pub_key': keypair.address, 'priv_key': keypair._private_key.hex()}]).execute()
            print(f'Wallet created and saved to database.')
            return [True,keypair.address,0]


    [isnew,address,balance]=wallet1(update.message.from_user.id)
    if isnew:
        await update.message.reply_text(f'Wallet has been succesfully created!  Your wallet address: {address}')
        await update.message.reply_text(f'Your balance: {balance} ETH')
    else:
        await update.message.reply_text(f'Your wallet address: {address}')
        await update.message.reply_text(f'Your balance: {balance} ETH')



    wallet_executed[user_id] = True
    await update.message.reply_text('You have successfully entered your primary details. Click /schema or type schema to enter your schema details!')


async def schema_command(update: Update, context: CallbackContext): # i have assigned each variable to each parameters like attestaion id and more.
    user_id = update.message.from_user.id
    global schema_name
    schema_name = None  # Initialize the variable here
    await update.message.reply_text('Please enter the Schema Name:')
    return SCHE_NAME

async def recieve_schema_name(update: Update, context: CallbackContext):
    global schema_name
    schema_name = update.message.text
    global ip_data
    ip_data["name"]=update.message.text
    await update.message.reply_text('Please Enter Schema Decrpription:')

    return SCHE_DESP



async def recieve_schema_descp(update: Update, context: CallbackContext):
    global schema_desp
    schema_desp = update.message.text

    ip_data['description']=update.message.text

    await update.message.reply_text('Enter Field Name:')
    return FIELD_NAME

async def recieve_field_name(update: Update, context: CallbackContext):
    global field_name
    field_name = update.message.text

    global ip_data
    ip_data["data"].append({"name": field_name, "type": "string"})

    def create_schema(ip_data, tele_id):
        url = os.environ.get('SUPABASE_URL')
        key = os.environ.get('SUPABASE_KEY')
        alchemy_arb_url = os.environ.get('ALCHEMY_ARB_URL')

        supabase = create_client(url, key)
        web3 = Web3(Web3.HTTPProvider(alchemy_arb_url))

        # Create schema

        try:
            data = supabase.table("wallets").select("pub_key,priv_key").eq("tel_id", tele_id).execute()
            print(f'data:{data.data[0]}')
            address = data.data[0]["pub_key"]
            priv_key = data.data[0]["priv_key"]
            print(f"Wallet address: {address}")
            try:
                ethsign = web3.eth.contract(
                    address=Web3.to_checksum_address("0x4e4af2a21ebf62850fd99eb6253e1efbb56098cd"),
                    abi=abi)
                nonce = web3.eth.get_transaction_count(address)
                create_schema_tx = ethsign.functions.register(
                    [address, False, 0, 0, "0x0000000000000000000000000000000000000000", 0, json.dumps(ip_data)],
                    '0x').build_transaction({"chainId": 421614, "gas": 250000, "maxFeePerGas": web3.to_wei("2", "gwei"),
                                             "maxPriorityFeePerGas": web3.to_wei("1", "gwei"), "nonce": nonce, })
                print(create_schema_tx)
                signed_txn = web3.eth.account.sign_transaction(create_schema_tx, private_key=priv_key)
                print(signed_txn)
                web3.eth.send_raw_transaction(signed_txn.rawTransaction)
                print(f"Transaction Sent Successsfully: https://sepolia.arbiscan.io/tx/{signed_txn.hash.hex()}")
                tx_receipt = web3.eth.get_transaction_receipt(signed_txn.hash.hex())
                events = ethsign.events.SchemaRegistered().process_receipt(tx_receipt)
                print(f'Created Schema Id: {events[0].args.schemaId}')
                return [signed_txn.hash.hex(),events[0].args.schemaId]
            except Exception as e:
                print("Error creating schema")
                print(e)
        except Exception as e:

            print("Wallet not found")
            print(e)




    print(f'ip data: {ip_data}')
    print(f'user id:{update.message.from_user.id}')
    [tx,schema_id2]=create_schema(ip_data,update.message.from_user.id)
    await update.message.reply_text(f'Tx hash: {tx}')
    await update.message.reply_text(f'SchemaID: {schema_id2}')



    await update.message.reply_text('You have successfully entered the details. Click /viewall or type viewall to view your all details!')


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


async def viewall_command(update: Update, context: CallbackContext):  # i have assigned each variable to each parameters like attestaion id and more.
    user_id = update.message.from_user.id

    await update.message.reply_text('Transacation Details:')
    await update.message.reply_text(f'Attestation ID: {attest_id}')
    await update.message.reply_text(f'From Address: {from_address_id}')
    await update.message.reply_text(f'To Address: {to_address_id}')
    await update.message.reply_text(f'Schema Name: {schema_name}')
    await update.message.reply_text(f'Schema Descrption: {schema_desp}')
    await update.message.reply_text(f'Field Name: {field_name}')

    #signed_txn.hash.hex()




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
    app.run_polling(poll_interval=10)  # Poll


#fns

def create_schema (ip_data,tele_id):
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_KEY')
    alchemy_arb_url = os.environ.get('ALCHEMY_ARB_URL')

    supabase = create_client(url, key)
    web3 = Web3(Web3.HTTPProvider(alchemy_arb_url))

    # Create schema

    try:
        data = supabase.table("wallets").select("pub_key,priv_key").eq("tele_id", tele_id).execute()
        address = data.data[0]["pub_key"]
        priv_key = data.data[0]["priv_key"]
        print(f"Wallet address: {address}")
        try:
            ethsign = web3.eth.contract(address=Web3.to_checksum_address("0x4e4af2a21ebf62850fd99eb6253e1efbb56098cd"),
                                        abi=abi)
            nonce = web3.eth.get_transaction_count(address)
            create_schema_tx = ethsign.functions.register(
                [address, False, 0, 0, "0x0000000000000000000000000000000000000000", 0, ip_data],
                '0x').build_transaction({"chainId": 421614, "gas": 250000, "maxFeePerGas": web3.to_wei("2", "gwei"),
                                         "maxPriorityFeePerGas": web3.to_wei("1", "gwei"), "nonce": nonce, })
            print(create_schema_tx)
            signed_txn = web3.eth.account.sign_transaction(create_schema_tx, private_key=priv_key)
            print(signed_txn)
            web3.eth.send_raw_transaction(signed_txn.rawTransaction)
            print(f"Transaction Sent Successsfully: https://sepolia.arbiscan.io/tx/{signed_txn.hash.hex()}")
            tx_receipt = web3.eth.get_transaction_receipt(signed_txn.hash.hex())
            events = ethsign.events.SchemaRegistered().process_receipt(tx_receipt)
            print(f'Created Schema Id: {events[0].args.schemaId}')
        except Exception as e:
            print("Error creating schema")
            print(e)
    except:
        print("Wallet not found")


def wallet1(tele_id):
    url = os.environ.get('SUPABASE_URL')
    key = os.environ.get('SUPABASE_KEY')
    alchemy_arb_url = os.environ.get('ALCHEMY_ARB_URL')

    supabase = create_client(url, key)
    web3 = Web3(Web3.HTTPProvider(alchemy_arb_url))

    # Fetch wallet public key from backend
    try:
        data = supabase.table('wallets').select('pub_key').eq('tel_id', tele_id).execute()
        address = data.data[0]['pub_key']
        print(f"Wallet address: {address}")
        try:
            balance_wei = web3.eth.get_balance(address)
            print(f"Wallet balance: {balance_wei / constants.WEI_PER_ETHER} ETH")
        except Exception as e:
            print(f'Error getting balance: {e}')
    except:
        print('Wallet not found')
        keypair = web3.eth.account.create()
        print(f"Public Key: {keypair.address}")
        print(f"Private Key: {keypair._private_key.hex()}")
        data = supabase.table('wallets').insert(
            [{'tel_id': tele_id, 'pub_key': keypair.address, 'priv_key': keypair._private_key.hex()}]).execute()
        print(f'Wallet created and saved to database.')

#signed_txn.hash.hex()- tx hash
#events[0].args.schemaId - scheama id