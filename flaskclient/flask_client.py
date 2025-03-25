from flask import Flask, request, jsonify, render_template
import requests
from dotenv import load_dotenv
import os
from urllib.parse import urlencode

# Carrega as variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configurações da API
DJANGO_API_URL = "http://localhost:8000/api"
OAUTH_TOKEN_URL = "http://localhost:8000/o/token/"

# Configurações do OAuth2
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

def get_oauth_token():
    """Obtém um token OAuth2 usando client credentials"""
    try:
        data = {
            'grant_type': 'client_credentials',
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'scope': 'read write'
        }
        
        print("Tentando obter token com:", data)  # Debug
        
        response = requests.post(
            OAUTH_TOKEN_URL,
            data=data,
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Accept': 'application/json'
            },
            verify=False  # Apenas para desenvolvimento
        )
        
        print(f"Status da resposta: {response.status_code}")  # Debug
        print(f"Headers da resposta: {response.headers}")  # Debug
        print(f"Conteúdo da resposta: {response.text}")  # Debug
        
        if response.status_code != 200:
            print(f"Erro na resposta: Status {response.status_code}")
            print(f"Resposta da API: {response.text}")
            return None
            
        token_data = response.json()
        if 'access_token' not in token_data:
            print("Token não encontrado na resposta")
            return None
            
        return token_data['access_token']
    except Exception as e:
        print(f"Erro ao obter token: {str(e)}")
        return None

def make_authenticated_request(method, url, **kwargs):
    """Faz uma requisição autenticada para a API"""
    token = get_oauth_token()
    if not token:
        return {"error": "Não foi possível obter o token de autenticação"}, 401
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    # Merge com headers existentes, se houver
    if 'headers' in kwargs:
        kwargs['headers'].update(headers)
    else:
        kwargs['headers'] = headers
    
    try:
        print(f"Fazendo requisição para {url} com headers:", headers)  # Debug
        response = requests.request(method, url, **kwargs)
        print(f"Status da resposta: {response.status_code}")  # Debug
        print(f"Conteúdo da resposta: {response.text}")  # Debug
        
        if response.status_code == 401:
            # Tenta renovar o token e fazer a requisição novamente
            token = get_oauth_token()
            if token:
                kwargs['headers']['Authorization'] = f'Bearer {token}'
                response = requests.request(method, url, **kwargs)
        
        return response.json(), response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {str(e)}")  # Debug
        return {"error": str(e)}, 500

# Página inicial
@app.route('/')
def home():
    return render_template("index.html")

# Página para listar usuários
@app.route('/listar')
def listar_usuarios():
    usuarios, status_code = make_authenticated_request('GET', f"{DJANGO_API_URL}/users/")
    return render_template("listar_usuarios.html", usuarios=usuarios)

# Página para criar usuário
@app.route('/criar', methods=['GET', 'POST'])
def criar_usuario():
    resultado = None
    if request.method == 'POST':
        data = {
            'name': request.form.get('name'),
            'age': request.form.get('age'),
            'ssn': request.form.get('ssn')
        }
        resultado, status_code = make_authenticated_request('POST', f"{DJANGO_API_URL}/users/create_user", json=data)
    return render_template("criar_usuario.html", resultado=resultado)

# Página para buscar usuário específico
@app.route('/buscar', methods=['GET', 'POST'])
def buscar_usuario():
    resultado = None
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        resultado, status_code = make_authenticated_request('GET', f"{DJANGO_API_URL}/users/{user_id}")
    return render_template("buscar_usuario.html", resultado=resultado)

# Rotas da API
@app.route('/api/users', methods=['GET'])
def get_users():
    return make_authenticated_request('GET', f"{DJANGO_API_URL}/users/")

@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    return make_authenticated_request('POST', f"{DJANGO_API_URL}/users/create_user", json=data)

@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user_detail(user_id):
    return make_authenticated_request('GET', f"{DJANGO_API_URL}/users/{user_id}")

if __name__ == '__main__':
    app.run(debug=True, port=5000) 