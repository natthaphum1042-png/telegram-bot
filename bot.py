import os
import asyncio
from flask import Flask
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# --- ส่วนของ Flask เพื่อหลอก Render ---
server = Flask('')

@server.route('/')
def home():
    return "Bot is alive!"

def run():
    # Render จะส่ง Port มาให้ผ่าน Environment Variable ชื่อ PORT
    port = int(os.environ.get("PORT", 10000))
    server.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

# --- ส่วนของ Telegram Bot เดิมของคุณพี่ ---
TOKEN = os.getenv("BOT_TOKEN")

async def delete_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await update.message.delete()
    except:
        pass

async def main():
    # เริ่มต้น Flask Server
    keep_alive()
    
    # เริ่มต้น Telegram Bot
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, delete_join))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, delete_join))
    
    # รันบอท
    await app.initialize()
    await app.start()
    print("Bot started...")
    await app.updater.start_polling()
    
    # ป้องกันไม่ให้โปรแกรมจบการทำงาน
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
