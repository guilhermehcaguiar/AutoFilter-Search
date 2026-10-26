@echo off
setlocal
title Sistema Atend-Car - Filtros
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo Criando ambiente virtual...
    python -m venv .venv
    if errorlevel 1 goto erro
)

".venv\Scripts\python.exe" -c "import streamlit, pandas" >nul 2>&1
if errorlevel 1 goto instalar
".venv\Scripts\python.exe" -m pip check >nul 2>&1
if errorlevel 1 goto instalar
goto iniciar

:instalar
echo Instalando ou reparando dependencias. Esta etapa precisa de internet.
".venv\Scripts\python.exe" -m ensurepip --upgrade
if errorlevel 1 goto erro
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto erro
".venv\Scripts\python.exe" -m pip check
if errorlevel 1 goto erro

:iniciar
echo Iniciando o sistema...
".venv\Scripts\python.exe" -m streamlit run app.py
if errorlevel 1 goto erro
exit /b 0

:erro
echo [ERRO] Nao foi possivel preparar ou iniciar o sistema.
pause
exit /b 1
