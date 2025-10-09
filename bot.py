from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import os, re

BOT_TOKEN = os.getenv("BOT_TOKEN")  # token will come from Render environment

def format_trade_message(text: str):
    pattern = r"(LONG|SHORT).*?COIN:\s*([\w/]+).*?LEVERAGE:\s*(\d+x).*?ENTRY:\s*([\d.]+).*?TP1:\s*([\d.]+).*?TP2:\s*([\d.]+).*?TP3:\s*([\d.]+).*?TP4:\s*([\d.]+).*?STOP:\s*([\d.]+)"
    match = re.search(pattern, text, re.S | re.I)
    
    if match:
        direction = match.group(1).upper()
        coin = match.group(2).upper()
        leverage = match.group(3)
        entry = match.group(4)
        tp1, tp2, tp3, tp4 = match.group(5), match.group(6), match.group(7), match.group(8)
        stop = match.group(9)
        emoji = "🟢" if direction == "LONG" else "🔴"

        return (
            f"{emoji} *{direction} Trade Setup*\n\n"
            f"💹 *Coin:* {coin}\n"
            f"⚙️ *Leverage:* {leverage}\n"
            f"💰 *Entry:* {entry}\n"
            f"🎯 *Targets:* {tp1} / {tp2} / {tp3} / {tp4}\n"
            f"❌ *Stop Loss:* {stop}\n\n"
            f"📊 Risk: Trade only with 5–10% of your funds.\n"
            f"Enter in parts for better risk management. 🚀"
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    formatted = format_trade_message(text)
    if formatted:
        await update.message.reply_text(formatted, parse_mode="Markdown")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🤖 Bot is running...")
app.run_polling()