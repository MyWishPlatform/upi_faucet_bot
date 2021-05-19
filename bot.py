import logging
from json import load

from telegram import Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    MessageFilter,
    CallbackContext,
)

from blockchain import validate_address, send_tokens
from cache import check_timeout
from utils import readable_timeout


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def start(update: Update, context) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi!\nI'm UPI faucet-bot!\nYou can get test tokens from me.")


def help(update: Update, context) -> None:
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="You can receive tokens by simply sending me your ETH address.")


def valid_address_callback(update: Update, _: CallbackContext) -> None:
    user_id = update.effective_user['id']
    address = update.message.text
    if not check_timeout(user_id, address):
        update.message.reply_text(f"Transaction sent. \n{send_tokens(user_id, address)}")
    else:
        update.message.reply_text(
            f"Sorry bit you've already received tokens. \n{readable_timeout(user_id, address)} remains")


def invalid_address_callback(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Please input valid ETH address")


def main() -> None:
    with open('settings/local.json') as file:
        BOT_TOKEN = load(file)['token']

    updater = Updater(token=BOT_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(MessageHandler(AddressFilter(), valid_address_callback))

    # AddressFilter with logical operator ~ as NOT, check BaseFilter class for more info
    dispatcher.add_handler(MessageHandler(~AddressFilter(), invalid_address_callback))

    updater.start_polling()
    updater.idle()


class AddressFilter(MessageFilter):
    def filter(self, message: str) -> bool:
        address = message.text
        return validate_address(address)


if __name__ == '__main__':
    main()
