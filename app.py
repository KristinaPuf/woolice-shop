#test change
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import json

app = Flask(_name_)
CORS(app)

ORDERS_FILE = "orders.json"

# TELEGRAM SETTINGS
BOT_TOKEN = "8637912065:AAG6x0A2Z8Oigt5MYaTjBxga878HMafy2iA
CHAT_ID = "7908028371"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": message
    })


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

👤 Name: {data['name']}
📧 Email: {data['email']}
📝 Details: {data['details']}
"""

    send_telegram_message(message)

    return jsonify({"message": "Order received!"})

# GET ORDERS
@app.route("/orders", methods=["GET"])
def get_orders():
    return jsonify(load_orders())

if _name_ == "_main_":
    app.run(host="0.0.0.0", port=10000, debug=True)