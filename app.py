import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime
import os

# ─── CONFIG ───────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Consulta de Filtros Atend-Car",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── ESTILOS ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@400;600;700;800&family=Barlow:wght@400;500;600&display=swap');

/* Reset e base */
html, body, [class*="css"] {
    font-family: 'Barlow', sans-serif;
}

/* Fundo escuro industrial */
.stApp {
    background-color: #0f1117;
}

/* Header customizado */
.main-header {
    background: linear-gradient(135deg, #1a1d27 0%, #0f1117 100%);
    border-bottom: 3px solid #2ecc71;
    padding: 1.5rem 2rem;
    margin: -1rem -1rem 2rem -1rem;
    display: flex;
    align-items: center;
    gap: 1rem;
}

.main-header h1 {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 2.2rem;
    font-weight: 800;
    color: #ffffff;
    margin: 0;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.main-header .subtitle {
    font-size: 0.85rem;
    color: #8b8fa8;
    margin: 0;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

.logo-icon {
    font-size: 2.5rem;
    line-height: 1;
}

/* Steps indicador */
.steps-bar {
    display: flex;
    align-items: center;
    margin-bottom: 2rem;
    background: #1a1d27;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    border: 1px solid #2a2d3a;
}

.step-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    flex: 1;
}

.step-num {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 0.8rem;
    font-family: 'Barlow Condensed', sans-serif;
    flex-shrink: 0;
}

.step-num.done   { background: #2ecc71; color: #0f1117; }
.step-num.active { background: #ffffff; color: #0f1117; }
.step-num.todo   { background: #2a2d3a; color: #555870; }

.step-label {
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

.step-label.done   { color: #2ecc71; }
.step-label.active { color: #ffffff; }
.step-label.todo   { color: #555870; }

.step-arrow {
    color: #2a2d3a;
    font-size: 1rem;
    margin: 0 0.5rem;
}

/* Cards de seleção */
.select-title {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #2ecc71;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-bottom: 0.3rem;
}

.select-hint {
    font-size: 0.82rem;
    color: #6b7080;
    margin-bottom: 1.2rem;
}

/* Selectbox estilizado */
.stSelectbox > div > div {
    background-color: #1a1d27 !important;
    border: 2px solid #2a2d3a !important;
    border-radius: 8px !important;
    color: #ffffff !important;
    font-family: 'Barlow', sans-serif !important;
    font-size: 1rem !important;
}

.stSelectbox > div > div:focus-within {
    border-color: #2ecc71 !important;
    box-shadow: 0 0 0 1px #2ecc71 !important;
}

/* Divider laranja */
.orange-divider {
    height: 3px;
    background: linear-gradient(90deg, #2ecc71, transparent);
    border: none;
    margin: 1.5rem 0;
    border-radius: 2px;
}

/* Cards de resultado */
.result-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin-top: 1rem;
}

.filter-card {
    background: #1a1d27;
    border: 1px solid #2a2d3a;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}

.filter-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 4px;
    height: 100%;
    background: #2ecc71;
    border-radius: 0 0 0 12px;
}

.filter-card.empty::before {
    background: #2a2d3a;
}

.filter-type {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    color: #8b8fa8;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-bottom: 0.4rem;
}

.filter-icon {
    font-size: 1.4rem;
    margin-bottom: 0.4rem;
    display: block;
}

.filter-code {
    font-family: 'Barlow Condensed', sans-serif;
    font-size: 1.8rem;
    font-weight: 800;
    color: #ffffff;
    letter-spacing: 0.05em;
    line-height: 1;
}

.filter-code.empty {
    color: #3a3d4a;
    font-size: 1.1rem;
    font-weight: 400;
    font-family: 'Barlow', sans-serif;
    font-style: italic;
}

/* Botão resetar */
.stButton > button {
    background: transparent !important;
    border: 2px solid #2ecc71 !important;
    color: #2ecc71 !important;
    font-family: 'Barlow Condensed', sans-serif !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.1em !important;
    padding: 0.6rem 2rem !important;
    border-radius: 8px !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    background: #2ecc71 !important;
    color: #0f1117 !important;
}

/* Sumário da seleção */
.summary-bar {
    background: #1a1d27;
    border: 1px solid #2a2d3a;
    border-radius: 10px;
    padding: 1rem 1.4rem;
    margin-bottom: 1.5rem;
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
}

.summary-item {
    display: flex;
    flex-direction: column;
    gap: 0.15rem;
}

.summary-key {
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #2ecc71;
}

.summary-val {
    font-size: 0.95rem;
    font-weight: 600;
    color: #ffffff;
}

/* Mensagem de resultado vazio */
.no-result {
    background: #1a1d27;
    border: 1px dashed #3a3d4a;
    border-radius: 10px;
    padding: 2rem;
    text-align: center;
    color: #555870;
    font-style: italic;
}

/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0f1117; }
::-webkit-scrollbar-thumb { background: #2a2d3a; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #2ecc71; }
</style>
""", unsafe_allow_html=True)


# ─── FUNÇÕES UTILITÁRIAS ───────────────────────────────────────────────────────

def converter_ano(val):
    """Converte ano de 2 ou 4 dígitos para inteiro de 4 dígitos."""
    if pd.isna(val):
        return None
    try:
        n = int(str(val).strip())
        if n > 9999:   # segurança
            return None
        if n > 50:
            return 1900 + n if n < 100 else n
        else:
            return 2000 + n if n < 100 else n
    except (ValueError, TypeError):
        return None


@st.cache_data
def carregar_dados():
    """Carrega e pré-processa o CSV automaticamente."""
    # Procura o CSV na mesma pasta do script ou em caminhos comuns
    caminhos = [
        os.path.join(os.path.dirname(__file__), "catalogo.csv"),
        os.path.join(os.path.dirname(__file__), "data", "catalogo.csv"),
        "catalogo.csv",
    ]
    csv_path = None
    for c in caminhos:
        if os.path.exists(c):
            csv_path = c
            break

    if csv_path is None:
        return None, "Arquivo catalogo.csv não encontrado na pasta do sistema."

    df = pd.read_csv(csv_path, sep=";", dtype=str)
    df.columns = df.columns.str.strip()

    # Limpa espaços em todas as strings
    for col in df.columns:
        df[col] = df[col].str.strip()

    # Converte anos
    df["Ano_Inicio_Int"] = df["Ano_Inicio"].apply(converter_ano)
    df["Ano_Fim_Int"]    = df["Ano_Fim"].apply(converter_ano)

    # Ano_Fim vazio = vigente até hoje
    ano_atual = datetime.now().year
    df["Ano_Fim_Int"] = df["Ano_Fim_Int"].fillna(ano_atual)

    return df, None


def gerar_anos(row):
    """Retorna lista de anos de vigência de uma linha."""
    ini = row["Ano_Inicio_Int"]
    fim = row["Ano_Fim_Int"]
    if ini is None:
        return []
    return list(range(int(ini), int(fim) + 1))


# ─── CARREGA DADOS ─────────────────────────────────────────────────────────────
df, erro = carregar_dados()

# ─── HEADER ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <span class="logo-icon">🔧</span>
    <div>
        <h1>Consulta de Filtros Automotivos Atend-Car</h1>
        <p class="subtitle">Consulta rápida por montadora · modelo · ano</p>
    </div>
</div>
""", unsafe_allow_html=True)

if erro:
    st.error(f"❌ {erro}")
    st.info("Coloque o arquivo **catalogo.csv** na mesma pasta que este script e reinicie.")
    st.stop()

# ─── ESTADO DA SESSÃO ──────────────────────────────────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = 1

def reset():
    for k in ["step","montadora","modelo","ano","classificacao"]:
        if k in st.session_state:
            del st.session_state[k]
    st.session_state.step = 1

# ─── BARRA DE ETAPAS ──────────────────────────────────────────────────────────
etapas = ["Montadora", "Modelo", "Ano", "Versão", "Filtros"]

def step_class(i):
    s = st.session_state.step
    if i + 1 < s:  return "done"
    if i + 1 == s: return "active"
    return "todo"

html_steps = '<div class="steps-bar">'
for i, label in enumerate(etapas):
    cls = step_class(i)
    num_icon = "✓" if cls == "done" else str(i + 1)
    html_steps += f"""
        <div class="step-item">
            <div class="step-num {cls}">{num_icon}</div>
            <span class="step-label {cls}">{label}</span>
        </div>
    """
    if i < len(etapas) - 1:
        html_steps += '<span class="step-arrow">›</span>'
html_steps += "</div>"
st.markdown(html_steps, unsafe_allow_html=True)

# ─── LAYOUT PRINCIPAL ──────────────────────────────────────────────────────────
col_sel, col_res = st.columns([1, 1.4], gap="large")

with col_sel:
    # ── ETAPA 1: MONTADORA ────────────────────────────────────────────────────
    st.markdown('<div class="select-title">① Montadora</div>', unsafe_allow_html=True)
    st.markdown('<div class="select-hint">Selecione a fabricante do veículo</div>', unsafe_allow_html=True)

    montadoras = sorted(df["Nome_Montadora"].dropna().unique().tolist())
    montadora_sel = st.selectbox(
        "Montadora",
        ["— Selecione —"] + montadoras,
        label_visibility="collapsed",
        key="sel_montadora",
    )

    if montadora_sel != "— Selecione —":
        st.session_state.montadora = montadora_sel
        if st.session_state.step < 2:
            st.session_state.step = 2
    else:
        reset()

    st.markdown('<hr class="orange-divider">', unsafe_allow_html=True)

    # ── ETAPA 2: MODELO ───────────────────────────────────────────────────────
    st.markdown('<div class="select-title">② Modelo</div>', unsafe_allow_html=True)
    st.markdown('<div class="select-hint">Selecione o modelo principal</div>', unsafe_allow_html=True)

    if st.session_state.step >= 2:
        df_m = df[df["Nome_Montadora"] == st.session_state.montadora]
        modelos = sorted(df_m["Nome_Modelo"].dropna().unique().tolist())
        modelo_sel = st.selectbox(
            "Modelo",
            ["— Selecione —"] + modelos,
            label_visibility="collapsed",
            key="sel_modelo",
        )
        if modelo_sel != "— Selecione —":
            st.session_state.modelo = modelo_sel
            if st.session_state.step < 3:
                st.session_state.step = 3
        elif st.session_state.step > 2:
            st.session_state.step = 2
            for k in ["modelo","ano","classificacao"]:
                st.session_state.pop(k, None)
    else:
        st.selectbox("Modelo", ["— Selecione primeiro a montadora —"],
                     disabled=True, label_visibility="collapsed")

    st.markdown('<hr class="orange-divider">', unsafe_allow_html=True)

    # ── ETAPA 3: ANO ─────────────────────────────────────────────────────────
    st.markdown('<div class="select-title">③ Ano</div>', unsafe_allow_html=True)
    st.markdown('<div class="select-hint">Ano de fabricação do veículo</div>', unsafe_allow_html=True)

    if st.session_state.step >= 3:
        df_mod = df_m[df_m["Nome_Modelo"] == st.session_state.modelo]

        # Expande todos os anos disponíveis para este modelo
        anos_set = set()
        for _, row in df_mod.iterrows():
            anos_set.update(gerar_anos(row))
        anos_disp = sorted(anos_set, reverse=True)

        ano_sel = st.selectbox(
            "Ano",
            ["— Selecione —"] + [str(a) for a in anos_disp],
            label_visibility="collapsed",
            key="sel_ano",
        )
        if ano_sel != "— Selecione —":
            st.session_state.ano = int(ano_sel)
            if st.session_state.step < 4:
                st.session_state.step = 4
        elif st.session_state.step > 3:
            st.session_state.step = 3
            for k in ["ano","classificacao"]:
                st.session_state.pop(k, None)
    else:
        st.selectbox("Ano", ["— Selecione primeiro o modelo —"],
                     disabled=True, label_visibility="collapsed")

    st.markdown('<hr class="orange-divider">', unsafe_allow_html=True)

    # ── ETAPA 4: CLASSIFICAÇÃO / VERSÃO ───────────────────────────────────────
    st.markdown('<div class="select-title">④ Versão / Motor</div>', unsafe_allow_html=True)
    st.markdown('<div class="select-hint">Selecione a versão específica</div>', unsafe_allow_html=True)

    if st.session_state.step >= 4:
        ano_int = st.session_state.ano
        df_ano = df_mod[
            (df_mod["Ano_Inicio_Int"].astype(float) <= ano_int) &
            (df_mod["Ano_Fim_Int"].astype(float)    >= ano_int)
        ]
        versoes = sorted(df_ano["Classificacao_Modelo"].dropna().unique().tolist())

        versao_sel = st.selectbox(
            "Versão",
            ["— Selecione —"] + versoes,
            label_visibility="collapsed",
            key="sel_versao",
        )
        if versao_sel != "— Selecione —":
            st.session_state.classificacao = versao_sel
            st.session_state.step = 5
        elif st.session_state.step > 4:
            st.session_state.step = 4
            st.session_state.pop("classificacao", None)
    else:
        st.selectbox("Versão", ["— Selecione primeiro o ano —"],
                     disabled=True, label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("↺  Nova Consulta", use_container_width=True):
        reset()
        st.rerun()

# ─── PAINEL DE RESULTADOS ──────────────────────────────────────────────────────
with col_res:
    st.markdown('<div class="select-title">⑤ Filtros Indicados</div>', unsafe_allow_html=True)

    if st.session_state.step < 5:
        passos_falt = {1:"montadora",2:"modelo",3:"ano",4:"versão"}
        prox = passos_falt.get(st.session_state.step, "versão")
        st.markdown(f"""
        <div class="no-result">
            <span style="font-size:2rem">🔍</span><br><br>
            Complete a seleção à esquerda.<br>
            <strong style="color:#2ecc71">Próximo passo:</strong> escolha a {prox}.
        </div>
        """, unsafe_allow_html=True)
    else:
        # Filtra a linha correta
        ano_int = st.session_state.ano
        df_res = df[
            (df["Nome_Montadora"]      == st.session_state.montadora) &
            (df["Nome_Modelo"]         == st.session_state.modelo) &
            (df["Classificacao_Modelo"]== st.session_state.classificacao) &
            (df["Ano_Inicio_Int"].astype(float) <= ano_int) &
            (df["Ano_Fim_Int"].astype(float)    >= ano_int)
        ]

        # ── Sumário da seleção ─────────────────────────────────────────────
        ano_ini = int(df_res["Ano_Inicio_Int"].iloc[0]) if not df_res.empty else "—"
        ano_fim_raw = df_res["Ano_Fim_Int"].iloc[0] if not df_res.empty else None
        ano_fim_str = str(int(ano_fim_raw)) if ano_fim_raw and int(ano_fim_raw) != datetime.now().year else "atual"

        st.markdown(f"""
        <div class="summary-bar">
            <div class="summary-item">
                <span class="summary-key">Montadora</span>
                <span class="summary-val">{st.session_state.montadora}</span>
            </div>
            <div class="summary-item">
                <span class="summary-key">Modelo</span>
                <span class="summary-val">{st.session_state.modelo}</span>
            </div>
            <div class="summary-item">
                <span class="summary-key">Ano</span>
                <span class="summary-val">{st.session_state.ano}</span>
            </div>
            <div class="summary-item">
                <span class="summary-key">Vigência</span>
                <span class="summary-val">{ano_ini} – {ano_fim_str}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if df_res.empty:
            st.markdown("""
            <div class="no-result">
                ⚠️ Nenhum filtro encontrado para esta combinação.
            </div>
            """, unsafe_allow_html=True)
        else:
            row = df_res.iloc[0]

            def card(icone, tipo, codigo):
                if pd.isna(codigo) or str(codigo).strip() in ["", "nan"]:
                    return f"""
                    <div class="filter-card empty">
                        <span class="filter-icon" style="opacity:.3">{icone}</span>
                        <div class="filter-type">{tipo}</div>
                        <div class="filter-code empty">não disponível</div>
                    </div>"""
                return f"""
                <div class="filter-card">
                    <span class="filter-icon">{icone}</span>
                    <div class="filter-type">{tipo}</div>
                    <div class="filter-code">{str(codigo).strip()}</div>
                </div>"""

            html_cards = f"""
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@700;800&family=Barlow:wght@400;600&display=swap');
                body {{ margin: 0; background: transparent; }}
                .result-grid {{
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 1rem;
                }}
                .filter-card {{
                    background: #1a1d27;
                    border: 1px solid #2a2d3a;
                    border-radius: 12px;
                    padding: 1.2rem 1.4rem;
                    position: relative;
                    overflow: hidden;
                }}
                .filter-card::before {{
                    content: '';
                    position: absolute;
                    top: 0; left: 0;
                    width: 4px; height: 100%;
                    background: #2ecc71;
                }}
                .filter-card.empty::before {{ background: #2a2d3a; }}
                .filter-icon {{ font-size: 1.4rem; display: block; margin-bottom: 0.4rem; }}
                .filter-type {{
                    font-family: 'Barlow Condensed', sans-serif;
                    font-size: 0.75rem; font-weight: 700;
                    color: #8b8fa8; text-transform: uppercase;
                    letter-spacing: 0.15em; margin-bottom: 0.4rem;
                }}
                .filter-code {{
                    font-family: 'Barlow Condensed', sans-serif;
                    font-size: 1.8rem; font-weight: 800;
                    color: #ffffff; letter-spacing: 0.05em; line-height: 1;
                }}
                .filter-code.empty {{
                    color: #3a3d4a; font-size: 1rem;
                    font-weight: 400; font-style: italic;
                    font-family: 'Barlow', sans-serif;
                }}
            </style>
            <div class="result-grid">
                {card("💨", "Filtro de Ar",           row.get("Filtro_Ar"))}
                {card("🛢️",  "Filtro de Óleo",        row.get("Filtro_Oleo"))}
                {card("⛽", "Filtro de Combustível",   row.get("Filtro_Combustivel"))}
                {card("🌬️", "Filtro de Cabine",       row.get("Filtro_Cabine"))}
            </div>
            """
            components.html(html_cards, height=280)

            if len(df_res) > 1:
                st.markdown("""
                <br>
                <div style="background:#1a1d27;border:1px solid #103c22;border-radius:8px;
                            padding:0.8rem 1.2rem;color:#4ADE80;font-size:0.85rem;">
                    ⚠️ <strong>Atenção:</strong> foram encontradas múltiplas entradas para esta seleção.
                    Exibindo a primeira correspondência. Verifique o catálogo se necessário.
                </div>
                """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="margin-top:1rem;padding:0.8rem 1.2rem;background:#1a1d27;
                    border-radius:8px;border:1px solid #2a2d3a;font-size:0.82rem;color:#6b7080;">
            <span style="color:#2ecc71;font-weight:700;text-transform:uppercase;
                         font-size:0.7rem;letter-spacing:0.1em;">Versão completa</span><br>
            {st.session_state.get('classificacao','—')}
        </div>
        """, unsafe_allow_html=True)