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
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@400;500;600&display=swap');

/* Oculta o menu padrão do Streamlit para visual de App Nativo */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* Reset e base */
html, body, [class*="css"] { font-family: 'Barlow', sans-serif; }

/* --- TEMA DINÂMICO (CLARO/ESCURO) --- */
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

/* Header customizado */
.main-header {
    background: var(--bg-card);
    border-bottom: 3px solid #2ecc71;
    padding: 1.5rem 2rem;
    margin: -1rem -1rem 2rem -1rem;
    display: flex; align-items: center; gap: 1rem;
}
.main-header h1 {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2.2rem; font-weight: 800; color: var(--text-title);
    margin: 0; letter-spacing: 0.05em; text-transform: uppercase;
}
.main-header .subtitle {
    font-size: 0.85rem; color: var(--text-sub); margin: 0;
    letter-spacing: 0.1em; text-transform: uppercase;
}
.logo-icon { font-size: 2.5rem; line-height: 1; }

/* Cards Menu Inicial */
.menu-card {
    background: var(--bg-card); border: 2px solid var(--border-line);
    border-radius: 12px; padding: 2rem 1.5rem; text-align: center;
    transition: all 0.3s ease; height: 100%;
}
.menu-card:hover { border-color: #2ecc71; transform: translateY(-5px); }
.menu-icon { font-size: 3rem; margin-bottom: 1rem; display: block; }
.menu-title { font-family: 'Barlow Condensed', sans-serif; font-size: 1.5rem; font-weight: 700; color: var(--text-title); margin-bottom: 0.5rem; text-transform: uppercase;}
.menu-desc { color: var(--text-sub); font-size: 0.9rem; margin-bottom: 1.5rem; }

/* Steps indicador */
.steps-bar {
    display: flex; align-items: center; margin-bottom: 2rem;
    background: var(--bg-card); border-radius: 12px;
    padding: 1rem 1.5rem; border: 1px solid var(--border-line);
}
.step-item { display: flex; align-items: center; gap: 0.5rem; flex: 1; }
.step-num { width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: 700; font-size: 0.8rem; font-family: 'Barlow Condensed', sans-serif; flex-shrink: 0; }
.step-num.done, .step-num.active { background: #2ecc71; color: #ffffff; }
.step-num.todo { background: var(--step-todo-bg); color: var(--step-todo-text); }
.step-label { font-size: 0.78rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.08em; }
.step-label.done { color: #2ecc71; }
.step-label.active { color: var(--text-title); }
.step-label.todo { color: var(--step-todo-text); }
.step-arrow { color: var(--border-line); font-size: 1rem; margin: 0 0.5rem; }

/* Componentes Genéricos */
.select-title { font-family: 'Barlow Condensed', sans-serif; font-size: 1.3rem; font-weight: 700; color: #2ecc71; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.3rem; }
.select-hint { font-size: 0.82rem; color: var(--text-sub); margin-bottom: 1.2rem; }
.stSelectbox > div > div { background-color: var(--bg-card) !important; border: 2px solid var(--border-line) !important; border-radius: 8px !important; color: var(--text-title) !important; font-family: 'Barlow', sans-serif !important; font-size: 1rem !important; }
.stSelectbox > div > div:focus-within { border-color: #2ecc71 !important; box-shadow: 0 0 0 1px #2ecc71 !important; }
.orange-divider { height: 3px; background: linear-gradient(90deg, #2ecc71, transparent); border: none; margin: 1.5rem 0; border-radius: 2px; }

/* Botões */
.stButton > button { font-family: 'Barlow Condensed', sans-serif !important; font-weight: 700 !important; font-size: 1rem !important; text-transform: uppercase !important; letter-spacing: 0.1em !important; padding: 0.6rem 2rem !important; border-radius: 8px !important; transition: all 0.2s !important; }
.btn-voltar > button { background: var(--bg-card) !important; border: 2px solid var(--border-line) !important; color: var(--text-title) !important; width: auto !important; margin-bottom: 1rem !important;}
.btn-voltar > button:hover { border-color: #2ecc71 !important; color: #2ecc71 !important; }

/* Sumário e Mensagens */
.summary-bar { background: var(--bg-card); border: 1px solid var(--border-line); border-radius: 10px; padding: 1rem 1.4rem; margin-bottom: 1.5rem; display: flex; gap: 2rem; flex-wrap: wrap; }
.summary-item { display: flex; flex-direction: column; gap: 0.15rem; }
.summary-key { font-size: 0.7rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.12em; color: #2ecc71; }
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
    if pd.isna(val): return None
    try:
        n = int(str(val).strip())
        if n > 9999: return None
        if n > 50: return 1900 + n if n < 100 else n
        else: return 2000 + n if n < 100 else n
    except (ValueError, TypeError): return None

@st.cache_data
def carregar_dados(arquivo_csv):
    caminhos = [
        os.path.join(os.path.dirname(__file__), arquivo_csv),
        os.path.join(os.path.dirname(__file__), "data", arquivo_csv),
        arquivo_csv,
    ]
    csv_path = None
    for c in caminhos:
        if os.path.exists(c):
            csv_path = c
            break

    if csv_path is None: return None, f"Arquivo {arquivo_csv} não encontrado."

    df = pd.read_csv(csv_path, sep=";", dtype=str)
    df.columns = df.columns.str.strip()
    for col in df.columns: df[col] = df[col].str.strip()
    
    df["Ano_Inicio_Int"] = df["Ano_Inicio"].apply(converter_ano)
    df["Ano_Fim_Int"]    = df["Ano_Fim"].apply(converter_ano)
    df["Ano_Fim_Int"] = df["Ano_Fim_Int"].fillna(datetime.now().year)

    return df, None

def gerar_anos(row):
    ini, fim = row["Ano_Inicio_Int"], row["Ano_Fim_Int"]
    if ini is None: return []
    return list(range(int(ini), int(fim) + 1))

# ─── NAVEGAÇÃO E ESTADO ────────────────────────────────────────────────────────
if "pagina" not in st.session_state: st.session_state.pagina = "home"
if "step" not in st.session_state: st.session_state.step = 1

def reset():
    for k in ["step","montadora","modelo","ano","classificacao"]:
        st.session_state.pop(k, None)
    st.session_state.step = 1

def ir_para(pagina):
    reset()
    st.session_state.pagina = pagina

# ─── HEADER FIXO ──────────────────────────────────────────────────────────────
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
    st.markdown("<h2 style='text-align: center; color: var(--text-title); margin-bottom: 2rem; font-family: \"Barlow Condensed\", sans-serif;'>O QUE VOCÊ DESEJA CONSULTAR HOJE?</h2>", unsafe_allow_html=True)
    
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
# TELA DE CÂMBIO (EM DESENVOLVIMENTO)
# ==============================================================================
elif st.session_state.pagina == "cambio":
    st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
    if st.button("⬅️ Voltar ao Menu", key="voltar_cam"):
        ir_para("home")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="no-result" style="padding: 4rem;">
        <span style="font-size: 3rem;">🚧</span><br><br>
        <h2 style="color: var(--text-title); font-family: 'Barlow Condensed';">Módulo em Desenvolvimento</h2>
        <p>Em breve você poderá consultar os filtros e aplicações para transmissões automáticas!</p>
    </div>
    """, unsafe_allow_html=True)


# ==============================================================================
# TELAS DE CONSULTA (FILTROS E PALHETAS COMPARTILHAM A LÓGICA)
# ==============================================================================
elif st.session_state.pagina in ["filtros", "palhetas"]:
    # Define arquivo baseado na escolha
    arquivo = "catalogo.csv" if st.session_state.pagina == "filtros" else "palhetas.csv"
    titulo_pagina = "🛢️ CONSULTA DE REVISÃO (FILTROS)" if st.session_state.pagina == "filtros" else "🌧️ CONSULTA DE PALHETAS"
    label_resultado = "Filtros" if st.session_state.pagina == "filtros" else "Palhetas"
    
    st.markdown('<div class="btn-voltar">', unsafe_allow_html=True)
    if st.button("⬅️ Voltar ao Menu Inicial", key="voltar_cons"):
        ir_para("home")
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown(f"<h2 style='color: var(--text-title); font-family: \"Barlow Condensed\"; margin-top: -1rem; margin-bottom: 1.5rem;'>{titulo_pagina}</h2>", unsafe_allow_html=True)

    df, erro = carregar_dados(arquivo)
    
    if erro:
        st.error(f"❌ {erro}")
        st.info(f"Coloque o arquivo **{arquivo}** na mesma pasta que este script.")
        st.stop()

    # ── BARRA DE ETAPAS ──
    etapas = ["Montadora", "Modelo", "Ano", "Versão", label_resultado]
    def step_class(i):
        s = st.session_state.step
        if i + 1 < s:  return "done"
        if i + 1 == s: return "active"
        return "todo"

    html_steps = '<div class="steps-bar">'
    for i, label in enumerate(etapas):
        cls = step_class(i)
        num_icon = "✓" if cls == "done" else str(i + 1)
        html_steps += f'<div class="step-item"><div class="step-num {cls}">{num_icon}</div><span class="step-label {cls}">{label}</span></div>'
        if i < len(etapas) - 1: html_steps += '<span class="step-arrow">›</span>'
    html_steps += "</div>"
    st.markdown(html_steps, unsafe_allow_html=True)

    col_sel, col_res = st.columns([1, 1.4], gap="large")

    with col_sel:
        # 1: MONTADORA
        st.markdown('<div class="select-title">① Montadora</div>', unsafe_allow_html=True)
        montadoras = sorted(df["Nome_Montadora"].dropna().unique().tolist())
        montadora_sel = st.selectbox("Montadora", ["— Selecione —"] + montadoras, label_visibility="collapsed", key="sel_montadora")
        
        if montadora_sel != "— Selecione —":
            st.session_state.montadora = montadora_sel
            if st.session_state.step < 2: st.session_state.step = 2
        else: reset()

        st.markdown('<hr class="orange-divider">', unsafe_allow_html=True)

        # 2: MODELO
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
                for k in ["modelo","ano","classificacao"]: st.session_state.pop(k, None)
        else:
            st.selectbox("Modelo", ["— Selecione primeiro a montadora —"], disabled=True, label_visibility="collapsed")

        st.markdown('<hr class="orange-divider">', unsafe_allow_html=True)

        # 3: ANO
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
                for k in ["ano","classificacao"]: st.session_state.pop(k, None)
        else:
            st.selectbox("Ano", ["— Selecione primeiro o modelo —"], disabled=True, label_visibility="collapsed")

        st.markdown('<hr class="orange-divider">', unsafe_allow_html=True)

        # 4: VERSÃO
        st.markdown('<div class="select-title">④ Versão / Especificação</div>', unsafe_allow_html=True)
        if st.session_state.step >= 4:
            ano_int = st.session_state.ano
            df_ano = df_mod[(df_mod["Ano_Inicio_Int"].astype(float) <= ano_int) & (df_mod["Ano_Fim_Int"].astype(float) >= ano_int)]
            versoes = sorted(df_ano["Classificacao_Modelo"].fillna("Versão Única / Padrão").unique().tolist())

            versao_sel = st.selectbox("Versão", ["— Selecione —"] + versoes, label_visibility="collapsed", key="sel_versao")
            if versao_sel != "— Selecione —":
                st.session_state.classificacao = versao_sel if versao_sel != "Versão Única / Padrão" else ""
                st.session_state.step = 5
            elif st.session_state.step > 4:
                st.session_state.step = 4
                st.session_state.pop("classificacao", None)
        else:
            st.selectbox("Versão", ["— Selecione primeiro o ano —"], disabled=True, label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("↺  Limpar Filtros", use_container_width=True):
            reset()
            st.rerun()

    # PAINEL DE RESULTADOS
    with col_res:
        st.markdown(f'<div class="select-title">⑤ Resultados: {label_resultado}</div>', unsafe_allow_html=True)

        if st.session_state.step < 5:
            prox = {1:"montadora",2:"modelo",3:"ano",4:"versão"}.get(st.session_state.step, "versão")
            st.markdown(f"""
            <div class="no-result">
                <span style="font-size:2rem">🔍</span><br><br>
                Complete a seleção à esquerda.<br>
                <strong style="color:#2ecc71">Próximo passo:</strong> escolha a {prox}.
            </div>
            """, unsafe_allow_html=True)
        else:
            ano_int = st.session_state.ano
            # Trata busca considerando que Classificacao pode ser vazio/NaN
            filtro_class = df["Classificacao_Modelo"].fillna("") == st.session_state.classificacao
            if st.session_state.classificacao == "":
                filtro_class = df["Classificacao_Modelo"].isna() | (df["Classificacao_Modelo"] == "")

            df_res = df[
                (df["Nome_Montadora"] == st.session_state.montadora) &
                (df["Nome_Modelo"] == st.session_state.modelo) &
                filtro_class &
                (df["Ano_Inicio_Int"].astype(float) <= ano_int) &
                (df["Ano_Fim_Int"].astype(float) >= ano_int)
            ]

            ano_ini = int(df_res["Ano_Inicio_Int"].iloc[0]) if not df_res.empty else "—"
            ano_fim_raw = df_res["Ano_Fim_Int"].iloc[0] if not df_res.empty else None
            ano_fim_str = str(int(ano_fim_raw)) if ano_fim_raw and int(ano_fim_raw) != datetime.now().year else "atual"

            st.markdown(f"""
            <div class="summary-bar">
                <div class="summary-item"><span class="summary-key">Montadora</span><span class="summary-val">{st.session_state.montadora}</span></div>
                <div class="summary-item"><span class="summary-key">Modelo</span><span class="summary-val">{st.session_state.modelo}</span></div>
                <div class="summary-item"><span class="summary-key">Ano</span><span class="summary-val">{st.session_state.ano}</span></div>
                <div class="summary-item"><span class="summary-key">Vigência</span><span class="summary-val">{ano_ini} – {ano_fim_str}</span></div>
            </div>
            """, unsafe_allow_html=True)

            if df_res.empty:
                st.markdown('<div class="no-result">⚠️ Nenhuma peça encontrada para esta combinação.</div>', unsafe_allow_html=True)
            else:
                row = df_res.iloc[0]

                def card(icone, tipo, codigo):
                    if pd.isna(codigo) or str(codigo).strip() in ["", "nan"]:
                        return f'<div class="filter-card empty"><span class="filter-icon" style="opacity:.3">{icone}</span><div class="filter-type">{tipo}</div><div class="filter-code empty">não usa / ñ disp.</div></div>'
                    return f'<div class="filter-card"><span class="filter-icon">{icone}</span><div class="filter-type">{tipo}</div><div class="filter-code">{str(codigo).strip()}</div></div>'

                html_cards = """
                <style>
                    @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=Barlow:wght@400;600&display=swap');
                    body { margin: 0; background: transparent; }
                    .result-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 1rem; }
                    .filter-card { background: #ffffff; border: 1px solid #dee2e6; border-radius: 12px; padding: 1.2rem 1.4rem; position: relative; overflow: hidden; }
                    .filter-card::before { content: ''; position: absolute; top: 0; left: 0; width: 4px; height: 100%; background: #2ecc71; }
                    .filter-card.empty::before { background: #dee2e6; }
                    .filter-icon { font-size: 1.4rem; display: block; margin-bottom: 0.4rem; }
                    .filter-type { font-family: 'Barlow Condensed', sans-serif; font-size: 0.75rem; font-weight: 700; color: #6b7080; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 0.4rem; }
                    .filter-code { font-family: 'Barlow Condensed', sans-serif; font-size: 1.8rem; font-weight: 800; color: #1a1d27; letter-spacing: 0.05em; line-height: 1; }
                    .filter-code.empty { color: #6b7080; font-size: 1rem; font-weight: 400; font-style: italic; font-family: 'Barlow', sans-serif; }
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
                
                # Gera as cartas baseadas na página em que estamos
                if st.session_state.pagina == "filtros":
                    html_cards += card("💨", "Filtro de Ar", row.get("Filtro_Ar"))
                    html_cards += card("🛢️", "Filtro de Óleo", row.get("Filtro_Oleo"))
                    html_cards += card("⛽", "Filtro Combustível", row.get("Filtro_Combustivel"))
                    html_cards += card("🌬️", "Filtro de Cabine", row.get("Filtro_Cabine"))
                else:
                    html_cards += card("🚘", "Motorista", row.get("Palheta_Motorista"))
                    html_cards += card("💺", "Passageiro", row.get("Palheta_Passageiro"))
                    html_cards += card("🔙", "Traseira", row.get("Palheta_Traseira"))
                    html_cards += card("🪝", "Tipo de Encaixe", row.get("Tipo_Gancho"))
                    
                html_cards += "</div>"
                components.html(html_cards, height=280)

                versao_texto = st.session_state.classificacao if st.session_state.classificacao else "Versão Padrão"
                st.markdown(f"""
                <div style="margin-top:0.5rem;padding:0.8rem 1.2rem;background:var(--bg-card);
                            border-radius:8px;border:1px solid var(--border-line);font-size:0.82rem;color:var(--text-sub);">
                    <span style="color:#2ecc71;font-weight:700;text-transform:uppercase;
                                 font-size:0.7rem;letter-spacing:0.1em;">Observações / Versão:</span><br>
                    <span style="color:var(--text-title);">{versao_texto}</span>
                </div>
                """, unsafe_allow_html=True)