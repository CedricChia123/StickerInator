from dotenv import load_dotenv
import logging
import os

load_dotenv()

from telegram import Update, InputSticker
from telegram.ext import CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
from telegram.constants import StickerFormat

SELECTING_PACK, CONFIRM_DELETE = map(chr, range(2))

async def delete_pack(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logging.info("Delete pack by {}".format(update.effective_user.name))
    await update.message.reply_text("Please send the sticker you wish to delete")
    return SELECTING_PACK

async def select_pack(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["sticker"] = update.message.sticker
    await update.message.reply_text("Confirm delete sticker? Reply with yes")
    return CONFIRM_DELETE

async def confirm_delete(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text.lower() == "yes":
        bot = update.get_bot()
        sticker_set = context.user_data["sticker"].set_name
        sticker = context.user_data["sticker"].file_id
        await bot.delete_sticker_from_set(sticker)
        await update.message.reply_text(f"Sticker deleted from {sticker_set}")
    else:
        await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Invalid, command cancelled")
    return ConversationHandler.END

def delete_sticker_conv():
    return ConversationHandler(
        entry_points=[CommandHandler("delsticker", delete_pack)],
        states={
            SELECTING_PACK: [MessageHandler(filters.Sticker.ALL, select_pack)],
            CONFIRM_DELETE: [MessageHandler(filters.TEXT, confirm_delete)],
            },
        fallbacks=[MessageHandler(filters.ALL, cancel)]
    )
