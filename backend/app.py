from flask import Flask, jsonify, request
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# Carrega produtos
with open('produtos.json', 'r') as f:
    produtos = json.load(f)

@app.route('/produtos', methods=['GET'])
def listar_produtos():
    return jsonify(produtos)

@app.route('/adicionar-produto', methods=['POST'])
def adicionar_produto():
    data = request.get_json()
    codigo = data.get('codigo')
    for p in produtos:
        if p['codigo'] == codigo:
            p['quantidade'] = p.get('quantidade', 0) + 1
            with open('produtos.json', 'w') as f:
                json.dump(produtos, f, indent=2)
            return jsonify({'sucesso': True, 'produto': p})
    return jsonify({'sucesso': False, 'mensagem': 'Produto não encontrado'})

if __name__ == '__main__':
    # Host 0.0.0.0 permite que outros dispositivos na rede local acessem
    app.run(host='0.0.0.0', port=3000)
