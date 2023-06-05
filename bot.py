import os
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Retrieve the bot token from the repository secrets or environment variables
TOKEN = os.getenv('TOKEN')

# Create an updater and pass in your bot token
updater = Updater(token=TOKEN)

# Get the dispatcher to register handlers
dispatcher = updater.dispatcher

admin_username = 'Ali_J_Maghari'
pre_selected_username = 'Ali_J_Maghari'
words_to_delete = []  # Add the words you want to delete messages for
words_to_reply = ['كلمة ٥', 'كلمة ٦']  # Add the words you want to reply to

# Define the command for adding a word to the delete list and check if the user is admin
def add_delete_word(update, context):
    if update.message.from_user.username == admin_username:
        if len(context.args) > 0:
            new_word = ' '.join(context.args)
            # Add the new word to the delete list
            context.user_data.setdefault('delete_words', []).append(new_word)
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"'{new_word}' added to delete list.")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a word to add to the delete list.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")

add_delete_word_handler = CommandHandler('add_delete_word', add_delete_word)
dispatcher.add_handler(add_delete_word_handler)

# Define the command for removing a word from the delete list and check if the user is admin
def remove_delete_word(update, context):
    if update.message.from_user.username == admin_username:
        if len(context.args) > 0:
            word_to_remove = ' '.join(context.args)
            delete_words = context.user_data.get('delete_words', [])
            if word_to_remove in delete_words:
                # Remove the word from the delete list
                context.user_data['delete_words'].remove(word_to_remove)
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"'{word_to_remove}' removed from delete list.")
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text=f"'{word_to_remove}' is not in the delete list.")
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Please provide a word to remove from the delete list.")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="You are not authorized to use this command.")

remove_delete_word_handler = CommandHandler('remove_delete_word', remove_delete_word)
dispatcher.add_handler(remove_delete_word_handler)

# Define the command for adding the bot to a group
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="بوت مخصص للعناية بالأخلاق")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Define the function to send a reply message
def send_reply(update, context):
    reply_text = "This is a reply message from the bot."
    context.bot.send_message(chat_id=update.message.chat_id, text=reply_text, reply_to_message_id=update.message.message_id)

# Define the function to delete messages containing specific words
def delete_message(update, context):
    message_text = update.message.text.lower()
    if update.message.from_user.username == pre_selected_username:
        for word in words_to_reply:
            if word in message_text:
                send_reply(update, context)
                break

    delete_words = context.user_data.get('delete_words', [])
    for word in delete_words:
        if word in message_text:
            context.bot.delete_message(chat_id=update.effective_chat.id, message_id=update.message.message_id)
            break

delete_handler = MessageHandler(Filters.text, delete_message)
dispatcher.add_handler(delete_handler)

# Start the bot
updater.start_polling()
