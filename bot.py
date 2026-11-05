import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import gspread
from google.oauth2.service_account import Credentials

# Enable logging to see console outputs
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# --- GOOGLE SHEETS SETUP ---
# Define the scopes required for Google Sheets & Drive
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# Load credentials from your service account JSON file (or environment config)
# Make sure your credentials JSON file is uploaded to your repo if reading locally,
# or handled via environment variables on Koyeb.
CREDENTIALS_FILE = "credentials.json"  # Replace with your actual JSON filename if needed


def append_to_sheet(data_text):
  try:
    creds = Credentials.from_service_account_file(
        CREDENTIALS_FILE, scopes=SCOPES
    )
    client = gspread.authorize(creds)

    # Open your Google Sheet by its title
    sheet = client.open("YourGoogleSheetName").sheet1

    # Append the incoming message text as a new row
    sheet.append_row([data_text])
    print(f"Successfully added to sheet: {data_text}")
  except Exception as e:
    print(f"Error writing to Google Sheet: {e}")


# --- TELEGRAM BOT HANDLER ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
  user_message = update.message.text
  chat_id = update.message.chat_id

  # Respond back to Telegram to confirm receipt
  await update.message.reply_text(f"Received! Saving to Google Sheet: {user_message}")

  # Save the message text directly into your Google Sheet
  append_to_sheet(user_message)


def main():
  # Replace 'YOUR_TELEGRAM_BOT_TOKEN' with your actual token
  # (On Koyeb, you can also load this using os.environ.get("TELEGRAM_TOKEN"))
  TOKEN = "9139843284:AAGYbN69Ms0bJ5nEAsnf_KHO1YE87d1LYh4"

  application = ApplicationBuilder().token(TOKEN).build()

  # Listen for any text messages sent to the bot
  echo_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message)
  application.add_handler(echo_handler)

  print("Bot is running and listening for messages...")
  application.run_polling()


if __name__ == "__main__":
  main()
