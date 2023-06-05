import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Define your bot token
TOKEN = '6005891028:AAHJ1sGtywfpmDiQs0nskgBmb55OpiN2Zs0'

# Create an updater and pass in your bot token
updater = Updater(token=TOKEN)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

# Define the command for adding the bot to a group
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm ready to delete messages containing specific words in this group.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Define the function to send a reply message
def send_reply(update, context):
    reply_text = "This is a reply message from the bot."
    context.bot.send_message(chat_id=update.message.chat_id, text=reply_text, reply_to_message_id=update.message.message_id)

# Define the function to delete messages containing specific words
def delete_message(update, context):
    pre_selected_username = 'Ali_J_Maghari'
    words_to_delete = ['كلمة ١', 'كلمة ٢', 'كلمة ٣', 'كلمة ٤']  # Add the words you want to delete messages for
    words_to_reply = ['كلمة ٥', 'كلمة ٦']  # Add the words you want to reply to

    message_text = update.message.text.lower()
    if update.message.from_user.username == pre_selected_username:
        for word in words_to_reply:
            if word in message_text:
                send_reply(update, context)
                break

    for word in words_to_delete:
        if word in message_text:
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
            break

delete_handler = MessageHandler(Filters.text, delete_message)
dispatcher.add_handler(delete_handler)

# Start the bot
updater.start_polling()
