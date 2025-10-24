@echo off
setlocal enabledelayedexpansion

:: ============================================
:: Nome do arquivo de configuração
set CONFIG_FILE=_config.bat
set VENV_DIR=.venv
set PYTHON_PATH=%VENV_DIR%\Scripts\python.exe
set REQUIREMENTS=requirements.txt
set APP_FILE=app.py
:: ============================================

echo ============================================
echo Verificando ambiente Python e dependencias...
echo ============================================

:: 1️⃣ Verifica se o ambiente virtual existe
if not exist "%PYTHON_PATH%" (
    echo Ambiente virtual nao encontrado. Criando agora...
    call "%CONFIG_FILE%"
    goto RUN
)

:: 2️⃣ Verifica se o Flask está instalado dentro do venv
echo Verificando se o Flask esta instalado...
"%PYTHON_PATH%" -m pip show flask >nul 2>&1
if errorlevel 1 (
    echo Flask nao encontrado. Instalando dependencias...
    "%PYTHON_PATH%" -m pip install -r "%REQUIREMENTS%"
)

:: 3️⃣ Verifica se o requirements.txt foi alterado (opcional)
:: voce pode adicionar verificacao por hash aqui futuramente

:: 4️⃣ Tudo certo, iniciar o app
:RUN
echo ============================================
echo Iniciando o projeto Flask...
echo ============================================
"%PYTHON_PATH%" "project\%APP_FILE%"

pause
endlocal
