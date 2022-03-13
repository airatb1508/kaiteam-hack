from flask import Flask, request, jsonify
from static_analyzer.main import find_mistakes
import json

app = Flask(__name__)


@app.route("/analyze", methods = ["POST"])
def analyze():
    code = request.form.get("code")
    res = find_mistakes(code).to_json(orient='records')
    return res, 200, { "Access-Control-Allow-Origin": "*" }


if __name__ == "__main__":
    app.run()
