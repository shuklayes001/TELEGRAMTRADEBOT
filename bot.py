from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import re
import os

# Get bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Function to detect and format trade message
async def format_trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    # Regex pattern to extract trade info (handles both BTC and BTC/USDT)
    pattern = re.compile(
        r"(?i)([A-Z/]+)\s*(long|short)\s*([\d\.]+)\s*(\d+x).*?tp\s*([\d\.,\s]+).*?(?:sl|stop)\s*([\d\.]+)"
    )

    match = pattern.search(text)
    if not match:
        await update.message.reply_text("❌ Couldn't understand the message format.")
        return

    coin, direction, entry, leverage, tps, stop = match.groups()

    # Normalize coin pair
    coin = coin.upper()
    if "/" not in coin:
        coin = f"{coin}/USDT"

    # Clean and split TPs
    tp_values = [tp.strip() for tp in re.split(r"[, ]+", tps) if tp.strip()]

    # Choose headers and footers
    if direction.lower() == "long":
        header = "🟢 LONG TRADE SETUP 🟢"
        footer = "(Trade only with 5–10% of your funds\nEnter in parts for better risk management) 🚀"
    else:
        header = "🔴 SHORT TRADE SETUP 🔴"
        footer = "(Trade only with 5–10% of your funds) 🚀"

    # Build formatted message
    formatted = [
        header,
        "",
        f"▶️ COIN: {coin}",
        f"LEVERAGE: {leverage}",
        "",
        f"📌 ENTRY: {entry}",
        ""
    ]

    for i, tp in enumerate(tp_values, 1):
        formatted.append(f"🎯 TP{i}: {tp}")

    formatted.append("")
    formatted.append(f"❌ STOP: {stop}")
    formatted.append("")
    formatted.append(footer)

    await update.message.reply_text("\n".join(formatted))

# Start bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, format_trade))
    print("🤖 Bot is running...")
    app.run_polling()


