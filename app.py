from flask import Flask, render_template, request, jsonify
import random
import string
import os

app = Flask(__name__)

responses = {
    "yes": [
        "Yayyy! 💖 You said YES!",
        "Happy Valentine’s Day ❤️",
        "Let’s celebrate together! 🎉"
    ],
    "no": [
        "Please think again 🥺",
        "Are you sure? 🥺",
        "💔"
    ],
    "default": [
        "Type yes or no 😄"
    ]
}

keywords = {
    "yes": ["yes", "y", "yeah", "yep", "sure", "ok"],
    "no": ["no", "n", "nope", "nah"]
}


# ---------- text cleaning ----------
def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.split()


# ---------- chatbot logic ----------
def reply(msg):
    if not msg:
        return random.choice(responses["default"])

    tokens = preprocess(msg)

    for key, words in keywords.items():
        if any(word in tokens for word in words):
            return random.choice(responses[key])

    return random.choice(responses["default"])


# ---------- routes ----------
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)

    message = data.get("message", "")
    bot_reply = reply(message)

    return jsonify({"reply": bot_reply})


# ---------- run server ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # needed for Render/Heroku
    app.run(host="0.0.0.0", port=port, debug=True)
