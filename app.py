from flask import Flask, jsonify, render_template, request

from chatbot import FAQBot

app = Flask(__name__)
bot = FAQBot("faqs.json")


@app.route("/")
def home():
    return render_template("index.html", suggestions=bot.suggest(5))


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json(silent=True) or {}
    return jsonify(bot.ask(data.get("message", "")))


if __name__ == "__main__":
    app.run(debug=True)