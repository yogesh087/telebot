from typing import Final

# pip install python-telegram-bot
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

print('Starting up bot...')

TOKEN: Final = '6186281193:AAHlqvfU2m3HfdqRrCZ2QrH6Jp5moxzo4RA'
BOT_USERNAME: Final = '@asuaano_bot'


# Lets us use the /start command
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello there! I\'m a bot. What\'s up?')


# Lets us use the /help command
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Try typing anything and I will do my best to respond!')


# Lets us use the /custom command
async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome to our online store! How can I help you?')


from typing import List

class ShoppingCart:
    def __init__(self):
        self.items = []

    def add_item(self, item: str):
        self.items.append(item)

    def get_items(self) -> List[str]:
        return self.items

class Store:
    def __init__(self):
        self.cart = ShoppingCart()
        self.inventory = {'apple': 2, 'banana': 3, 'orange': 5}

    def add_to_cart(self, item: str):
        if item in self.inventory and self.inventory[item] > 0:
            self.cart.add_item(item)
            self.inventory[item] -= 1
            return f"{item} added to cart!"
        else:
            return "Sorry, we don't have that item in stock."

    def view_cart(self):
        if len(self.cart.get_items()) == 0:
            return "Your cart is empty."
        else:
            return f"Your cart contains: {', '.join(self.cart.get_items())}"

def handle_response(text: str) -> str:
    # Create your own response logic
    processed: str = text.lower()

    if 'hello' in processed:
        return 'Welcome to our online store! How can I help you?'

    if 'how are you' in processed:
        return 'I\'m good!'

    if 'add' in processed:
        item = processed.split('add ')[1]
        return Store().add_to_cart(item)

    if 'view cart' in processed:
        return Store().view_cart()

    return 'I don\'t understand'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get basic info of the incoming message
    message_type: str = update.message.chat.type
    text: str = update.message.text

    # Print a log for debugging
    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    # React to group messages only if users mention the bot directly
    if message_type == 'group':
        # Replace with your bot username
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response: str = handle_response(new_text)
        else:
            return  # We don't want the bot respond if it's not mentioned in the group
    else:
        response: str = handle_response(text)

    # Reply normal if the message is in private
    print('Bot:', response)
    await update.message.reply_text(response)


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)


