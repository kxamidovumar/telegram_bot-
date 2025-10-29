# -*- coding: utf-8 -*-
"""
Created on Wed Oct 29 10:35:21 2025

@author: user
"""
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from deep_translator import GoogleTranslator

# === Bu yerga o'z tokeningni joylashtir ===
BOT_TOKEN = "8358475521:AAGOc_b5FT8tUxd_vEsuczA_tY5aFjDGwSw"  # Masalan: "123456789:AAABBBCCCDDDEEEXXX"

# /start buyrug'i uchun
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Salom! Men tarjima botman.\nMatn yubor — men uni o'zbek tiliga tarjima qilib beraman.\n"
        "Tilni o'zgartirish uchun: /to en  (masalan inglizchaga)"
    )

# /to buyrug'i (maqsad tilni o'zgartirish)
async def set_target_lang(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Foydalanish: /to <til_kodi> (masalan: /to en yoki /to ru)")
        return
    lang = context.args[0].lower()
    context.user_data["target_lang"] = lang
    await update.message.reply_text(f"✅ Tarjima tili: {lang.upper()} qilib o'rnatildi.")

# Asosiy tarjima funksiyasi
async def translate_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    target_lang = context.user_data.get("target_lang", "uz")  # default o'zbekcha

    try:
        translated = GoogleTranslator(source="auto", target=target_lang).translate(text)
        await update.message.reply_text(f"🌐 ({target_lang.upper()})\n{translated}")
    except Exception as e:
        await update.message.reply_text("❌ Tarjima xatosi: " + str(e))

# Botni ishga tushirish
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("to", set_target_lang))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, translate_text))

    print("🤖 Bot ishga tushdi!")
    app.run_polling()

if __name__ == "__main__":
    main()
