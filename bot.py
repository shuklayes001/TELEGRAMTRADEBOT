import os
import re
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("Bot token not found! Please set BOT_TOKEN as environment variable.")

# Function to format trade messages
def format_trade_message(text: str):
    # Detect LONG or SHORT
    direction_match = re.search(r"(LONG|SHORT)", text, re.I)
    direction = direction_match.group(1).upper() if direction_match else "TRADE"
    emoji = "🟢" if direction == "LONG" else "🔴"

    heading = f"{emoji} {direction} TRADE SETUP {emoji}\n\n"

    # Detect COIN
    coin_match = re.search(r"COIN[:\s]*([\w/]+)", text, re.I)
    coin = coin_match.group(1).upper() if coin_match else "UNKNOWN"
    coin_line = f"▶️ COIN: {coin}"

    # Detect LEVERAGE
    leverage_match = re.search(r"LEVERAGE[:\s]*([\d]+x)", text, re.I)
    leverage = leverage_match.group(1) if leverage_match else "N/A"
    leverage_line = f"LEVERAGE: {leverage}\n"

    # Detect ENTRY
    entry_match = re.search(r"ENTRY[:\s]*([\d.]+)", text, re.I)
    entry = entry_match.group(1) if entry_match else "N/A"
    entry_line = f"\n📌 ENTRY: {entry}\n"

    # Detect all TPs
    tps = re.findall(r"TP\d*[:\s]*([\d.]+)", text, re.I)
    tp_lines = ""
    for idx, tp in enumerate(tps, start=1):
        tp_lines += f"🎯 TP{idx}: {tp}\n"

    # Detect STOP
    stop_match = re.search(r"STOP[:\s]*([\d.]+)", text, re.I)
    stop = stop_match.group(1) if stop_match else "N/A"
    stop_line = f"\n❌ STOP: {stop}\n"

    # Risk note
    risk_note = "\n(Trade only with 5-10% of your funds\nEnter in parts for better risk management) 🚀 By SANDY..."

    formatted_message = heading + coin_line + "\n" + leverage_line + entry_line + tp_lines + stop_line + risk_note
    return formatted_message

# Handler for messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    formatted = format_trade_message(text)
    await update.message.reply_text(formatted)

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Listen to all text messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
