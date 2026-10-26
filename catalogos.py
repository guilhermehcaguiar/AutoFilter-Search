"""Leitura e normalização dos catálogos, independente da interface."""

import csv
import io
import re
from datetime import datetime
from pathlib import Path

import pandas as pd


BASE = ["Nome_Montadora", "Nome_Modelo", "Classificacao_Modelo", "Ano_Inicio", "Ano_Fim"]
COLUNAS = {
    "catalogo.csv": BASE + ["Filtro_Ar", "Filtro_Oleo", "Filtro_Combustivel", "Filtro_Cabine"],
    "palhetas.csv": BASE + ["Palheta_Motorista", "Palheta_Passageiro", "Palheta_Traseira", "Tipo_Gancho"],
    "cambio.csv": ["Nome_Montadora", "Nome_Modelo", "Ano_Inicio", "Ano_Fim",
                   "Classificacao_Modelo", "Filtro_Cambio", "Codigo_Cambio"],
    "conversao.csv": ["Tipo_Filtro", "Codigo_Wega", "Codigo_Tecfil"],
}
COLUNAS["cilindradas.csv"] = COLUNAS["catalogo.csv"] + [
    "Litragem_Motor", "Motor_Fonte", "Fonte", "Consultado_em",
]
ANO_NAO_INFORMADO = "Ano não informado"
LITRAGEM_NAO_INFORMADA = "Não informada"
TODAS_LITRAGENS = "Todas as cilindradas"


def extrair_litragens(texto, aceitar_inteiro=False):
    texto = str(texto).strip().replace(",", ".")
    if aceitar_inteiro and re.fullmatch(r"\d{1,2}", texto):
        texto += ".0"
    valores = re.findall(r"(?<![\w.])(\d{1,2}\.\d{1,2})(?![\d.])", texto)
    return tuple(sorted({f"{float(v):.2f}".rstrip("0").rstrip(".")
                         + (".0" if float(v).is_integer() else "")
                         for v in valores if 0.1 <= float(v) <= 20}, key=float))


def litragens_do_registro(row, nome):
    explicita = row.get("Litragem_Motor", "")
    if explicita and str(explicita).lower() not in {"vazio", "nan", "none"}:
        return extrair_litragens(explicita, aceitar_inteiro=True)
    versao = extrair_litragens(row["Classificacao_Modelo"])
    if versao:
        return versao
    # A exportação de câmbio traz a cilindrada após o código da transmissão.
    # Inteiros soltos (XJ 6/8/12, Xedos 6/9) não são cilindradas.
    if nome == "cambio.csv":
        return extrair_litragens(row.get("Extra_0", ""))
    return ()


def filtrar_por_ano(df, ano):
    if ano == ANO_NAO_INFORMADO:
        return df[~df["Periodo_Informado"]]
    return df[(df["Ano_Inicio_Int"] <= int(ano)) & (df["Ano_Fim_Int"] >= int(ano))]


def filtrar_por_litragem(df, litragem):
    if not litragem or litragem == TODAS_LITRAGENS:
        return df
    if litragem == LITRAGEM_NAO_INFORMADA:
        return df[df["Litragens_Motor"].apply(lambda valores: not valores)]
    return df[df["Litragens_Motor"].apply(lambda valores: litragem in valores)]


def converter_ano(valor):
    if pd.isna(valor):
        return None
    texto = str(valor).strip()
    # Datas de fabricação no formato mês/ano, como 12/06.
    data = re.fullmatch(r"(0?[1-9]|1[0-2])/(\d{2}|\d{4})", texto)
    if data:
        texto = data[2]
    if not re.fullmatch(r"\d{1,4}(?:\.0+)?", texto):
        return None
    ano = int(float(texto))
    if ano < 100:
        ano += 1900 if ano > 50 else 2000
    return ano if 1886 <= ano <= 2100 else None


def ler_csv(conteudo, nome):
    """Aceita CSV com cabeçalhos ou exportações posicionais do catálogo."""
    try:
        texto = conteudo.decode("utf-8-sig")
    except UnicodeDecodeError:
        texto = conteudo.decode("cp1252")
    try:
        linhas = [r for r in csv.reader(io.StringIO(texto), delimiter=";", strict=True)
                  if any(c.strip() for c in r)]
    except csv.Error as exc:
        raise ValueError(f"CSV malformado: {exc}") from exc
    if not linhas:
        raise ValueError("O arquivo está vazio.")
    esperadas = COLUNAS[nome]
    primeira = [c.strip() for c in linhas[0]]
    tem_cabecalho = any(c in esperadas for c in primeira)
    if tem_cabecalho:
        faltantes = set(esperadas) - set(primeira)
        if faltantes:
            raise ValueError("Colunas ausentes: " + ", ".join(sorted(faltantes)))
        colunas = primeira
        if len(colunas) != len(set(colunas)):
            raise ValueError("O cabeçalho contém colunas duplicadas.")
        dados = linhas[1:]
    else:
        if len(primeira) < len(esperadas):
            raise ValueError(f"Esperadas pelo menos {len(esperadas)} colunas; encontradas {len(primeira)}.")
        colunas = esperadas + [f"Extra_{i}" for i in range(len(primeira) - len(esperadas))]
        dados = linhas
    if not dados:
        raise ValueError("O arquivo não contém registros.")
    for numero, linha in enumerate(dados, 2 if tem_cabecalho else 1):
        if len(linha) != len(colunas):
            raise ValueError(f"Linha {numero}: esperadas {len(colunas)} colunas; encontradas {len(linha)}.")
    df = pd.DataFrame(dados, columns=colunas)
    for coluna in df:
        df[coluna] = df[coluna].str.strip().replace({"nan": "", "None": "", "NAN": ""})
    return df


def normalizar_catalogo(conteudo, nome, ano_atual=None, complemento=b""):
    ano_atual = ano_atual or datetime.now().year
    df = ler_csv(conteudo, nome)
    inicios, finais, validos = [], [], []
    avisos = []
    for indice, row in df.iterrows():
        inicio, fim = row["Ano_Inicio"], row["Ano_Fim"]
        intervalo = re.fullmatch(r"(\d{2}|\d{4})\s*[–—-]\s*(\d{2}|\d{4})", inicio)
        if intervalo:
            inicio = intervalo[1]
            if not fim:
                fim = intervalo[2]
        ini = converter_ano(inicio) if inicio else None
        final = converter_ano(fim) if fim else (ano_atual if inicio else None)
        if ((inicio and ini is None) or (fim and final is None)
                or (ini is not None and final is not None and ini > final)):
            avisos.append(f"Registro {indice + 1} ({row['Nome_Montadora']} {row['Nome_Modelo']}) ignorado: período inválido ({row['Ano_Inicio']} a {row['Ano_Fim']}).")
            continue
        if not row["Nome_Montadora"] or not row["Nome_Modelo"]:
            avisos.append(f"Registro {indice + 1} ignorado: montadora ou modelo ausente.")
            continue
        validos.append(indice)
        inicios.append(ini)
        finais.append(final)
    if not validos:
        raise ValueError("Nenhum registro com identificação e período válidos. " + " ".join(avisos[:3]))
    df = df.loc[validos].copy()
    df["Ano_Inicio_Int"] = pd.array(inicios, dtype="Int64")
    df["Ano_Fim_Int"] = pd.array(finais, dtype="Int64")
    df["Periodo_Informado"] = df["Ano_Inicio_Int"].notna()
    if nome == "catalogo.csv" and complemento:
        motores = ler_csv(complemento, "cilindradas.csv")
        chaves = COLUNAS["catalogo.csv"]
        referencias = {}
        for chave, valor in zip(motores[chaves].itertuples(index=False, name=None), motores["Litragem_Motor"]):
            if chave in referencias and referencias[chave] != valor:
                raise ValueError("Há cilindradas conflitantes para a mesma aplicação no complemento.")
            referencias[chave] = valor
        if "Litragem_Motor" not in df:
            df["Litragem_Motor"] = ""
        valores = pd.Series([referencias.get(chave, "") for chave in df[chaves].itertuples(index=False, name=None)],
                            index=df.index, dtype="str")
        sem_valor = df["Litragem_Motor"].str.lower().isin(["", "vazio"])
        df.loc[sem_valor, "Litragem_Motor"] = valores[sem_valor]
    df["Litragens_Motor"] = df.apply(lambda row: litragens_do_registro(row, nome), axis=1)
    df.attrs["avisos"] = list(dict.fromkeys(avisos))
    return df


def localizar_csv(nome, pasta):
    return next((p for p in (Path(pasta) / nome, Path(pasta) / "data" / nome, Path(nome))
                 if p.is_file()), None)


def ler_conversoes(conteudo):
    df = ler_csv(conteudo, "conversao.csv")
    referencias = {}
    for _, row in df.iterrows():
        wega = row["Codigo_Wega"].replace("\xa0", "").upper()
        tecfil = row["Codigo_Tecfil"].replace("\xa0", "").upper()
        if wega and tecfil and tecfil not in {"N/A", "NONE"}:
            referencias.setdefault(wega, [])
            if tecfil not in referencias[wega]:
                referencias[wega].append(tecfil)
    return {wega: " / ".join(codigos) for wega, codigos in referencias.items()}
