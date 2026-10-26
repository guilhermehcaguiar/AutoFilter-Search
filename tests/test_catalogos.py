import unittest
from pathlib import Path

from catalogos import (
    COLUNAS, converter_ano, ler_conversoes, ler_csv, normalizar_catalogo,
    extrair_litragens, filtrar_por_ano, filtrar_por_litragem, ANO_NAO_INFORMADO,
)


def csv_catalogo(linhas, cabecalho=True):
    texto = ";".join(COLUNAS["catalogo.csv"]) + "\n" if cabecalho else ""
    return (texto + "\n".join(";".join(row) for row in linhas)).encode("utf-8-sig")


class CatalogosTest(unittest.TestCase):
    def test_exportacao_sem_cabecalho_preserva_primeiro_registro_e_extras(self):
        row = ["Marca", "Modelo", "", "95", "", "A", "O", "", "", "extra", ""]
        d = normalizar_catalogo(csv_catalogo([row], False), "catalogo.csv", 2026)
        self.assertEqual(len(d), 1)
        self.assertEqual(d.iloc[0].Nome_Montadora, "Marca")
        self.assertEqual(d.iloc[0].Extra_0, "extra")
        self.assertEqual(d.iloc[0].Ano_Inicio_Int, 1995)
        self.assertEqual(d.iloc[0].Ano_Fim_Int, 2026)
        self.assertEqual(d.iloc[0].Classificacao_Modelo, "")

    def test_cabecalho_com_acentos_espacos_e_ordem_diferente(self):
        cols = COLUNAS["catalogo.csv"][::-1]
        values = ["Marca", "Veículo", "Versão", "2001", "2005", "A", "O", "C", "X"][::-1]
        data = (";".join(" " + c + " " for c in cols) + "\n" + ";".join(values)).encode("cp1252")
        d = normalizar_catalogo(data, "catalogo.csv")
        self.assertEqual(d.iloc[0].Nome_Modelo, "Veículo")
        self.assertEqual(d.iloc[0].Ano_Fim_Int, 2005)

    def test_datas_por_mes_e_intervalos(self):
        rows = [["M", "A", "", "12/06", "09/10", "", "", "", ""],
                ["M", "B", "", "14 – 16", "", "", "", "", ""]]
        d = normalizar_catalogo(csv_catalogo(rows), "catalogo.csv")
        self.assertEqual(d.Ano_Inicio_Int.tolist(), [2006, 2014])
        self.assertEqual(d.Ano_Fim_Int.tolist(), [2010, 2016])

    def test_periodo_invalido_e_sinalizado_sem_bloquear_validos(self):
        rows = [["M", "A", "", "2009", "2006", "", "", "", ""],
                ["M", "B", "", "2000", "", "", "", "", ""]]
        d = normalizar_catalogo(csv_catalogo(rows), "catalogo.csv")
        self.assertEqual(d.Nome_Modelo.tolist(), ["B"])
        self.assertIn("período inválido", d.attrs["avisos"][0])

    def test_entrada_invalida_mostra_erro_claro(self):
        for content in [b"", b"Nome_Modelo;Ano_Inicio\nA;2000", b"a;b", b'"abc',
                        csv_catalogo([["M", "A", "", "2005", "2000", "", "", "", ""]])]:
            with self.subTest(content=content), self.assertRaises(ValueError):
                normalizar_catalogo(content, "catalogo.csv")

    def test_anos_invalidos_nao_sao_convertidos_silenciosamente(self):
        for value in ["abc", "-1", "2010.5", "99999", "13/06", None]:
            with self.subTest(value=value):
                self.assertIsNone(converter_ano(value))
        self.assertEqual(converter_ano("95"), 1995)
        self.assertEqual(converter_ano("03"), 2003)

    def test_conversoes_preservam_multiplas_referencias(self):
        data = b"Tipo_Filtro;Codigo_Wega;Codigo_Tecfil\nOleo;wo1;PSL1\nOleo;WO1;PSL2\nOleo;WO1;PSL1\nOleo;;PSL3\nOleo;WO2;\n"
        self.assertEqual(ler_conversoes(data), {"WO1": "PSL1 / PSL2"})

    def test_ano_ausente_nao_inventa_periodo(self):
        d = normalizar_catalogo(csv_catalogo([["Stihl", "Roçadeira", "FS120", "", "", "FAP1050", "", "", ""]]), "catalogo.csv")
        self.assertFalse(d.attrs["avisos"])
        self.assertFalse(d.iloc[0].Periodo_Informado)
        self.assertTrue(d.Ano_Inicio_Int.isna().all())
        self.assertEqual(len(filtrar_por_ano(d, ANO_NAO_INFORMADO)), 1)
        self.assertTrue(filtrar_por_ano(d, 1990).empty)

    def test_cilindrada_multiplos_motores_e_modelos_numericos(self):
        self.assertEqual(extrair_litragens("1.6 E 1.8 / 2,0 TFSI"), ("1.6", "1.8", "2.0"))
        self.assertEqual(extrair_litragens("XJ 12 / V6 / 16V / Xedos 9"), ())
        self.assertEqual(extrair_litragens("2", aceitar_inteiro=True), ("2.0",))
        data = b"Audi;A3;2000;2010;1.6 E 1.8;WFC-538;01M;1.6;\n"
        d = normalizar_catalogo(data, "cambio.csv")
        self.assertEqual(d.iloc[0].Litragens_Motor, ("1.6", "1.8"))
        self.assertEqual(len(filtrar_por_litragem(d, "1.8")), 1)
        self.assertTrue(filtrar_por_litragem(d, "2.0").empty)

    def test_cilindrada_explicita_em_coluna_opcional(self):
        data = (";".join(COLUNAS["catalogo.csv"] + ["Litragem_Motor"]) + "\n"
                + "Marca;Modelo;Versão;2000;2010;A;O;C;X;1,6\n").encode()
        d = normalizar_catalogo(data, "catalogo.csv")
        self.assertEqual(d.iloc[0].Litragens_Motor, ("1.6",))

    def test_catalogos_reais_carregam_e_preservam_registros_validos(self):
        for name in ["catalogo.csv", "palhetas.csv", "cambio.csv"]:
            with self.subTest(name=name):
                content = (Path(__file__).resolve().parents[1] / "data" / name).read_bytes()
                bruto = ler_csv(content, name)
                d = normalizar_catalogo(content, name)
                ignorados = sum("ignorado:" in a for a in d.attrs["avisos"])
                self.assertEqual(len(d) + ignorados, len(bruto))
                self.assertGreater(len(d), 400)
                self.assertTrue((d.Ano_Inicio_Int <= d.Ano_Fim_Int).all())
