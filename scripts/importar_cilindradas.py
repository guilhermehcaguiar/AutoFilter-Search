"""Importa cilindradas das respostas públicas do catálogo Wega, para uso offline.

Não associa motores apenas por modelo: exige montadora, modelo, versão,
combustível compatível e período iguais, com uma única cilindrada confirmada.
"""

import argparse
import csv
import html
import json
import re
import sys
import unicodedata
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from catalogos import COLUNAS, converter_ano, extrair_litragens, normalizar_catalogo


def normalizar_texto(valor):
    texto = unicodedata.normalize("NFKD", str(valor)).encode("ascii", "ignore").decode().lower()
    texto = re.sub(r"\bautomatic[oa]\b", "at", texto)
    texto = re.sub(r"\bmecanic[oa]\b", "mt", texto)
    texto = re.sub(r"\b(gasolina|diesel|flex|alcool|eletrico|gas|gnv)\b", "", texto)
    return re.sub(r"[^a-z0-9]", "", texto)


def montadora(valor):
    texto = normalizar_texto(valor)
    return {"chevroletgm": "chevrolet", "chanachangan": "chana"}.get(texto, texto)


def combustiveis(valor):
    texto = unicodedata.normalize("NFKD", str(valor)).encode("ascii", "ignore").decode().lower()
    tipos = set(re.findall(r"\b(gasolina|diesel|alcool|flex|eletrico|gnv)\b", texto))
    if "flex" in tipos:
        tipos.update({"gasolina", "alcool"})
    return tipos


def periodo(texto):
    texto = texto.strip().replace("-->", "").strip()
    partes = re.split(r"\s*(?:--|[–—‐-])\s*", texto)
    inicio = converter_ano(partes[0]) if partes else None
    fim = converter_ano(partes[1]) if len(partes) == 2 else None
    return inicio, fim


def ler_aplicacoes(resposta):
    if not resposta.get("success") or not isinstance(resposta.get("data"), str):
        raise ValueError("A consulta Wega não retornou aplicações válidas.")
    entradas = []
    blocos = re.findall(r'<ul class="conteudo elemento mostrar espacamento">(.*?)</ul>',
                        resposta["data"], re.S)
    for bloco in blocos:
        celulas = [html.unescape(re.sub(r"<[^>]+>", "", v)).strip()
                   for v in re.findall(r"<li[^>]*>(.*?)</li>", bloco, re.S)]
        if len(celulas) != 7:
            continue
        linha, _, marca, modelo, versao, motor, ano = celulas
        valores = extrair_litragens(motor)
        link = re.search(r'href="([^"]+)"', bloco)
        if linha != "Leve" or not valores or not link:
            continue
        entradas.append({
            "chave": (montadora(marca), normalizar_texto(modelo), normalizar_texto(versao), *periodo(ano)),
            "combustiveis": combustiveis(versao + " " + motor),
            "valores": valores,
            "motor": motor,
            "fonte": html.unescape(link[1]),
        })
    return entradas


def complementar(df, entradas):
    indice = {}
    for entrada in entradas:
        indice.setdefault(entrada["chave"], []).append(entrada)
    registros = []
    for _, row in df.iterrows():
        ano = row["Ano_Inicio"]
        if row["Ano_Fim"]:
            ano += " -- " + row["Ano_Fim"]
        chave = (montadora(row["Nome_Montadora"]), normalizar_texto(row["Nome_Modelo"]),
                 normalizar_texto(row["Classificacao_Modelo"]), *periodo(ano))
        combustivel = combustiveis(row["Classificacao_Modelo"])
        candidatos = [v for v in indice.get(chave, [])
                      if not combustivel or not v["combustiveis"] or combustivel & v["combustiveis"]]
        valores = {valor for c in candidatos for valor in c["valores"]}
        if len(valores) != 1:
            continue
        registro = {coluna: row[coluna] for coluna in COLUNAS["catalogo.csv"]}
        registro.update({
            "Litragem_Motor": next(iter(valores)),
            "Motor_Fonte": " / ".join(sorted({c["motor"] for c in candidatos})),
            "Fonte": " | ".join(sorted({c["fonte"] for c in candidatos})),
            "Consultado_em": date.today().isoformat(),
        })
        registros.append(registro)
    # Linhas idênticas do catálogo não geram associações duplicadas.
    return list({tuple(r.items()): r for r in registros}.values())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("respostas", nargs="+", type=Path)
    parser.add_argument("--catalogo", type=Path, default=Path("data/catalogo.csv"))
    parser.add_argument("--saida", type=Path, default=Path("data/cilindradas.csv"))
    args = parser.parse_args()
    entradas = []
    for arquivo in args.respostas:
        entradas.extend(ler_aplicacoes(json.loads(arquivo.read_text())))
    df = normalizar_catalogo(args.catalogo.read_bytes(), "catalogo.csv")
    registros = complementar(df, entradas)
    if not registros:
        raise ValueError("Nenhuma associação confirmada; o arquivo de saída não foi alterado.")
    with args.saida.open("w", encoding="utf-8", newline="") as arquivo:
        writer = csv.DictWriter(arquivo, fieldnames=list(registros[0]), delimiter=";", lineterminator="\n")
        writer.writeheader()
        writer.writerows(registros)
    print(f"{len(registros)} associações de cilindrada gravadas em {args.saida}.")


if __name__ == "__main__":
    main()
