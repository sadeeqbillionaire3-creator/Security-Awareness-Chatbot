"""
Minimal Flask skeleton for the Security Awareness Chatbot.
Mirrors the pattern used in the FarmAI / MediLinguaAI projects:
Flask backend + Gemini API + simple JSON chat endpoint.

Also includes a WhatsApp Cloud API webhook so this bot can run as a
WhatsApp Business bot, not just a web app.

To run on Render:
1. pip install -r requirements.txt
2. Set env vars: GEMINI_API_KEY, WHATSAPP_VERIFY_TOKEN, WHATSAPP_ACCESS_TOKEN,
   WHATSAPP_PHONE_NUMBER_ID (see setup notes at the bottom of this file)
3. Fill in / verify contacts.py before deploying
"""

import os
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai

from knowledge_base import SYSTEM_PROMPT
from contacts import get_verified_contacts

app = Flask(__name__)
CORS(app)

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel(
    model_name="gemini-3-flash-preview",
    system_instruction=SYSTEM_PROMPT,
)

WHATSAPP_VERIFY_TOKEN = os.environ.get("WHATSAPP_VERIFY_TOKEN")
WHATSAPP_ACCESS_TOKEN = os.environ.get("WHATSAPP_ACCESS_TOKEN")
WHATSAPP_PHONE_NUMBER_ID = os.environ.get("WHATSAPP_PHONE_NUMBER_ID")
WHATSAPP_API_URL = f"https://graph.facebook.com/v21.0/{WHATSAPP_PHONE_NUMBER_ID}/messages"


@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        response = model.generate_content(user_message)
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/contacts", methods=["GET"])
def contacts():
    return jsonify(get_verified_contacts())


@app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "Security Awareness Chatbot API is running"})


@app.route("/webhook", methods=["GET"])
def whatsapp_verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == WHATSAPP_VERIFY_TOKEN:
        return challenge, 200
    return "Verification failed", 403


@app.route("/webhook", methods=["POST"])
def whatsapp_receive():
    data = request.get_json(force=True)

    try:
        entry = data["entry"][0]
        changes = entry["changes"][0]
        value = changes["value"]

        if "messages" not in value:
            return jsonify({"status": "ignored"}), 200

        message = value["messages"][0]
        from_number = message["from"]
        text = message.get("text", {}).get("body", "")

        if not text:
            send_whatsapp_message(from_number, "Sorry, I can only read text messages right now.")
            return jsonify({"status": "ok"}), 200

        ai_response = model.generate_content(text)
        send_whatsapp_message(from_number, ai_response.text)

    except (KeyError, IndexError):
        pass

    return jsonify({"status": "ok"}), 200


def send_whatsapp_message(to_number, message_text):
    headers = {
        "Authorization": f"Bearer {WHATSAPP_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to_number,
        "type": "text",
        "text": {"body": message_text},
    }
    response = requests.post(WHATSAPP_API_URL, headers=headers, json=payload)
    if response.status_code != 200:
        print(f"WhatsApp send failed: {response.status_code} {response.text}")
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))