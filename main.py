from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import os

# File path to question papers
BASE_DIR = "question_papers"

# Start command handler
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Welcome to the Question Paper Bot!\n"
        "Choose your class to get last year's question papers.",
        reply_markup=main_menu()
    )

# Menu for selecting class
def main_menu():
    keyboard = [
        [InlineKeyboardButton("Class 9", callback_data="class_9")],
        [InlineKeyboardButton("Class 10", callback_data="class_10")],
        [InlineKeyboardButton("Class 11", callback_data="class_11")],
        [InlineKeyboardButton("Class 12", callback_data="class_12")],
    ]
    return InlineKeyboardMarkup(keyboard)

# Callback for class selection
def class_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    class_name = query.data
    papers = get_question_papers(class_name)
    
    if papers:
        query.edit_message_text(
            text=f"Select a subject for {class_name.replace('_', ' ').capitalize()}:",
            reply_markup=papers_menu(class_name, papers)
        )
    else:
        query.edit_message_text(text="No question papers available for this class.")

# Get question papers for a class
def get_question_papers(class_name):
    class_dir = os.path.join(BASE_DIR, class_name)
    if os.path.exists(class_dir):
        return os.listdir(class_dir)
    return []

# Menu for selecting question papers
def papers_menu(class_name, papers):
    keyboard = [
        [InlineKeyboardButton(paper, callback_data=f"{class_name}|{paper}")]
        for paper in papers
    ]
    keyboard.append([InlineKeyboardButton("Back", callback_data="back")])
    return InlineKeyboardMarkup(keyboard)

# Handle subject selection and send the file
def paper_handler(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    query.answer()
    data = query.data
    
    if data == "back":
        query.edit_message_text(
            text="Choose your class to get last year's question papers:",
            reply_markup=main_menu()
        )
    else:
        class_name, paper = data.split("|")
        file_path = os.path.join(BASE_DIR, class_name, paper)
        
        if os.path.exists(file_path):
            query.edit_message_text(text=f"Here is your {paper}:")
            context.bot.send_document(chat_id=query.message.chat_id, document=open(file_path, "rb"))
        else:
            query.edit_message_text(text="Sorry, the file does not exist.")

# Main function
def main():
    # Replace 'YOUR_BOT_TOKEN' with your bot token
    updater = Updater("7541573126:AAGanJEXLDgyTAa10AmrRztIgFNvQ4fnWho")
    dispatcher = updater.dispatcher
    
    # Command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(class_handler, pattern="class_"))
    dispatcher.add_handler(CallbackQueryHandler(paper_handler))
    
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
        
