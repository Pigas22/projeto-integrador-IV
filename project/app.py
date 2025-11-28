from sqlalchemy import asc
from sqlalchemy.orm import aliased
from flask import render_template, url_for, request, Flask, redirect, session
from backend.models import Usuario, Medico, Consulta, SessionLocal

app = Flask(__name__)
app.secret_key = "chave_super_secreta_123"

db_session = SessionLocal()

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
            usuario = db_session.query(Usuario).filter(
                Usuario.email == email,
                Usuario.senha == senha
            ).first()
            if usuario:
                session['usuario_id'] = usuario.id
                session['usuario_nome'] = usuario.nome
                return redirect(url_for('listar_consultas'))
            else:
                return render_template('login.html', erro='Email ou senha incorretos.')
        except Exception:
            return render_template('login.html', erro='Erro ao processar login.')
    return render_template('login.html')


@app.route('/criacao_usuarios', methods=['GET', 'POST'])
def criacao_usuarios():
    if request.method == 'POST':
        cpf = request.form.get('cpf')
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        comorbidades = request.form.get('comorbidades')
        try:
            if db_session.query(Usuario).filter(Usuario.cpf == cpf).first():
                return render_template('criacao_usuarios.html', erro='CPF já cadastrado.')
            if db_session.query(Usuario).filter(Usuario.email == email).first():
                return render_template('criacao_usuarios.html', erro='Email já cadastrado.')
            novo = Usuario(cpf=cpf, nome=nome, email=email, senha=senha, comorbidades=comorbidades)
            db_session.add(novo)
            db_session.commit()
            return redirect(url_for('login'))
        except Exception:
            db_session.rollback()
            return render_template('criacao_usuarios.html', erro='Erro ao criar usuário.')
    return render_template('criacao_usuarios.html')


@app.route('/listar_medicos')
def listar_medicos():
    especialidade = request.args.get('especialidade', 'todos')
    try:
        sql = db_session.query(
            med.id.label('IDMedico'),
            med.nome.label('NomeMedico'),
            med.especialidade.label('Especialidade'),
            med.crm.label('CRM')
        )
        if especialidade != 'todos':
            sql = sql.filter(med.especialidade == especialidade)
        sql = sql.order_by(med.nome.asc())
        resultado = sql.all()
    except Exception:
        resultado = []
    return render_template('listar_medicos.html', especialidade=especialidade, resultado=resultado)


@app.route('/listar_consultas')
def listar_consultas():
    nome = request.args.get('nome', 'todos')

    try:
        sql = (
            db_session.query(
                con.id.label('IDConsulta'),
                pac.nome.label('NomePaciente'),
                pac.cpf.label('CpfPaciente'),
                med.nome.label('NomeMedico'),
                con.data_hora.label('DataHora'),
                con.sintomas.label('Sintomas')
            )
            .select_from(con)
            .outerjoin(pac, con.id_usuario == pac.id)
            .outerjoin(med, con.id_medico == med.id)
        )

        if nome != 'todos' and nome.strip() != "":
            sql = sql.filter(pac.nome.ilike(f"%{nome}%"))

        sql = sql.order_by(con.data_hora.asc())
        resultado = sql.all()

    except Exception:
        resultado = []

    return render_template('listar_consultas.html', resultado=resultado, nome=nome)



@app.route('/criar_consulta', methods=['GET', 'POST'])
def criar_consulta():
    usuario_id = session.get('usuario_id')
    usuario_nome = session.get('usuario_nome')
    if not usuario_id:
        return redirect(url_for('login'))
    if request.method == 'POST':
        id_medico = request.form.get('id_medico')
        data_hora = request.form.get('data_hora')
        sintomas = request.form.get('sintomas')
        try:
            nova = Consulta(id_usuario=usuario_id, id_medico=id_medico, data_hora=data_hora, sintomas=sintomas)
            db_session.add(nova)
            db_session.commit()
            return redirect(url_for('listar_consultas'))
        except Exception:
            db_session.rollback()
            medicos = db_session.query(Medico).order_by(Medico.nome).all()
            return render_template('criar_consulta.html', erro='Erro ao criar consulta.', usuario_id=usuario_id, usuario_nome=usuario_nome, medicos=medicos)
    medicos = db_session.query(Medico).order_by(Medico.nome).all()
    return render_template('criar_consulta.html', usuario_id=usuario_id, usuario_nome=usuario_nome, medicos=medicos)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.close()


if __name__ == "__main__":
    app.run(debug=True)
