from flask import Flask, request
import requests
import os

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")

@app.route("/", methods=["POST"])
def webhook():
    data = request.json

    message = data.get("message", {}).get("text")
    chat_id = data.get("message", {}).get("chat", {}).get("id")

    if message:
        requests.post(f"https://api.telegram.org/bot{TOKEN}/sendMessage", json={
            "chat_id": chat_id,
            "text": f"Bạn vừa gửi: {message}"
        })

    return "OK"

@app.route("/", methods=["GET"])
def home():
    return "Bot is running"