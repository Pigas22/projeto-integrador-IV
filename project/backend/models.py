from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./project/backend/banco.db"

engine = create_engine(DATABASE_URL, echo=False, future=True)
Base = declarative_base()
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf = Column(String, unique=True, nullable=False)
    nome = Column(String, nullable=False)
    nome_usuario = Column(String, unique=True)
    email = Column(String, unique=True, nullable=False)
    senha = Column(String, nullable=False)
    comorbidades = Column(String)

class Medico(Base):
    __tablename__ = 'medico'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String, nullable=False)
    especialidade = Column(String, nullable=False)
    crm = Column(String, nullable=False)

class Consulta(Base):
    __tablename__ = 'consulta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(Integer, nullable=False)
    id_medico = Column(Integer, nullable=False)
    data_hora = Column(String, nullable=False)
    sintomas = Column(String, nullable=False)

Base.metadata.create_all(engine)

session = SessionLocal()

medicos_fixos = [
    Medico(nome="João Pereira", especialidade="Cardiologia", crm="12345-SP"),
    Medico(nome="Maria Silva", especialidade="Pediatria", crm="98765-SP"),
    Medico(nome="Carlos Eduardo", especialidade="Ortopedia", crm="02211-RJ"),
    Medico(nome="Ana Beatriz", especialidade="Dermatologia", crm="99887-MG"),
    Medico(nome="Rafael Costa", especialidade="Neurologia", crm="55443-SP")
]

existe = session.query(Medico).first()

if not existe:
    session.add_all(medicos_fixos)
    session.commit()

session.close()
