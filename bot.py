from telegram import Update 
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes 
import re
import os

# 🔹 Import keep_alive
from keep_alive import keep_alive

# Get bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Function to detect and format trade message
async def format_trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    pattern = re.compile(
        r"(?i)([A-Z/]+)\s*(long|short)\s*([\d\.]+)\s*(\d+x).*?tp\s*([\d\.,\s]+).*?(?:sl|stop)\s*([\d\.]+)"
    )

    match = pattern.search(text)
    if not match:
        await update.message.reply_text("❌ Couldn't understand the message format.")
        return

    coin, direction, entry, leverage, tps, stop = match.groups()

    coin = coin.upper()
    if "/" not in coin:
        coin = f"{coin}/USDT"

    tp_values = [tp.strip() for tp in re.split(r"[, ]+", tps) if tp.strip()]

    if direction.lower() == "long":
        header = "🟢 LONG TRADE SETUP 🟢"
        footer = "(Trade only with 5–10% of your funds\nEnter in parts for better risk management) 🚀"
    else:
        header = "🔴 SHORT TRADE SETUP 🔴"
        footer = "(Trade only with 5–10% of your funds) 🚀"

    formatted = [
        header, "",
        f"▶️ COIN: {coin}",
        f"LEVERAGE: {leverage}",
        "",
        f"📌 ENTRY: {entry}", ""
    ]

    for i, tp in enumerate(tp_values, 1):
        formatted.append(f"🎯 TP{i}: {tp}")

    formatted.append("")
    formatted.append(f"❌ STOP: {stop}")
    formatted.append("")
    formatted.append(footer)

    await update.message.reply_text("\n".join(formatted))


# 🔹 Start bot
if name == "main":
    keep_alive()   # <-- added line
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, format_trade)) 
    print("🤖 Bot is running...")
    app.run_polling()
