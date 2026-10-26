#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "$0")"

if [[ ! -x .venv/bin/python ]]; then
    echo "Criando ambiente virtual..."
    python3 -m venv .venv
fi

if ! .venv/bin/python -c 'import streamlit, pandas' >/dev/null 2>&1 ||
   ! .venv/bin/python -m pip check >/dev/null 2>&1; then
    echo "Instalando ou reparando dependências. Esta etapa precisa de internet."
    .venv/bin/python -m ensurepip --upgrade
    .venv/bin/python -m pip install -r requirements.txt
    .venv/bin/python -m pip check
fi

exec .venv/bin/python -m streamlit run app.py "$@"
