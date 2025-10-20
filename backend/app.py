from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PRODUTOS_PATH = os.path.join(BASE_DIR, "produtos.json")

with open(PRODUTOS_PATH, "r", encoding="utf-8") as f:
    produtos = json.load(f)

@app.route("/produto/<codigo>", methods=["GET"])
def get_produto(codigo):
    for p in produtos:
        if p["codigo"] == codigo:
            return jsonify(p)
    return jsonify({"erro": "Produto não encontrado"}), 404

@app.route("/venda", methods=["POST"])
def registrar_venda():
    data = request.json
    print(f"Venda recebida: {data}")
    return jsonify({"status": "OK"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000)
