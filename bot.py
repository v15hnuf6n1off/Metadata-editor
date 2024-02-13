import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from moviepy.editor import VideoFileClip
import eyed3
import PyPDF2
import rarfile
import zipfile

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Your Telegram bot token
TOKEN = '6536175076:AAGzf8AHlGni9q_cEAYzZ54s-Im-Gqd1CJU'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Welcome! Send me a file (video, audio, document, etc.) to edit its metadata.")

def handle_document(update: Update, context: CallbackContext) -> None:
    file = update.message.document.get_file()
    file.download('temp_file')

    # Determine the file type
    file_extension = os.path.splitext(file.file_path)[-1].lower()

    if file_extension in ['.mp4', '.mkv', '.avi']:
        # Edit video metadata
        clip = VideoFileClip('temp_file')
        # Modify metadata here (e.g., clip.set_duration(), clip.set_audio(), etc.)
        # Save the updated video
        clip.write_videofile('edited_video.mp4')
        update.message.reply_document(document=open('edited_video.mp4', 'rb'))

    elif file_extension in ['.mp3', '.wav']:
        # Edit audio metadata
        audio = eyed3.load('temp_file')
        # Modify metadata here (e.g., audio.tag.artist, audio.tag.album, etc.)
        # Save the updated audio
        audio.tag.save()
        update.message.reply_document(document=open('temp_file', 'rb'))

    elif file_extension == '.pdf':
        # Edit PDF metadata using PyPDF2
        # Modify metadata here (e.g., pdf.addMetadata(), pdf.setPageLabels(), etc.)
        # Save the updated PDF
        update.message.reply_document(document=open('temp_file', 'rb'))

    elif file_extension in ['.rar', '.zip']:
        # Extract the archive
        with rarfile.RarFile('temp_file', 'r') as rar:
            rar.extractall('extracted_files')

        # Edit metadata of individual files within the archive
        # Modify metadata here (e.g., using eyed3 for audio files)
        # Re-archive the files
        with rarfile.RarFile('edited_archive.rar', 'w') as edited_rar:
            for root, _, files in os.walk('extracted_files'):
                for file in files:
                    edited_rar.write(os.path.join(root, file))

        update.message.reply_document(document=open('edited_archive.rar', 'rb'))

    else:
        update.message.reply_text("Unsupported file type. Please send a valid file.")

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.document.mime_type("video/*") | Filters.document.mime_type("audio/*") | Filters.document.mime_type("application/pdf") | Filters.document.mime_type("application/x-rar-compressed") | Filters.document.mime_type("application/zip"), handle_document))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
