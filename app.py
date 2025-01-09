from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/pront_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Pasta onde as fotos serão armazenadas

db = SQLAlchemy(app)

# Modelo do banco de dados
class Paciente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    cpf = db.Column(db.String(11), unique=True, nullable=False)
    rg = db.Column(db.String(12), unique=True, nullable=False)
    telefone = db.Column(db.String(15), nullable=False)
    cep = db.Column(db.String(8), nullable=False)
    endereco = db.Column(db.String(200), nullable=False)
    anotacoes = db.Column(db.Text, nullable=True)
    fotos = db.Column(db.Text, nullable=True)  # Coluna para armazenar os caminhos das fotos

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/pacientes')
def pacientes():
    pacientes = Paciente.query.all()
    return render_template('pacientes.html', pacientes=pacientes)

@app.route('/api/cadastrar', methods=['POST'])
def cadastrar():
    try:
        data = request.json
        nome = data['nome']
        cpf = data['cpf']
        rg = data['rg']
        telefone = data['telefone']
        cep = data['cep']
        endereco = data['endereco']
        anotacoes = data.get('anotacoes')

        print(f"Recebido: {data}")

        if Paciente.query.filter_by(cpf=cpf).first() is not None:
            return jsonify({'message': 'Erro: CPF já cadastrado!'}), 400

        if Paciente.query.filter_by(rg=rg).first() is not None:
            return jsonify({'message': 'Erro: RG já cadastrado!'}), 400

        novo_paciente = Paciente(
            nome=nome, cpf=cpf, rg=rg, telefone=telefone,
            cep=cep, endereco=endereco, anotacoes=anotacoes
        )
        db.session.add(novo_paciente)
        db.session.commit()

        print(f'Paciente Cadastrado: {nome}, CPF: {cpf}, RG: {rg}, Telefone: {telefone}, CEP: {cep}, Endereço: {endereco}, Anotações: {anotacoes}')
        return jsonify({'message': 'Paciente cadastrado com sucesso!'})
    
    except Exception as e:
        print(f"Erro ao cadastrar paciente: {e}")
        return jsonify({'message': 'Erro ao cadastrar paciente.'}), 400

@app.route('/api/editar/<int:id>', methods=['POST'])
def editar(id):
    try:
        data = request.json
        paciente = Paciente.query.get(id)
        if not paciente:
            return jsonify({'message': 'Paciente não encontrado.'}), 404

        paciente.cpf = data['cpf']
        paciente.rg = data['rg']
        paciente.telefone = data['telefone']
        paciente.cep = data['cep']
        paciente.endereco = data['endereco']
        paciente.anotacoes = data.get('anotacoes')

        db.session.commit()

        print(f'Paciente Atualizado: {paciente.nome}, CPF: {paciente.cpf}, RG: {paciente.rg}, Telefone: {paciente.telefone}, CEP: {paciente.cep}, Endereço: {paciente.endereco}, Anotações: {paciente.anotacoes}')
        return jsonify({'message': 'Dados do paciente atualizados com sucesso!'})
    
    except Exception as e:
        print(f"Erro ao atualizar paciente: {e}")
        return jsonify({'message': 'Erro ao atualizar paciente.'}), 400

@app.route('/api/upload/<int:id>', methods=['POST'])
def upload(id):
    try:
        if 'file' not in request.files:
            return jsonify({'message': 'Nenhum arquivo enviado.'}), 400
        file = request.files['file']
        if file.filename == '':
            return jsonify({'message': 'Nenhum arquivo selecionado.'}), 400

        paciente = Paciente.query.get(id)
        if not paciente:
            return jsonify({'message': 'Paciente não encontrado.'}), 404

        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        if paciente.fotos:
            paciente.fotos += f";{file_path}"
        else:
            paciente.fotos = file_path

        db.session.commit()
        print(f'Foto adicionada para o paciente {paciente.nome}: {file_path}')
        return jsonify({'message': 'Foto adicionada com sucesso!', 'file_path': file_path})
    
    except Exception as e:
        print(f"Erro ao adicionar foto: {e}")
        return jsonify({'message': 'Erro ao adicionar foto.'}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados, incluindo a nova coluna de fotos
    app.run(debug=True)
