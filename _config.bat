@echo off
echo ================================
echo Criando ambiente virtual...
echo ================================
python -m venv .venv

echo ================================
echo Instalando dependencias...
echo ================================
".venv\Scripts\python.exe" -m pip install -r requirements.txt

echo ================================
echo Ambiente configurado com sucesso!
echo ================================
pause

@REM echo ================================
@REM echo Verificando se a instalacao do Streamlit funcionou...
@REM echo ================================
@REM ".venv\Scripts\python.exe" -m streamlit hello
@REM pause
