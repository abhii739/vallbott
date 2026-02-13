from flask import Flask, render_template, request, jsonify
import random
import string

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

# more keywords supported
keywords = {
    "yes": ["yes", "y", "yeah", "yep", "sure", "ok"],
    "no": ["no", "n", "nope", "nah"]
}


def preprocess(text):
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text.split()


def reply(msg):
    if not msg:
        return random.choice(responses["default"])

    tokens = preprocess(msg)

    for key, words in keywords.items():
        if any(word in tokens for word in words):
            return random.choice(responses[key])

    return random.choice(responses["default"])


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()

    message = data.get("message", "")
    bot_reply = reply(message)

    return jsonify({"reply": bot_reply})


if __name__ == "__main__":
    app.run(debug=True)
