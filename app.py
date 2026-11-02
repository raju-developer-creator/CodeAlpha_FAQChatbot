import logging
import os
import threading
import webbrowser

import flask.cli
from flask import Flask, jsonify, render_template, request

from chatbot import FAQBot

# Flask banner + WARNING hide
flask.cli.show_server_banner = lambda *args, **kwargs: None
logging.getLogger("werkzeug").setLevel(logging.ERROR)

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
    # debug=True vunte Flask rendu sarlu run avtundi, anduke ee check
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        threading.Timer(1.5, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=True)