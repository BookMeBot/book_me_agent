from flask import Flask, request
import telegram
import os

app = Flask(__name__)
bot = telegram.Bot(token=os.getenv("TELEGRAM_BOT_TOKEN"))

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telegram.Update.de_json(request.get_json(force=True), bot)
    # Process the update here
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text="Hello, this is a response from the bot!")
    return 'ok'

if __name__ == '__main__':
    app.run(port=5000)