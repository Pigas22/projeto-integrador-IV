from sqlalchemy import (
    create_engine, select, asc, desc, update, delete,
    text, Date, cast, func, String, literal, literal_column
)

from sqlalchemy.orm import (
    sessionmaker, aliased, join, contains_eager
)

from  flask import render_template, url_for,app,request, Flask,flash,redirect
from backend.models import Usuario, Medico, SessionLocal,Consulta
app = Flask(__name__)
session=SessionLocal()
pac=aliased(Usuario,name='pac')
med=aliased(Medico,name='med')
con=aliased(Consulta,name='con')

@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        try:
            # Busca o usuário pelo email
            usuario = session.query(Usuario).filter(Usuario.email == email).first()
            
            if usuario and usuario.senha == senha:  # Em produção, use hash de senha!
                # Salva informações na sessão
                session['usuario_id'] = pac.id
                session['usuario_nome'] = pac.nome
                session['usuario_email'] = pac.email
                
                flash(f'Bem-vindo(a), {usuario.nome}!', 'success')
                return redirect(url_for('home.html'))
            else:
                flash('Email ou senha incorretos.', 'danger')
                
        except Exception as e:
            print(f'Erro ao fazer login: {e}')
            flash('Erro ao processar login. Tente novamente.', 'danger')
    
    return render_template('login.html')

@app.route('/criacao_usuarios')
def criacao_usuarios():
    cpf=request.args.get('cpf')
    nome=request.args.get('nome')
    email=request.args.get('email')
    senha=request.args.get('senha')
    comorbidades=request.args.get('comorbidades')
    try:
        novo_usuario=pac(
            cpf=id,
            nome=nome,
            email=email,
            senha=senha,
            comorbidades=comorbidades
        )
        session.add(novo_usuario)
        session.commit()
    except Exception as e:
        print(f'Erro ao criar usuario: {e}')
    return render_template(
        'criacao_usuarios.html',
        cpf=id,
        nome=nome,
        email=email,
        senha=senha,
        comorbidades=comorbidades
    )

@app.route('/criacao_medicos')
def criacao_medicos():
    nome=request.args.get('nome')
    especialidade=request.args.get('especialidade')
    crm=request.args.get('crm')

    try:
        novo_medico=med(
            nome=nome,
            especialidade=especialidade,
            crm=crm
        )
        session.add(novo_medico)
        session.commit()
    except Exception as e:
        print(f'Erro ao cadastrar médico: {e}')
    return render_template(
        'cadastro-medico.html',
        nome=nome,
        especialidade=especialidade,
        crm=crm )

@app.route('/listar_usuarios')
def listar_usuarios():
    nome=request.args.get('nome','todos')
    try:
        sql=(
            session.query(
                pac.nome.label('NomePaciente'),
                pac.email.label('EmailPaciente'),
                pac.comorbidades.label('ComorbidadesPaciente')
            ).select_from(pac)
        )

        if nome!='todos':
            sql=sql.filter(pac.nome==nome)
        sql=sql.order_by(pac.nome.asc())
        resultado=sql.all()
    except Exception as e:
        print(f'Erro ao listar usuarios:{e}')
        resultado=[]
    return render_template(
        'listar_usuarios.html',
        nome=nome,
        resultado=resultado
    )

@app.route('/listar_medicos')
def listar_medicos():
    especialidade=request.args.get('especialidade','todos')
    try:
        sql=(
            session.query(
                med.nome.label('NomeMedico'),
                med.especialidade.label('Especialidade'),
                med.crm.label('CRM')    
            ).select_from(med)
        )

        if especialidade!='todos':
            sql=sql.filter(med.especialidade==especialidade)
        sql=sql.order_by(med.nome.asc())
        resultado=sql.all() 
    except Exception as e:
        print(f'Erro ao listar medicos:{e}')
        resultado=[]    
    return render_template(
        'listar_medicos.html',
        especialidade=especialidade,
        resultado=resultado)
    
@app.route('/listar_consultas')
def listar_consultas():
    nome=request.args.get('nome','todos')
    try:
        sql=(
            session.query(
                con.id.label('IDConsulta'),
                pac.nome.label('NomePaciente'),
                med.nome.label('NomeMedico'),
                con.data_hora.label('DataHora'),
                con.sintomas.label('Sintomas')  
            ).select_from(con)
            .outerjoin(pac,con.id_usuario==pac.id)
            .outerjoin(med,med.id==con.id_medico)
        )
        if nome!='todos':
            sql=sql.filter(pac.nome==nome)
        sql=sql.order_by(con.data_hora.asc())
        resultado=sql.all() 
    except Exception as e:
        print(f'Erro ao listar consultas:{e}')
        resultado=[]    
    return render_template(
        'listar_consultas.html',
        nome=nome,
        resultado=resultado)





if __name__ == "__main__":
    app.run(debug=True)  # inicia o servidor Flask em modo debug


