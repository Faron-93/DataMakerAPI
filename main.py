from flask import Flask, request, jsonify
from data_maker import csv_creator, pgsql_creator
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/generate": {"origins": "http://localhost:3000"}})

@app.route("/")
def home():
    return "hello world"

@app.route('/generate', methods=['POST'])
def generate():
    # try:
    data = request.get_json()
    print(data)
    data_type = data["data_type"]
    dictionary = data["dictionary"]
    table_name = data["table_name"]
    quantity = data["quantity"]
    lang = data["language"]
    if data_type == "PostgreSQL":
        datas = pgsql_creator(dictionary, table_name, quantity, lang)
    elif data_type == "csv":
        datas = csv_creator(dictionary, table_name, quantity, lang)
    return datas
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)