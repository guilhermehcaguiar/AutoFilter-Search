import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
import os

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
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

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
def converter_ano(val):
    if pd.isna(val) or str(val).strip() in ["", "nan", "None"]: return None
    try:
        n = int(float(str(val).strip()))
        if n > 9999: return None
        if n < 100: return 1900 + n if n > 50 else 2000 + n
        return n
    except: return None

@st.cache_data
def carregar_dados(arquivo_csv):
    caminhos = [
        os.path.join(os.path.dirname(__file__), arquivo_csv),
        os.path.join(os.path.dirname(__file__), "data", arquivo_csv),
        arquivo_csv,
    ]
    csv_path = next((c for c in caminhos if os.path.exists(c)), None)

    if csv_path is None: return None, f"Arquivo {arquivo_csv} não encontrado."

    df = pd.read_csv(csv_path, sep=";", dtype=str)
    df.columns = df.columns.str.strip()
    
    for col in df.columns: 
        df[col] = df[col].astype(str).str.strip()
    
    df["Ano_Inicio_Int"] = df["Ano_Inicio"].apply(converter_ano)
    df["Ano_Fim_Int"]    = df["Ano_Fim"].apply(converter_ano)
    df["Ano_Inicio_Int"] = pd.to_numeric(df["Ano_Inicio_Int"], errors='coerce').fillna(1990)
    df["Ano_Fim_Int"] = pd.to_numeric(df["Ano_Fim_Int"], errors='coerce').fillna(datetime.now().year)

    return df, None

def carregar_conversoes():
    arquivo_csv = "conversao.csv"
    caminhos = [
        os.path.join(os.path.dirname(__file__), arquivo_csv),
        os.path.join(os.path.dirname(__file__), "data", arquivo_csv),
        arquivo_csv,
    ]
    
    dict_conv = {}
    for c in caminhos:
        if os.path.exists(c):
            try:
                df_conv = pd.read_csv(c, sep=";", dtype=str)
                for _, row in df_conv.iterrows():
                    wega = str(row.get("Codigo_Wega", "")).replace('\xa0', '').strip().upper()
                    tecfil = str(row.get("Codigo_Tecfil", "")).replace('\xa0', '').strip().upper()
                    if wega and tecfil and tecfil not in ["NAN", "N/A", "NONE"]:
                        dict_conv[wega] = tecfil
                return dict_conv
            except:
                pass
    return dict_conv

def gerar_anos(row):
    try:
        ini = int(float(row.get("Ano_Inicio_Int", 1990)))
    except:
        ini = 1990
    try:
        fim = int(float(row.get("Ano_Fim_Int", datetime.now().year)))
    except:
        fim = datetime.now().year
        
    return list(range(ini, fim + 1))

# ─── NAVEGAÇÃO E ESTADO ────────────────────────────────────────────────────────
if "pagina" not in st.session_state: st.session_state.pagina = "home"
if "step" not in st.session_state: st.session_state.step = 1

def reset():
    for k in ["step","montadora","modelo","ano","classificacao", "transmissao"]:
        st.session_state.pop(k, None)
    st.session_state.step = 1

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
        if st.button("Consultar Filtros", use_container_width=True, key="btn_rev"):
            ir_para("filtros")
            st.rerun()

    with col2:
        st.markdown("""
        <div class="menu-card">
            <span class="menu-icon">🌧️</span>
            <div class="menu-title">Palhetas</div>
            <div class="menu-desc">Limpadores Dianteiros, Traseiros e Encaixes</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Consultar Palhetas", use_container_width=True, key="btn_palh"):
            ir_para("palhetas")
            st.rerun()

    with col3:
        st.markdown("""
        <div class="menu-card" style="opacity: 0.8;">
            <span class="menu-icon">⚙️</span>
            <div class="menu-title">Câmbio</div>
            <div class="menu-desc">Fluidos e Filtros de Transmissão (WFC/WFCK)</div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Consultar Câmbio", use_container_width=True, key="btn_cam"):
            ir_para("cambio")
            st.rerun()

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
    if st.button("⬅️ Voltar ao Menu Inicial", key="voltar_cons"):
        ir_para("home")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(f"<h2 style='color: var(--text-title); font-weight: 900; margin-top: -1rem; margin-bottom: 1.5rem; letter-spacing: -0.02em;'>{titulo_pagina}</h2>", unsafe_allow_html=True)

    df, erro = carregar_dados(arquivo)
    if erro: st.error(f"❌ {erro}"); st.stop()

    if is_cambio:
        etapas = ["Montadora", "Modelo", "Ano", "Versão", "Transmissão", label_resultado]
    else:
        etapas = ["Montadora", "Modelo", "Ano", "Versão", label_resultado]

    def step_class(i):
        s = st.session_state.step
        if i + 1 < s:  return "done"
        if i + 1 == s: return "active"
        return "todo"

    html_steps = '<div class="steps-bar">'
    for i, label in enumerate(etapas):
        cls = step_class(i)
        num_icon = "✓" if (cls == "done" or (st.session_state.step == passo_final and i == passo_final - 1)) else str(i + 1)
        html_steps += f'<div class="step-item"><div class="step-num {cls}">{num_icon}</div><span class="step-label {cls}">{label}</span></div>'
        if i < len(etapas) - 1: html_steps += '<span class="step-arrow">›</span>'
    html_steps += "</div>"
    st.markdown(html_steps, unsafe_allow_html=True)

    col_sel, col_res = st.columns([1, 1.4], gap="large")

    with col_sel:
        st.markdown('<div class="select-title">① Montadora</div>', unsafe_allow_html=True)
        montadoras = sorted(df["Nome_Montadora"].dropna().unique().tolist())
        montadora_sel = st.selectbox("Montadora", ["— Selecione —"] + montadoras, label_visibility="collapsed", key="sel_montadora")
        
        if montadora_sel != "— Selecione —":
            st.session_state.montadora = montadora_sel
            if st.session_state.step < 2: st.session_state.step = 2
        else: reset()

        st.markdown('<hr class="orange-divider">', unsafe_allow_html=True)

        st.markdown('<div class="select-title">② Modelo</div>', unsafe_allow_html=True)
        if st.session_state.step >= 2:
            df_m = df[df["Nome_Montadora"] == st.session_state.montadora]
            modelos = sorted(df_m["Nome_Modelo"].dropna().unique().tolist())
            modelo_sel = st.selectbox("Modelo", ["— Selecione —"] + modelos, label_visibility="collapsed", key="sel_modelo")
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

            ano_sel = st.selectbox("Ano", ["— Selecione —"] + [str(a) for a in anos_disp], label_visibility="collapsed", key="sel_ano")
            if ano_sel != "— Selecione —":
                st.session_state.ano = int(ano_sel)
                if st.session_state.step < 4: st.session_state.step = 4
            elif st.session_state.step > 3:
                st.session_state.step = 3
                for k in ["ano","classificacao", "transmissao"]: st.session_state.pop(k, None)
        else:
            st.selectbox("Ano", ["— Selecione primeiro o modelo —"], disabled=True, label_visibility="collapsed")

        st.markdown('<hr class="orange-divider">', unsafe_allow_html=True)

        st.markdown('<div class="select-title">④ Versão / Especificação</div>', unsafe_allow_html=True)
        if st.session_state.step >= 4:
            ano_int = st.session_state.ano
            df_ano = df_mod[(df_mod["Ano_Inicio_Int"] <= ano_int) & (df_mod["Ano_Fim_Int"] >= ano_int)]
            versoes = sorted(df_ano["Classificacao_Modelo"].replace("nan","").fillna("Versão Única / Padrão").unique().tolist())

            versao_sel = st.selectbox("Versão", ["— Selecione —"] + versoes, label_visibility="collapsed", key="sel_versao")
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
                transmissoes = sorted(df_trans["Codigo_Cambio"].dropna().unique().tolist())
                
                # Se só houver 1 transmissão disponível, seleciona-a automaticamente
                if len(transmissoes) == 1:
                    st.session_state.transmissao = transmissoes[0]
                    st.session_state.step = 6
                    st.selectbox("Transmissão", transmissoes, disabled=True, label_visibility="collapsed", key="sel_trans_auto")
                else:
                    trans_sel = st.selectbox("Transmissão", ["— Qual a transmissão do veículo? —"] + transmissoes, label_visibility="collapsed", key="sel_transmissao")
                    if trans_sel != "— Qual a transmissão do veículo? —":
                        st.session_state.transmissao = trans_sel
                        st.session_state.step = 6
                    elif st.session_state.step > 5:
                        st.session_state.step = 5
                        st.session_state.pop("transmissao", None)
            else:
                st.selectbox("Transmissão", ["— Selecione primeiro a versão —"], disabled=True, label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("↺  Limpar Filtros", use_container_width=True): reset(); st.rerun()

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
            ano_int = st.session_state.ano
            filtro_class = df["Classificacao_Modelo"].replace("nan","").fillna("") == st.session_state.classificacao
            if st.session_state.classificacao == "":
                filtro_class = df["Classificacao_Modelo"].isna() | (df["Classificacao_Modelo"] == "") | (df["Classificacao_Modelo"] == "nan")

            if is_cambio:
                filtro_trans = df["Codigo_Cambio"] == st.session_state.transmissao
                df_res = df[
                    (df["Nome_Montadora"] == st.session_state.montadora) &
                    (df["Nome_Modelo"] == st.session_state.modelo) &
                    filtro_class &
                    filtro_trans &
                    (df["Ano_Inicio_Int"] <= ano_int) &
                    (df["Ano_Fim_Int"] >= ano_int)
                ]
            else:
                df_res = df[
                    (df["Nome_Montadora"] == st.session_state.montadora) &
                    (df["Nome_Modelo"] == st.session_state.modelo) &
                    filtro_class &
                    (df["Ano_Inicio_Int"] <= ano_int) &
                    (df["Ano_Fim_Int"] >= ano_int)
                ]

            st.markdown(f"""
            <div class="summary-bar">
                <div class="summary-item">
                    <span class="summary-key">Montadora</span>
                    <span class="summary-val">{st.session_state.montadora}</span>
                </div>
                <div class="summary-item">
                    <span class="summary-key">Veículo</span>
                    <span class="summary-val">{st.session_state.modelo} ({st.session_state.ano})</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            if df_res.empty:
                st.markdown('<div class="no-result">⚠️ Nenhuma peça encontrada para esta combinação.</div>', unsafe_allow_html=True)
            else:
                row = df_res.iloc[0]

                def card(icone, tipo, codigo):
                    codigo_limpo = str(codigo).replace('\xa0', '').strip().upper()
                    if pd.isna(codigo) or codigo_limpo in ["", "NAN", "NONE"]:
                        return f'<div class="filter-card empty"><span class="filter-icon" style="opacity:.3">{icone}</span><div class="filter-type">{tipo}</div><div class="filter-code empty">ñ disp.</div></div>'
                    
                    if st.session_state.pagina == "filtros":
                        conv = dict_conversoes.get(codigo_limpo, "")
                        html_tec = f'<div class="filter-tecfil">⇄ TECFIL: {conv}</div>' if conv else ''
                        return f'<div class="filter-card"><span class="filter-icon">{icone}</span><div class="filter-type">{tipo}</div><div class="filter-code">{str(codigo).strip()}</div>{html_tec}</div>'
                    
                    if len(str(codigo)) > 20: fonte = "1.0rem"
                    elif len(str(codigo)) > 12: fonte = "1.2rem"
                    else: fonte = "1.6rem"
                    
                    return f'<div class="filter-card"><span class="filter-icon">{icone}</span><div class="filter-type">{tipo}</div><div class="filter-code" style="font-size:{fonte};">{str(codigo).strip()}</div></div>'

                html_cards = """
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
                    
                    body { 
                        margin: 0; 
                        background: transparent; 
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
                    .filter-code { font-weight: 900; color: #1a1d27; letter-spacing: -0.02em; line-height: 1.3; transform: translateZ(0); }
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
                    
                html_cards += "</div>"
                
               # 📏 ALTURA DINÂMICA: Ajuste milimétrico para cada módulo
                if st.session_state.pagina == "filtros":
                    altura_iframe = 340  # 2 linhas de cartões + conversão Tecfil
                elif st.session_state.pagina == "palhetas":
                    altura_iframe = 290  # 2 linhas de cartões limpos
                else:
                    altura_iframe = 160  # 1 linha de cartões (Câmbio)
                    
                components.html(html_cards, height=altura_iframe)

                versao_texto = st.session_state.classificacao if st.session_state.classificacao else "Versão Padrão"
                if is_cambio:
                    versao_texto += f" | Câmbio: {st.session_state.transmissao}"
                
                st.markdown(f"""
                <div style="margin-top:0.5rem;padding:0.8rem 1.2rem;background:var(--bg-card);
                            border-radius:8px;border:1px solid var(--border-line);font-size:0.82rem;color:var(--text-sub);">
                    <span style="color:#2ecc71;font-weight:800;text-transform:uppercase;
                                 font-size:0.7rem;letter-spacing:0.05em;">Observações / Configuração:</span><br>
                    <span style="color:var(--text-title); font-weight: 500;">{versao_texto}</span>
                </div>
                """, unsafe_allow_html=True)