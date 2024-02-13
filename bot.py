from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient

# Create a MongoClient to the running MongoDB instance
mongo_client = MongoClient('mongodb+srv://file:link@cluster0.jth5g3y.mongodb.net/?retryWrites=true&w=majority')

# Getting a Database
db = mongo_client['Cluster0']

# Getting a Collection
collection = db['metedit']

app = Client("my_bot", bot_token="6536175076:AAGzf8AHlGni9q_cEAYzZ54s-Im-Gqd1CJU", api_id="21165589", api_hash="8cc762f4873e84a7cf0cbfd66a07244b")

# Start command
@app.on_message(filters.command("start"))
def start(client, message):
    # Save user id and profile link to database
    user_id = message.from_user.id
    profile_link = message.from_user.mention
    collection.insert_one({"user_id": user_id, "profile_link": profile_link})
    # Send user id and profile link to log channel
    # Welcome the user
    message.reply_text("Welcome to the bot!")

# Inline commands
@app.on_message(filters.command("edit metadata"))
def edit_metadata(client, message):
    # Edit metadata of the given file
    pass

@app.on_message(filters.command("rename"))
def rename(client, message):
    # Rename the title of the given file
    pass

@app.on_message(filters.command("convert"))
def convert(client, message):
    # Convert the given file to another format
    pass

@app.on_message(filters.command("extract"))
def extract(client, message):
    # Extract the video or audio from the given file
    pass

# Commands
@app.on_message(filters.command("set_thumb"))
def set_thumb(client, message):
    # Set custom thumbnail
    pass

@app.on_message(filters.command("del_thumb"))
def del_thumb(client, message):
    # Delete the custom thumbnail
    pass

@app.on_message(filters.command("set_caption"))
def set_caption(client, message):
    # Set custom caption
    pass

@app.on_message(filters.command("del_caption"))
def del_caption(client, message):
    # Remove the custom caption
    pass

@app.on_message(filters.command("users"))
def users(client, message):
    # Show how many users are using the bot (only for admin use)
    pass

@app.on_message(filters.command("broadcast"))
def broadcast(client, message):
    # Broadcast message to user (only for admin use)
    pass

app.run()
