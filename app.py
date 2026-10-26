import streamlit as st
import pandas as pd
from datetime import datetime
import os
from html import escape
from catalogos import (
    localizar_csv, normalizar_catalogo, ler_conversoes, filtrar_por_ano,
    filtrar_por_litragem, ANO_NAO_INFORMADO, LITRAGEM_NAO_INFORMADA, TODAS_LITRAGENS,
)

# ─── CONFIG ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sistema Atend-Car",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── ESTILOS (TEMA DINÂMICO E OCULTAÇÃO DE MENUS) ─────────────────────────────
st.markdown("""
<style>


#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

html, body, [class*="css"] {
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
}

:root {
    --bg-app: #f0f2f6;
    --bg-card: #ffffff;
    --text-title: #1a1d27;
    --text-sub: #6b7080;
    --border-line: #dee2e6;
    --step-todo-bg: #e0e2e6;
    --step-todo-text: #6b7080;
}

@media (prefers-color-scheme: dark) {
    :root {
        --bg-app: #0f1117;
        --bg-card: #1a1d27;
        --text-title: #ffffff;
        --text-sub: #8b8fa8;
        --border-line: #2a2d3a;
        --step-todo-bg: #2a2d3a;
        --step-todo-text: #555870;
    }
}

.stApp { background-color: var(--bg-app); }

.main-header {
    background: var(--bg-card);
    border-bottom: 3px solid #2ecc71;
    padding: 1.5rem 2rem;
    margin: -1rem -1rem 2rem -1rem;
    display: flex; align-items: center; gap: 1rem;
}
.main-header h1 {
    font-weight: 900; color: var(--text-title);
    margin: 0; letter-spacing: -0.02em; text-transform: uppercase;
    font-size: 2.2rem;
}
.main-header .subtitle {
    font-size: 0.85rem; font-weight: 500; color: var(--text-sub); margin: 0;
    letter-spacing: 0.1em; text-transform: uppercase;
}
.logo-icon { font-size: 2.5rem; line-height: 1; }

.menu-card {
    background: var(--bg-card); border: 2px solid var(--border-line);
    border-radius: 12px; padding: 2rem 1.5rem; text-align: center;
    transition: all 0.3s ease; height: 100%;
}
.menu-card:hover { border-color: #2ecc71; transform: translateY(-5px); }
.menu-icon { font-size: 3rem; margin-bottom: 1rem; display: block; }
.menu-title { font-weight: 800; font-size: 1.5rem; color: var(--text-title); margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: -0.02em;}
.menu-desc { color: var(--text-sub); font-size: 0.9rem; font-weight: 400; margin-bottom: 1.5rem; }

.steps-bar {
    display: flex; align-items: center; margin-bottom: 2rem;
    background: var(--bg-card); border-radius: 12px;
    padding: 1rem 1.5rem; border: 1px solid var(--border-line);
    overflow-x: auto; white-space: nowrap;
}
.step-item { display: flex; align-items: center; gap: 0.5rem; flex: 1; }
.step-num { width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 0.8rem; flex-shrink: 0; }
.step-num.done, .step-num.active { background: #2ecc71; color: #ffffff; }
.step-num.todo { background: var(--step-todo-bg); color: var(--step-todo-text); }
.step-label { font-size: 0.75rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em; }
.step-label.done { color: #2ecc71; }
.step-label.active { color: var(--text-title); }
.step-label.todo { color: var(--step-todo-text); }
.step-arrow { color: var(--border-line); font-size: 1rem; margin: 0 0.5rem; }

.select-title { font-weight: 800; font-size: 1.1rem; color: #2ecc71; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.3rem; }
.stSelectbox > div > div { background-color: var(--bg-card) !important; border: 2px solid var(--border-line) !important; border-radius: 8px !important; color: var(--text-title) !important; font-size: 1rem !important; font-weight: 500 !important; }
.orange-divider { height: 3px; background: linear-gradient(90deg, #2ecc71, transparent); border: none; margin: 1.5rem 0; border-radius: 2px; }

.stButton > button { font-weight: 700 !important; font-size: 0.95rem !important; text-transform: uppercase !important; letter-spacing: 0.05em !important; padding: 0.6rem 2rem !important; border-radius: 8px !important; transition: all 0.2s !important; }
.btn-voltar > button { background: var(--bg-card) !important; border: 2px solid var(--border-line) !important; color: var(--text-title) !important; width: auto !important; margin-bottom: 1rem !important;}
.btn-voltar > button:hover { border-color: #2ecc71 !important; color: #2ecc71 !important; }

.summary-bar { background: var(--bg-card); border: 1px solid var(--border-line); border-radius: 10px; padding: 1rem 1.4rem; margin-bottom: 1.5rem; display: flex; gap: 2rem; flex-wrap: wrap; }
.summary-item { display: flex; flex-direction: column; gap: 0.15rem; }
.summary-key { font-size: 0.7rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.08em; color: #2ecc71; }
.summary-val { font-size: 0.95rem; font-weight: 600; color: var(--text-title); }
.no-result { background: var(--bg-card); border: 1px dashed var(--border-line); border-radius: 10px; padding: 2rem; text-align: center; color: var(--text-sub); font-style: italic; }

::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg-app); }
::-webkit-scrollbar-thumb { background: var(--border-line); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #2ecc71; }
</style>
""", unsafe_allow_html=True)


# ─── FUNÇÕES UTILITÁRIAS E CARREGAMENTO ───────────────────────────────────────
@st.cache_data
def _carregar_catalogo(conteudo, nome, ano_atual, complemento):
    return normalizar_catalogo(conteudo, nome, ano_atual, complemento)


def carregar_dados(arquivo_csv):
    caminho = localizar_csv(arquivo_csv, os.path.dirname(__file__))
    if caminho is None:
        return None, f"Arquivo {arquivo_csv} não encontrado."
    try:
        # O conteúdo faz parte da chave do cache: alterações no CSV são lidas imediatamente.
        motores = localizar_csv("cilindradas.csv", os.path.dirname(__file__)) if arquivo_csv == "catalogo.csv" else None
        complemento = motores.read_bytes() if motores else b""
        return _carregar_catalogo(caminho.read_bytes(), arquivo_csv, datetime.now().year, complemento), None
    except (ValueError, OSError, UnicodeError, pd.errors.ParserError) as exc:
        return None, f"Não foi possível carregar {arquivo_csv}: {exc}"


@st.cache_data
def _carregar_conversoes(conteudo):
    return ler_conversoes(conteudo)


def carregar_conversoes():
    caminho = localizar_csv("conversao.csv", os.path.dirname(__file__))
    if caminho is None:
        st.warning("Arquivo de conversões não encontrado. As referências Wega continuam disponíveis.")
        return {}
    try:
        return _carregar_conversoes(caminho.read_bytes())
    except (ValueError, OSError, UnicodeError) as exc:
        st.warning(f"Não foi possível carregar as conversões Tecfil: {exc}")
        return {}

def gerar_anos(row):
    if not row["Periodo_Informado"]:
        return []
    return range(int(row["Ano_Inicio_Int"]), int(row["Ano_Fim_Int"]) + 1)

# ─── NAVEGAÇÃO E ESTADO ────────────────────────────────────────────────────────
if "pagina" not in st.session_state: st.session_state.pagina = "home"
if "step" not in st.session_state: st.session_state.step = 1

CAMPOS = ["montadora", "modelo", "ano", "classificacao", "transmissao"]
WIDGETS = ["sel_montadora", "sel_modelo", "sel_ano", "sel_versao", "sel_transmissao"]


def limpar_dependentes(nivel, limpar_litragem=True):
    # Executado como callback, antes da criação dos widgets na próxima renderização.
    for chave in CAMPOS[nivel:] + WIDGETS[nivel:] + ["sel_trans_auto"]:
        st.session_state.pop(chave, None)
    if nivel <= 3 and limpar_litragem:
        st.session_state.pop("sel_litragem", None)
    st.session_state.step = nivel + 1


def reset():
    limpar_dependentes(0)
    st.session_state.pop("mostrar_litragem", None)


def ir_para(pagina):
    reset()
    st.session_state.pagina = pagina

# ─── HEADER ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <span class="logo-icon">🔧</span>
    <div>
        <h1>Sistema Atend-Car</h1>
        <p class="subtitle">Catálogo Técnico Integrado para Oficinas</p>
    </div>
</div>
""", unsafe_allow_html=True)


# ==============================================================================
# TELA INICIAL (MENU)
# ==============================================================================
if st.session_state.pagina == "home":
    st.markdown("<h2 style='text-align: center; font-weight: 900; color: var(--text-title); margin-bottom: 2rem; letter-spacing: -0.02em;'>O QUE VOCÊ DESEJA CONSULTAR HOJE?</h2>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="large")

    with col1:
        st.markdown("""
        <div class="menu-card">
            <span class="menu-icon">🛢️</span>
            <div class="menu-title">Revisão Básica</div>
            <div class="menu-desc">Filtros de Ar, Óleo, Combustível e Cabine</div>
        </div>
        """, unsafe_allow_html=True)
        st.button("Consultar Filtros", use_container_width=True, key="btn_rev", on_click=ir_para, args=("filtros",))

    with col2:
        st.markdown("""
        <div class="menu-card">
            <span class="menu-icon">🌧️</span>
            <div class="menu-title">Palhetas</div>
            <div class="menu-desc">Limpadores Dianteiros, Traseiros e Encaixes</div>
        </div>
        """, unsafe_allow_html=True)
        st.button("Consultar Palhetas", use_container_width=True, key="btn_palh", on_click=ir_para, args=("palhetas",))

    with col3:
        st.markdown("""
        <div class="menu-card" style="opacity: 0.8;">
            <span class="menu-icon">⚙️</span>
            <div class="menu-title">Câmbio</div>
            <div class="menu-desc">Fluidos e Filtros de Transmissão (WFC/WFCK)</div>
        </div>
        """, unsafe_allow_html=True)
        st.button("Consultar Câmbio", use_container_width=True, key="btn_cam", on_click=ir_para, args=("cambio",))

# ==============================================================================
# TELAS DE CONSULTA
# ==============================================================================
elif st.session_state.pagina in ["filtros", "palhetas", "cambio"]:

    is_cambio = st.session_state.pagina == "cambio"

    if st.session_state.pagina == "filtros":
        arquivo = "catalogo.csv"
        titulo_pagina = "🛢️ CONSULTA DE REVISÃO (FILTROS)"
        label_resultado = "Peças"
        passo_final = 5
    elif st.session_state.pagina == "palhetas":
        arquivo = "palhetas.csv"
        titulo_pagina = "🌧️ CONSULTA DE PALHETAS"
        label_resultado = "Peças"
        passo_final = 5
    else:
        arquivo = "cambio.csv"
        titulo_pagina = "⚙️ CONSULTA DE FILTROS DE CÂMBIO"
        label_resultado = "Filtros do Câmbio"
        passo_final = 6

    dict_conversoes = carregar_conversoes()

    st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
    st.button("⬅️ Voltar ao Menu Inicial", key="voltar_cons", on_click=ir_para, args=("home",))
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown(f"<h2 style='color: var(--text-title); font-weight: 900; margin-top: -1rem; margin-bottom: 1.5rem; letter-spacing: -0.02em;'>{titulo_pagina}</h2>", unsafe_allow_html=True)

    df, erro = carregar_dados(arquivo)
    if erro: st.error(f"❌ {erro}"); st.stop()
    avisos = df.attrs.get("avisos", [])
    if avisos:
        with st.expander(f"⚠️ {len(avisos)} avisos sobre os dados do catálogo"):
            for aviso in avisos:
                st.write(aviso)

    if is_cambio:
        etapas = ["Montadora", "Modelo", "Ano", "Versão", "Transmissão", label_resultado]
    else:
        etapas = ["Montadora", "Modelo", "Ano", "Versão", label_resultado]

    def step_class(i):
        s = st.session_state.step
        if i + 1 < s:  return "done"
        if i + 1 == s: return "active"
        return "todo"

    barra_etapas = st.empty()

    col_sel, col_res = st.columns([1, 1.4], gap="large")

    with col_sel:
        st.markdown('<div class="select-title">① Montadora</div>', unsafe_allow_html=True)
        montadoras = sorted(df["Nome_Montadora"].dropna().unique().tolist())
        montadora_sel = st.selectbox("Montadora", ["— Selecione —"] + montadoras, label_visibility="collapsed", key="sel_montadora", on_change=limpar_dependentes, args=(1,))

        if montadora_sel != "— Selecione —":
            st.session_state.montadora = montadora_sel
            if st.session_state.step < 2: st.session_state.step = 2
        else: st.session_state.step = 1

        st.markdown('<hr class="orange-divider">', unsafe_allow_html=True)

        st.markdown('<div class="select-title">② Modelo</div>', unsafe_allow_html=True)
        if st.session_state.step >= 2:
            df_m = df[df["Nome_Montadora"] == st.session_state.montadora]
            modelos = sorted(df_m["Nome_Modelo"].dropna().unique().tolist())
            modelo_sel = st.selectbox("Modelo", ["— Selecione —"] + modelos, label_visibility="collapsed", key="sel_modelo", on_change=limpar_dependentes, args=(2,))
            if modelo_sel != "— Selecione —":
                st.session_state.modelo = modelo_sel
                if st.session_state.step < 3: st.session_state.step = 3
            elif st.session_state.step > 2:
                st.session_state.step = 2
                for k in ["modelo","ano","classificacao", "transmissao"]: st.session_state.pop(k, None)
        else:
            st.selectbox("Modelo", ["— Selecione primeiro a montadora —"], disabled=True, label_visibility="collapsed")

        st.markdown('<hr class="orange-divider">', unsafe_allow_html=True)

        st.markdown('<div class="select-title">③ Ano</div>', unsafe_allow_html=True)
        if st.session_state.step >= 3:
            df_mod = df_m[df_m["Nome_Modelo"] == st.session_state.modelo]
            anos_set = set()
            for _, row in df_mod.iterrows(): anos_set.update(gerar_anos(row))
            anos_disp = sorted(anos_set, reverse=True)

            opcoes_anos = [str(a) for a in anos_disp]
            if (~df_mod["Periodo_Informado"]).any():
                opcoes_anos.append(ANO_NAO_INFORMADO)
            ano_sel = st.selectbox("Ano", ["— Selecione —"] + opcoes_anos, label_visibility="collapsed", key="sel_ano", on_change=limpar_dependentes, args=(3,))
            if ano_sel != "— Selecione —":
                st.session_state.ano = ano_sel if ano_sel == ANO_NAO_INFORMADO else int(ano_sel)
                if st.session_state.step < 4: st.session_state.step = 4
            elif st.session_state.step > 3:
                st.session_state.step = 3
                for k in ["ano","classificacao", "transmissao"]: st.session_state.pop(k, None)
        else:
            st.selectbox("Ano", ["— Selecione primeiro o modelo —"], disabled=True, label_visibility="collapsed")

        st.markdown('<hr class="orange-divider">', unsafe_allow_html=True)

        if st.session_state.step >= 4:
            df_ano = filtrar_por_ano(df_mod, st.session_state.ano)

        if st.session_state.pagina != "palhetas":
            if st.session_state.step >= 4:
                litragens = sorted({v for valores in df_ano["Litragens_Motor"] for v in valores}, key=float)
                sem_litragem = df_ano["Litragens_Motor"].apply(lambda valores: not valores).any()
                opcoes = [TODAS_LITRAGENS] + litragens if litragens else []
                if sem_litragem:
                    opcoes.append(LITRAGEM_NAO_INFORMADA)
                litragem = st.selectbox("Cilindrada do motor", opcoes, key="sel_litragem",
                                       disabled=not litragens,
                                       format_func=lambda valor: f"{valor} L" if valor in litragens else valor,
                                       on_change=limpar_dependentes, args=(3, False))
                if not litragens:
                    st.caption("Cilindrada ainda não cadastrada para esta aplicação.")
                df_ano = filtrar_por_litragem(df_ano, litragem)
            else:
                st.selectbox("Cilindrada do motor", ["Selecione primeiro o ano"],
                             disabled=True, key="sel_litragem")
            st.markdown('<hr class="orange-divider">', unsafe_allow_html=True)

        st.markdown('<div class="select-title">④ Versão / Especificação</div>', unsafe_allow_html=True)
        if st.session_state.step >= 4:
            versoes = sorted(df_ano["Classificacao_Modelo"].replace("", "Versão Única / Padrão").unique().tolist())

            versao_sel = st.selectbox("Versão", ["— Selecione —"] + versoes, label_visibility="collapsed", key="sel_versao", on_change=limpar_dependentes, args=(4,))
            if versao_sel != "— Selecione —":
                st.session_state.classificacao = versao_sel if versao_sel != "Versão Única / Padrão" else ""
                st.session_state.step = 5
            elif st.session_state.step > 4:
                st.session_state.step = 4
                for k in ["classificacao", "transmissao"]: st.session_state.pop(k, None)
        else:
            st.selectbox("Versão", ["— Selecione primeiro o ano —"], disabled=True, label_visibility="collapsed")

        # ─── CAMPO EXCLUSIVO DE CÂMBIO ───
        if is_cambio:
            st.markdown('<hr class="orange-divider">', unsafe_allow_html=True)
            st.markdown('<div class="select-title">⑤ Modelo da Transmissão</div>', unsafe_allow_html=True)
            if st.session_state.step >= 5:
                filtro_class = df_ano["Classificacao_Modelo"].replace("nan","").fillna("") == st.session_state.classificacao
                if st.session_state.classificacao == "":
                    filtro_class = df_ano["Classificacao_Modelo"].isna() | (df_ano["Classificacao_Modelo"] == "") | (df_ano["Classificacao_Modelo"] == "nan")

                df_trans = df_ano[filtro_class]
                transmissoes = sorted(df_trans["Codigo_Cambio"].replace("", "Não informado no catálogo").unique().tolist())

                # Se só houver 1 transmissão disponível, seleciona-a automaticamente
                if len(transmissoes) == 1:
                    st.session_state.transmissao = "" if transmissoes[0] == "Não informado no catálogo" else transmissoes[0]
                    st.session_state.step = 6
                    st.selectbox("Transmissão", transmissoes, disabled=True, label_visibility="collapsed", key="sel_trans_auto")
                else:
                    trans_sel = st.selectbox("Transmissão", ["— Qual a transmissão do veículo? —"] + transmissoes, label_visibility="collapsed", key="sel_transmissao")
                    if trans_sel != "— Qual a transmissão do veículo? —":
                        st.session_state.transmissao = "" if trans_sel == "Não informado no catálogo" else trans_sel
                        st.session_state.step = 6
                    elif st.session_state.step > 5:
                        st.session_state.step = 5
                        st.session_state.pop("transmissao", None)
            else:
                st.selectbox("Transmissão", ["— Selecione primeiro a versão —"], disabled=True, label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)
        st.button("↺  Limpar Filtros", use_container_width=True, key="limpar_filtros", on_click=reset)

    html_steps = '<div class="steps-bar">'
    for i, label in enumerate(etapas):
        cls = step_class(i)
        num_icon = "✓" if cls == "done" or (st.session_state.step == passo_final and i == passo_final - 1) else str(i + 1)
        html_steps += f'<div class="step-item"><div class="step-num {cls}">{num_icon}</div><span class="step-label {cls}">{label}</span></div>'
        if i < len(etapas) - 1:
            html_steps += '<span class="step-arrow">›</span>'
    barra_etapas.markdown(html_steps + "</div>", unsafe_allow_html=True)

    with col_res:
        if is_cambio:
            st.markdown(f'<div class="select-title">⑥ Resultados: {label_resultado}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="select-title">⑤ Resultados: {label_resultado}</div>', unsafe_allow_html=True)

        if st.session_state.step < passo_final:
            passos_nomes = {1:"a montadora", 2:"o modelo", 3:"o ano", 4:"a versão", 5:"a transmissão"}
            prox = passos_nomes.get(st.session_state.step, "os dados")
            st.markdown(f"""
            <div class="no-result">
                <span style="font-size:2rem">🔍</span><br><br>
                Complete a seleção à esquerda.<br>
                <strong style="color:#2ecc71">Próximo passo:</strong> escolha {prox}.
            </div>
            """, unsafe_allow_html=True)
        else:
            filtro_class = df_ano["Classificacao_Modelo"] == st.session_state.classificacao
            df_res = df_ano[filtro_class]
            if is_cambio:
                df_res = df_res[df_res["Codigo_Cambio"] == st.session_state.transmissao]

            st.markdown(f"""
            <div class="summary-bar">
                <div class="summary-item">
                    <span class="summary-key">Montadora</span>
                    <span class="summary-val">{escape(st.session_state.montadora)}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-key">Veículo</span>
                    <span class="summary-val">{escape(st.session_state.modelo)} ({st.session_state.ano})</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if df_res.empty:
                st.markdown('<div class="no-result">⚠️ Nenhuma peça encontrada para esta combinação.</div>', unsafe_allow_html=True)
            else:
                colunas_pecas = {
                    "filtros": ["Filtro_Ar", "Filtro_Oleo", "Filtro_Combustivel", "Filtro_Cabine"],
                    "palhetas": ["Palheta_Motorista", "Palheta_Passageiro", "Palheta_Traseira", "Tipo_Gancho"],
                    "cambio": ["Filtro_Cambio", "Codigo_Cambio"],
                }[st.session_state.pagina]
                aplicacoes = df_res.drop_duplicates(subset=colunas_pecas + ["Litragens_Motor"])
                if len(aplicacoes) > 1:
                    st.info(
                        f"{len(aplicacoes)} aplicações possíveis para esta seleção. "
                        "Essas opções não confirmam configurações distintas do veículo. "
                        "Antes de escolher, confira o código do motor, o chassi ou a referência da peça instalada."
                    )

                def card(icone, tipo, codigo):
                    codigo_limpo = str(codigo).replace('\xa0', '').strip().upper()
                    if pd.isna(codigo) or codigo_limpo in ["", "NAN", "NONE"]:
                        return f'<div class="filter-card empty"><span class="filter-icon" style="opacity:.3">{icone}</span><div class="filter-type">{tipo}</div><div class="filter-code empty">Não disponível</div></div>'

                    if st.session_state.pagina == "filtros":
                        conv = dict_conversoes.get(codigo_limpo, "")
                        html_tec = f'<div class="filter-tecfil">⇄ TECFIL: {escape(conv)}</div>' if conv else ''
                        return f'<div class="filter-card"><span class="filter-icon">{icone}</span><div class="filter-type">{tipo}</div><div class="filter-code">{escape(str(codigo).strip())}</div>{html_tec}</div>'

                    if len(str(codigo)) > 20: fonte = "1.0rem"
                    elif len(str(codigo)) > 12: fonte = "1.2rem"
                    else: fonte = "1.6rem"

                    return f'<div class="filter-card"><span class="filter-icon">{icone}</span><div class="filter-type">{tipo}</div><div class="filter-code" style="font-size:{fonte};">{escape(str(codigo).strip())}</div></div>'

                estilo_cards = """
                <style>


                    .result-grid {
                        margin: 0;
                        font-family: 'Inter', system-ui, sans-serif;
                        -webkit-font-smoothing: antialiased;
                        -moz-osx-font-smoothing: grayscale;
                    }
                    .result-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }
                    .filter-card { background: #ffffff; border: 1px solid #dee2e6; border-radius: 12px; padding: 1.2rem 1.4rem; position: relative; overflow: hidden; }
                    .filter-card::before { content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: #2ecc71; }
                    .filter-card.empty::before { background: #dee2e6; }
                    .filter-icon { font-size: 1.4rem; display: block; margin-bottom: 0.4rem; }
                    .filter-type { font-size: 0.75rem; font-weight: 800; color: #6b7080; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 0.4rem; }
                    .filter-code { overflow-wrap: anywhere; font-size: 1.6rem; font-weight: 900; color: #1a1d27; letter-spacing: -0.02em; line-height: 1.3; transform: translateZ(0); }
                    .filter-code.empty { color: #6b7080; font-size: 1rem !important; font-weight: 500; font-style: italic; }
                    .filter-tecfil { font-size: 0.85rem; font-weight: 800; color: #e67e22; margin-top: 0.5rem; transform: translateZ(0); }

                    @media (prefers-color-scheme: dark) {
                        .filter-card { background: #1a1d27; border-color: #2a2d3a; }
                        .filter-card.empty::before { background: #2a2d3a; }
                        .filter-type { color: #8b8fa8; }
                        .filter-code { color: #ffffff; }
                        .filter-code.empty { color: #555870; }
                    }
                </style>
                <div class="result-grid">
                """

                for numero, (_, row) in enumerate(aplicacoes.iterrows(), 1):
                    if len(aplicacoes) > 1:
                        st.caption(f"Aplicação possível {numero}")
                    if row["Litragens_Motor"]:
                        st.caption("Motor: " + " / ".join(row["Litragens_Motor"]) + " L")
                    html_cards = estilo_cards
                    if st.session_state.pagina == "filtros":
                        html_cards += card("💨", "Filtro de Ar", row.get("Filtro_Ar"))
                        html_cards += card("🛢️", "Filtro de Óleo", row.get("Filtro_Oleo"))
                        html_cards += card("⛽", "Filtro Combustível", row.get("Filtro_Combustivel"))
                        html_cards += card("🌬️", "Filtro de Cabine", row.get("Filtro_Cabine"))
                    elif st.session_state.pagina == "palhetas":
                        html_cards += card("🚘", "Motorista", row.get("Palheta_Motorista"))
                        html_cards += card("💺", "Passageiro", row.get("Palheta_Passageiro"))
                        html_cards += card("🔙", "Traseira", row.get("Palheta_Traseira"))
                        html_cards += card("🪝", "Tipo de Encaixe", row.get("Tipo_Gancho"))
                    else:
                        html_cards += card("⚙️", "Filtros Necessários", row.get("Filtro_Cambio"))
                        html_cards += card("🔀", "Transmissão", row.get("Codigo_Cambio"))
                    st.html(html_cards + "</div>")

                versao_texto = st.session_state.classificacao if st.session_state.classificacao else "Versão Padrão"
                if st.session_state.pagina != "palhetas":
                    litragem = st.session_state.get("sel_litragem", TODAS_LITRAGENS)
                    if litragem != TODAS_LITRAGENS:
                        versao_texto += f" | Cilindrada: {litragem}" + (" L" if litragem != LITRAGEM_NAO_INFORMADA else "")
                if is_cambio:
                    versao_texto += f" | Câmbio: {st.session_state.transmissao}"

                st.markdown(f"""
                <div style="margin-top:0.5rem;padding:0.8rem 1.2rem;background:var(--bg-card);
                            border-radius:8px;border:1px solid var(--border-line);font-size:0.82rem;color:var(--text-sub);">
                    <span style="color:#2ecc71;font-weight:800;text-transform:uppercase;
                                 font-size:0.7rem;letter-spacing:0.05em;">Observações / Aplicação:</span><br>
                    <span style="color:var(--text-title); font-weight: 500;">{escape(versao_texto)}</span>
                </div>
                """, unsafe_allow_html=True)
