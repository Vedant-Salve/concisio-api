from flask import Flask, request, jsonify
from text_summary import summarizer

import spacy
from spacy.cli import download

try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")


app = Flask(__name__)

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()
    raw_text = data.get("text")

    if not raw_text:
        return jsonify({"error": "No text provided"}), 400

    summary, _, _, _ = summarizer(raw_text)
    return jsonify({"summary": summary})

if __name__ == "__main__":
    app.run()
