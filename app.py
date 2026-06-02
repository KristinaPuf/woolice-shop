import requests
from flask import Flask, request, jsonify, render_template  # <-- Dodaj render_template
from flask_cors import CORS
import json
import os
from dotenv import load_dotenv

# Load .env
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("index.html")

ORDERS_FILE = "orders.json"

# TELEGRAM SETTINGS
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


def send_telegram_message(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram not configured")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    try:
        requests.post(url, data={
            "chat_id": CHAT_ID,
            "text": message
        })
    except Exception as e:
        print("Telegram error:", e)


# LOAD ORDERS
def load_orders():
    try:
        with open(ORDERS_FILE, "r") as f:
            return json.load(f)
    except:
        return []


# SAVE ORDERS
def save_orders(orders):
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=2)


# ORDER ROUTE
@app.route("/order", methods=["POST"])
def order():
    data = request.json

    # Save order locally
    orders = load_orders()
    orders.append(data)
    save_orders(orders)

    # Telegram message
    message = f"""
🐶 New Woolice Order

👤 Name: {data.get('name')}
📧 Email: {data.get('email')}
📝 Details: {data.get('details')}
"""

    send_telegram_message(message)

    print("SENDING TO TELEGRAM:", message)
    print("TOKEN:", BOT_TOKEN)
    print("CHAT:", CHAT_ID)

    return jsonify({"message": "Order received!"})


# GET ORDERS
@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify(load_orders())


if __name__=="__main__":
    app.run(host="0.0.0.0", port=10000, debug=True)