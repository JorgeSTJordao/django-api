from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv
import os

# Carrega as variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# URL base da sua API Django
DJANGO_API_URL = "http://localhost:8000/api"  # Ajuste conforme sua configuração

# Página inicial
@app.route('/')
def home():
    return render_template("index.html")

# Página para listar usuários
@app.route('/listar')
def listar_usuarios():
    try:
        response = requests.get(f"{DJANGO_API_URL}/users/")
        usuarios = response.json()
    except:
        usuarios = {"error": "Erro ao buscar usuários"}
    
    return render_template("listar_usuarios.html", usuarios=usuarios)

# Página para criar usuário
@app.route('/criar', methods=['GET', 'POST'])
def criar_usuario():
    resultado = None
    if request.method == 'POST':
        try:
            data = {
                'username': request.form.get('username'),
                'email': request.form.get('email'),
                'password': request.form.get('password')
            }
            response = requests.post(f"{DJANGO_API_URL}/users/", json=data)
            resultado = response.json()
        except Exception as e:
            resultado = {"error": str(e)}

    return render_template("criar_usuario.html", resultado=resultado)


# Página para buscar usuário específico
@app.route('/buscar', methods=['GET', 'POST'])
def buscar_usuario():
    resultado = None
    if request.method == 'POST':
        try:
            user_id = request.form.get('user_id')
            response = requests.get(f"{DJANGO_API_URL}/users/{user_id}")
            resultado = response.json()
        except Exception as e:
            resultado = {"error": str(e)}
    
    return render_template("buscar_usuario.html", resultado=resultado)

# Mantendo as rotas da API originais
@app.route('/api/users', methods=['GET'])
def get_users():
    try:
        response = requests.get(f"{DJANGO_API_URL}/users/")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()
        response = requests.post(f"{DJANGO_API_URL}/users/", json=data)
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_detail(user_id):
    try:
        response = requests.get(f"{DJANGO_API_URL}/users/{user_id}/")
        return jsonify(response.json()), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000) 