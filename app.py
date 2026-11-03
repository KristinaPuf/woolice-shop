import json
import os

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)

# Dozvoljeni sajtovi koji smeju da šalju porudžbine (GitHub Pages + Render)
CORS(app, origins=[
    "https://kristinapuf.github.io",
    os.getenv("RENDER_EXTERNAL_URL", ""),
])

ORDERS_FILE = "orders.json"

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")


@app.route("/")
def index():
    return send_from_directory(".", "index.html")


def send_telegram_message(message):
    if not BOT_TOKEN or not CHAT_ID:
        print("Telegram not configured")
        return

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        requests.post(url, data={"chat_id": CHAT_ID, "text": message}, timeout=10)
    except requests.RequestException as e:
        print("Telegram error:", type(e).__name__)  # bez tokena u logovima


def load_orders():
    try:
        with open(ORDERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_orders(orders):
    with open(ORDERS_FILE, "w", encoding="utf-8") as f:
        json.dump(orders, f, indent=2, ensure_ascii=False)


@app.route("/order", methods=["POST"])
def order():
    data = request.get_json(silent=True) or {}

    name = str(data.get("name", "")).strip()[:100]
    email = str(data.get("email", "")).strip()[:150]
    details = str(data.get("details", "")).strip()[:2000]

    if not name or "@" not in email or not details:
        return jsonify({"message": "Please fill in all fields."}), 400

    clean = {"name": name, "email": email, "details": details}

    orders = load_orders()
    orders.append(clean)
    save_orders(orders)

    send_telegram_message(
        f"🐶 New Woolice Order\n\n"
        f"👤 Name: {name}\n"
        f"📧 Email: {email}\n"
        f"📝 Details: {details}"
    )

    return jsonify({"message": "Order received!"})


# Ruta /orders je namerno uklonjena: bila je javna i prikazivala je
# imena i mejlove kupaca svakome ko otvori adresu.


if __name__ == "__main__":
    port = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)