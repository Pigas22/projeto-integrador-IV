from sqlalchemy import (
    create_engine, select, asc, desc, update, delete,
    text, Date, cast, func, String, literal, literal_column
)

from sqlalchemy.orm import (
    sessionmaker, aliased, join, contains_eager
)

from flask import render_template, url_for, request, Flask, redirect
from backend.models import Usuario, Medico, SessionLocal, Consulta

app = Flask(__name__)

# Cria sessão do banco de dados
db_session = SessionLocal()

# Aliases para as tabelas
pac = aliased(Usuario, name='pac')
med = aliased(Medico, name='med')
con = aliased(Consulta, name='con')


@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        try:
            # Busca o usuário pelo email e senha diretamente no banco
            usuario = db_session.query(Usuario).filter(
                Usuario.email == email,
                Usuario.senha == senha
            ).first()
            
            if usuario:
                # Login bem-sucedido, redireciona para listagem
                return redirect(url_for('listar_consultas'))
            else:
                # Credenciais inválidas
                return render_template('login.html', erro='Email ou senha incorretos.')
                
        except Exception as e:
            print(f'Erro ao fazer login: {e}')
            return render_template('login.html', erro='Erro ao processar login.')
    
    return render_template('login.html')


@app.route('/criacao_usuarios', methods=['GET', 'POST'])
def criacao_usuarios():
    if request.method == 'POST':
        cpf = request.form.get('cpf')  # Mudado de args para form
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        comorbidades = request.form.get('comorbidades')
        
        try:
            novo_usuario = Usuario(  # Corrigido: usar Usuario, não pac
                cpf=cpf,  # Corrigido: era 'id'
                nome=nome,
                email=email,
                senha=senha,
                comorbidades=comorbidades
            )
            db_session.add(novo_usuario)
            db_session.commit()
            return redirect(url_for('listar_usuarios'))
        except Exception as e:
            db_session.rollback()
            print(f'Erro ao criar usuario: {e}')
            return render_template('criacao_usuarios.html', erro='Erro ao criar usuário.')
    
    return render_template('criacao_usuarios.html')


@app.route('/criacao_medicos', methods=['GET', 'POST'])
def criacao_medicos():
    if request.method == 'POST':
        nome = request.form.get('nome')  # Mudado de args para form
        especialidade = request.form.get('especialidade')
        crm = request.form.get('crm')

        try:
            novo_medico = Medico(  # Corrigido: usar Medico, não med
                nome=nome,
                especialidade=especialidade,
                crm=crm
            )
            db_session.add(novo_medico)
            db_session.commit()
            return redirect(url_for('listar_medicos'))
        except Exception as e:
            db_session.rollback()
            print(f'Erro ao cadastrar médico: {e}')
            return render_template('cadastro-medico.html', erro='Erro ao cadastrar médico.')
    
    return render_template('cadastro-medico.html')


@app.route('/listar_usuarios')
def listar_usuarios():
    nome = request.args.get('nome', 'todos')
    try:
        sql = (
            db_session.query(
                pac.nome.label('NomePaciente'),
                pac.email.label('EmailPaciente'),
                pac.comorbidades.label('ComorbidadesPaciente')
            ).select_from(pac)
        )

        if nome != 'todos':
            sql = sql.filter(pac.nome.like(f'%{nome}%'))  # Melhorado: busca parcial
        sql = sql.order_by(pac.nome.asc())
        resultado = sql.all()
    except Exception as e:
        print(f'Erro ao listar usuarios: {e}')
        resultado = []
    
    return render_template(
        'listar_usuarios.html',
        nome=nome,
        resultado=resultado
    )


@app.route('/listar_medicos')
def listar_medicos():
    especialidade = request.args.get('especialidade', 'todos')
    try:
        sql = (
            db_session.query(
                med.nome.label('NomeMedico'),
                med.especialidade.label('Especialidade'),
                med.crm.label('CRM')    
            ).select_from(med)
        )

        if especialidade != 'todos':
            sql = sql.filter(med.especialidade == especialidade)
        sql = sql.order_by(med.nome.asc())
        resultado = sql.all() 
    except Exception as e:
        print(f'Erro ao listar medicos: {e}')
        resultado = []
    
    return render_template(
        'listar_medicos.html',
        especialidade=especialidade,
        resultado=resultado
    )

    
@app.route('/listar_consultas')
def listar_consultas():
    nome = request.args.get('nome', 'todos')
    try:
        sql = (
            db_session.query(
                con.id.label('IDConsulta'),
                pac.nome.label('NomePaciente'),
                med.nome.label('NomeMedico'),
                con.data_hora.label('DataHora'),
                con.sintomas.label('Sintomas')  
            ).select_from(con)
            .outerjoin(pac, con.id_usuario == pac.id)
            .outerjoin(med, med.id == con.id_medico)
        )
        
        if nome != 'todos':
            sql = sql.filter(pac.nome.like(f'%{nome}%'))  # Melhorado: busca parcial
        sql = sql.order_by(con.data_hora.asc())
        resultado = sql.all() 
    except Exception as e:
        print(f'Erro ao listar consultas: {e}')
        resultado = []
    
    return render_template(
        'listar_consultas.html',
        nome=nome,
        resultado=resultado
    )


@app.teardown_appcontext
def shutdown_session(exception=None):
    """Fecha a sessão do banco ao final de cada requisição"""
    db_session.close()


if __name__ == "__main__":
    app.run(debug=True)  # inicia o servidor Flask em modo debug