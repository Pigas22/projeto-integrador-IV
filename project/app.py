from sqlalchemy import select,asc,desc,update,delete
from sqlalchemy.orm import create_engine, case, extract, and_, or_,text, Date,cast,select,func,String,outerjoin,desc,not_,exists,literal,literal_column,join,aliased
from  flask import render_template, url_for,app,request
from models import Usuario, Medico, SessionLocal,Consulta

session=SessionLocal()
pac=aliased(Usuario,name='pac')
med=aliased(Medico,name='med')
con=aliased(Consulta,name='con')

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/criacao_usuarios')
def criacao_usuarios():
    nome=request.args.get('nome')
    email=request.args.get('email')
    senha=request.args.get('senha')
    comorbidades=request.args.get('comorbidades')
    try:
        novo_usuario=pac(
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
        'criacao_medicos.html',
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

@app.route('listar_medicos')
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


