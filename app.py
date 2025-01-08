from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@127.0.0.1:3306/pront_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro')
def cadastro():
    return render_template('cadastro.html')

@app.route('/pacientes')
def pacientes():
    return render_template('pacientes.html')

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Cria as tabelas no banco de dados
    app.run(debug=True)
