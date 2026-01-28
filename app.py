from flask import Flask, request, jsonify
from flask_cors import CORS
from PIL import Image, ImageDraw, ImageFont
import requests
import os
import uuid
from io import BytesIO

app = Flask(__name__)
CORS(app)

# Telegram credentials (environment variable use karna best practice hai)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID", "YOUR_CHAT_ID")

@app.route("/")
def home():
    return "Backend is running OK"

@app.route("/generate", methods=["POST"])
def generate():
    name = request.form.get("name")
    status = request.form.get("status")

    if not all([name, status]):
        return jsonify({"status": "error", "message": "Name and Status required"}), 400

    # Create image
    img = Image.new("RGB", (500, 300), color="white")
    draw = ImageDraw.Draw(img)

    try:
        font_big = ImageFont.truetype("DejaVuSans.ttf", 32)
        font_small = ImageFont.truetype("DejaVuSans.ttf", 24)
    except:
        font_big = font_small = ImageFont.load_default()

    draw.text((20, 40), f"Name: {id}", fill="black", font=font_big)
    draw.text((20, 120), f"Status: {pass}", fill="black", font=font_small)

    # Save to buffer instead of file
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    # Send to Telegram
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto"
    requests.post(url, data={"chat_id": CHAT_ID}, files={"photo": buffer})

    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run()