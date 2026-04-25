@echo off
title Sistema Atend-Car - Filtros
echo Verificando ambiente e dependencias...

:: Entra na pasta do projeto
cd /d "%~dp0"

:: 1. Verifica se a pasta .venv existe. Se não existir, ele cria e instala tudo.
if not exist .venv (
    echo [AVISO] Ambiente virtual nao encontrado. Iniciando instalacao...
    echo [AVISO] Isso pode demorar uns 2 minutos e precisa de internet apenas agora.
    
    :: Cria o ambiente virtual
    python -m venv .venv
    
    :: Ativa e instala as dependencias
    call .venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install -r requirements.txt
    
    echo [OK] Instalacao concluida com sucesso!
) else (
    :: Se a pasta já existir, ele apenas ativa
    call .venv\Scripts\activate
)

:: 2. Inicia o sistema
echo [OK] Iniciando o sistema da oficina...
python -m streamlit run app.py

:: Se o sistema fechar por erro, a janela nao fecha sozinha
if %errorlevel% neq 0 (
    echo.
    echo [ERRO] Ocorreu um problema ao iniciar o sistema.
    pause
)