from flask import Flask, request, jsonify
from data_maker import csv_creator, pgsql_creator
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)
CORS(app, resources={r"/generate": {"origins": "http://46.41.149.164"}})

app = Flask(__name__)


@app.route("/")
def home():
    return "Random Data Maker in progress"


@app.route('/generate', methods=['POST'])
def generate():
    try:
        data = request.get_json()
        data_type = data["data_type"]
        dictionary = data["dictionary"]
        table_name = data["table_name"]
        quantity = data["quantity"]
        lang = data["language"]
        if quantity > 1000:
            datas = "max 1000 records"
        else:
            if data_type == "PostgreSQL":
                datas = pgsql_creator(dictionary, table_name, quantity, lang)
            elif data_type == "csv":
                datas = csv_creator(dictionary, table_name, quantity, lang)
        return datas

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__app__':
    app.run(host="0.0.0.0", port=5000, debug=True)

if not app.debug:
    handler = RotatingFileHandler('error.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)