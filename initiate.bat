@echo off
setlocal enabledelayedexpansion

:: ============================================
:: Nome do arquivo de configuração
set VENV_DIR=.venv
set PYTHON_PATH=%VENV_DIR%\Scripts\python.exe
set REQUIREMENTS=requirements.txt
set APP_FILE=app.py

echo ============================================
echo Verificando ambiente Python e dependencias...

:: 1️⃣ Verifica se o ambiente virtual existe
if not exist "%PYTHON_PATH%" (
    echo \
    echo Ambiente virtual nao encontrado. Criando agora...
    echo ================================
    python -m venv .venv

    echo ================================
    echo Instalando dependencias...
    echo ================================
    "%PYTHON_PATH%" -m pip install -r "%REQUIREMENTS%"

    echo ================================
    echo Ambiente configurado com sucesso!
    echo /
)

call %VENV_DIR%\Scripts\activate

:: 2️⃣ Verifica se o PIP esta instalado corretamente
echo ============================================
echo Verificando se o pip esta disponivel...
"%PYTHON_PATH%" -m pip --version >nul 2>&1
if errorlevel 1 (
    echo Pip nao encontrado. Instalando...
    "%PYTHON_PATH%" -m ensurepip --upgrade
    "%PYTHON_PATH%" -m pip install --upgrade pip
)

:: 3️⃣ Pega lista exata das libs instaladas no venv
echo ============================================
echo Obtendo lista de pacotes instalados...
"%PYTHON_PATH%" -m pip list --format=freeze > installed.txt 2>nul


:: 4️⃣ Verifica cada dependencia com seguranca
echo ============================================
echo Verificando dependencias individualmente...

for /f "usebackq tokens=1 delims== eol=#" %%d in ("%REQUIREMENTS%") do (
    if not "%%d"=="" (
        findstr /i "%%d" installed.txt >nul 2>&1
        if errorlevel 1 (
            echo Instalando dependencia faltante: %%d
            bash -c "cat -A %%d"
            bash -c "sed -i 's/\r$//' %%d"
            bash -c "sed -i 's/[ \t]*$//' %%d"
            call "%PYTHON_PATH%" -m pip install %%d
        ) else (
            echo /t/t Dependencia %%d OK!
        )
    )
)

del installed.txt >nul 2>&1


:: 5 Cria o arquivo .env com a variável padrão
echo ============================================
echo Verificando a existencia do arquivo .env no ambiente...
if not exist .env (
    echo Arquivo nao encontrado, criando agora... 
    > .env type nul
    echo|set /p="GEMINI_API_KEY="sua_chave"" > .env
    bash -c "sed -i 's/\r$//' .env"
    bash -c "sed -i 's/[ \t]*$//' .env"

    echo Informe a sua chave da API do Gemini no arquivo .env, apos informada, basta:
    pause
)

:: 6 Por fim, iniciar o app
:RUN
echo ============================================
echo Iniciando o projeto Flask...
echo ============================================
"%PYTHON_PATH%" "project\%APP_FILE%"

pause
endlocal
