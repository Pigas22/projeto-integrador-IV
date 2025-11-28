from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./project/backend/banco.db" # aqui a gnt cria o banco no diretorio

engine=create_engine(
    DATABASE_URL,
    echo=False,#ele false é quando nao é para aparecer no terminal
    future=True
)

#base do orm sqllachemy
Base=declarative_base()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)#aqui chama o session, que precisa para fazer as operações no banco

class Usuario(Base):
    __tablename__='usuario'

    cpf=Column(Integer,primary_key=True)
    nome=Column(String,nullable=False)
    nome_usuario=Column(String)
    email=Column(String,nullable=False)
    senha=Column(String,nullable=False)
    comorbidades=Column(String)

class Medico(Base):
    __tablename__='medico'

    id=Column(Integer,primary_key=True,autoincrement=True)
    nome=Column(String,nullable=False)
    especialidade=Column(String,nullable=False)
    crm=Column(String,nullable=False)

class Consulta(Base):
    __tablename__='consulta'

    id=Column(Integer,primary_key=True,autoincrement=True)
    id_usuario=Column(Integer,nullable=False)
    id_medico=Column(Integer,nullable=False)
    data_hora=Column(String,nullable=False)
    sintomas=Column(String,nullable=False)


Base.metadata.create_all(engine) #cria as tabelas no banco, caso nao existam ainda
