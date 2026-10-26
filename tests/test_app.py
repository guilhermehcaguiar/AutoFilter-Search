import shutil
import tempfile
import unittest
from pathlib import Path

from streamlit.testing.v1 import AppTest

ROOT = Path(__file__).resolve().parents[1]
SELECIONE = "— Selecione —"


class AppTestCase(unittest.TestCase):
    def abrir(self, botao):
        at = AppTest.from_file(str(ROOT / "app.py"), default_timeout=20).run()
        at.button(botao).click().run()
        self.assertFalse(at.exception)
        self.assertFalse(at.error)
        return at

    def selecionar_primeira_aplicacao(self, at):
        for campo in ["sel_montadora", "sel_modelo", "sel_ano", "sel_versao"]:
            widget = at.selectbox(campo)
            widget.select(widget.options[1]).run()
            self.assertFalse(at.exception)
        return at

    def test_consulta_limpeza_e_retorno_nos_tres_modulos(self):
        for botao, passo in [("btn_rev", 5), ("btn_palh", 5), ("btn_cam", 6)]:
            with self.subTest(botao=botao):
                at = self.selecionar_primeira_aplicacao(self.abrir(botao))
                self.assertEqual(at.session_state["step"], passo)
                self.assertTrue(at.get("html"))
                if botao == "btn_palh":
                    self.assertEqual(at.selectbox("sel_versao").value, "Versão Única / Padrão")
                at.button("limpar_filtros").click().run()
                self.assertFalse(at.exception)
                self.assertEqual(at.selectbox("sel_montadora").value, SELECIONE)
                self.assertEqual(at.session_state["step"], 1)
                self.assertFalse(at.get("html"))
                at.button("voltar_cons").click().run()
                self.assertEqual(len(at.button), 3)

    def test_mudar_ano_modelo_e_montadora_limpa_dependentes(self):
        at = self.selecionar_primeira_aplicacao(self.abrir("btn_rev"))
        ano = at.selectbox("sel_ano")
        ano.select(ano.options[2]).run()
        self.assertEqual(at.session_state["step"], 4)
        self.assertEqual(at.selectbox("sel_versao").value, SELECIONE)
        at.selectbox("sel_modelo").select(SELECIONE).run()
        self.assertEqual(at.session_state["step"], 2)
        self.assertFalse(at.get("html"))
        at.selectbox("sel_montadora").select("Audi").run()
        self.assertEqual(at.selectbox("sel_modelo").value, SELECIONE)
        self.assertFalse(at.exception)

    def test_todas_configuracoes_do_audi_a3_aparecem(self):
        at = self.abrir("btn_rev")
        for campo, valor in [("sel_montadora", "Audi"), ("sel_modelo", "A3"),
                             ("sel_ano", "2010"),
                             ("sel_versao", "TFSI ‐ (Sport / Sportback) ‐ gasolina ‐ automático / mecânico")]:
            at.selectbox(campo).select(valor).run()
        self.assertFalse(at.exception)
        html = "\n".join(el.proto.body for el in at.get("html"))
        for codigo in ["FAP6012", "FAP9025", "WO592", "WOE640"]:
            self.assertIn(codigo, html)
        self.assertGreaterEqual(len(at.get("html")), 2)

    def test_selecao_manual_de_transmissao(self):
        at = self.abrir("btn_cam")
        for campo, valor in [("sel_montadora", "Audi"), ("sel_modelo", "A5"),
                             ("sel_ano", "2014"), ("sel_versao", "1.8 TFSI")]:
            at.selectbox(campo).select(valor).run()
        self.assertEqual(at.session_state["step"], 5)
        at.selectbox("sel_transmissao").select("VL380 / VL381").run()
        self.assertEqual(at.session_state["step"], 6)
        html = "\n".join(el.proto.body for el in at.get("html"))
        self.assertIn("WFC-210", html)
        self.assertNotIn("WFC-214", html)
        at.selectbox("sel_transmissao").select("— Qual a transmissão do veículo? —").run()
        self.assertEqual(at.session_state["step"], 5)
        self.assertFalse(at.get("html"))
        self.assertFalse(at.exception)

    def test_edicao_de_csv_invalida_cache(self):
        with tempfile.TemporaryDirectory() as folder:
            pasta = Path(folder)
            shutil.copy(ROOT / "app.py", pasta / "app.py")
            shutil.copy(ROOT / "data" / "conversao.csv", pasta / "conversao.csv")
            arquivo = pasta / "catalogo.csv"
            arquivo.write_text("Marca A;Modelo;;2000;2010;A;O;C;X\n")
            at = AppTest.from_file(str(pasta / "app.py"), default_timeout=20).run()
            at.button("btn_rev").click().run()
            self.assertIn("Marca A", at.selectbox("sel_montadora").options)
            arquivo.write_text("Marca B;Modelo;;2000;2010;A;O;C;X\n")
            at.run()
            self.assertIn("Marca B", at.selectbox("sel_montadora").options)
            self.assertNotIn("Marca A", at.selectbox("sel_montadora").options)
            self.assertFalse(at.exception)

    def test_cilindrada_filtra_cambio_e_limpa_versao(self):
        at = self.abrir("btn_cam")
        self.assertTrue(at.selectbox("sel_litragem").disabled)
        for campo, valor in [("sel_montadora", "Audi"), ("sel_modelo", "A3"), ("sel_ano", "2010")]:
            at.selectbox(campo).select(valor).run()
        at.selectbox("sel_litragem").select("1.6").run()
        versoes = at.selectbox("sel_versao").options
        self.assertIn("1.6 E 1.8", versoes)
        self.assertNotIn("2.0", versoes)
        at.selectbox("sel_versao").select("1.6 E 1.8").run()
        self.assertEqual(at.session_state["step"], 6)
        self.assertIn("WFC-538", "\n".join(el.proto.body for el in at.get("html")))
        at.selectbox("sel_litragem").select("2.0").run()
        self.assertEqual(at.selectbox("sel_versao").value, SELECIONE)
        self.assertNotIn("1.6 E 1.8", at.selectbox("sel_versao").options)
        at.button("limpar_filtros").click().run()
        self.assertTrue(at.selectbox("sel_litragem").disabled)
        self.assertFalse(at.exception)

    def test_revisao_sem_cilindrada_nao_bloqueia_consulta(self):
        at = self.abrir("btn_rev")
        for campo, valor in [("sel_montadora", "Stihl"), ("sel_modelo", "Roçadeira"), ("sel_ano", "Ano não informado")]:
            at.selectbox(campo).select(valor).run()
        self.assertEqual(at.selectbox("sel_litragem").options, ["Não informada"])
        self.assertTrue(at.selectbox("sel_litragem").disabled)
        versao = at.selectbox("sel_versao")
        versao.select(versao.options[1]).run()
        self.assertTrue(at.get("html"))
        self.assertFalse(at.exception)

    def test_audi_a3_2010_mostra_cilindrada_na_revisao(self):
        at = self.abrir("btn_rev")
        for campo, valor in [("sel_montadora", "Audi"), ("sel_modelo", "A3"), ("sel_ano", "2010")]:
            at.selectbox(campo).select(valor).run()
        self.assertFalse(at.toggle)
        self.assertIn("2.0 L", at.selectbox("sel_litragem").options)
        at.selectbox("sel_litragem").select("2.0").run()
        versao = at.selectbox("sel_versao")
        versao.select(versao.options[1]).run()
        self.assertFalse(at.exception)
        self.assertEqual(len(at.get("html")), 2)
        self.assertTrue(any("Motor: 2.0 L" == c.value for c in at.caption))

    def test_cilindrada_separa_versoes_e_pecas_da_revisao(self):
        at = self.abrir("btn_rev")
        for campo, valor in [("sel_montadora", "Chevrolet/GM"), ("sel_modelo", "Corsa"), ("sel_ano", "2010")]:
            at.selectbox(campo).select(valor).run()
        self.assertIn("1.4 L", at.selectbox("sel_litragem").options)
        self.assertIn("1.6 L", at.selectbox("sel_litragem").options)
        at.selectbox("sel_litragem").select("1.4").run()
        versao = at.selectbox("sel_versao")
        self.assertEqual(len(versao.options), 2)
        versao.select(versao.options[1]).run()
        html = "\n".join(el.proto.body for el in at.get("html"))
        self.assertIn("FAP3280", html)
        self.assertNotIn("FAP2827", html)
        at.selectbox("sel_litragem").select("1.6").run()
        self.assertEqual(at.selectbox("sel_versao").value, SELECIONE)
        self.assertFalse(at.get("html"))
        self.assertFalse(at.exception)

    def test_registros_corrigidos_sem_avisos_e_consultaveis(self):
        casos = [("btn_rev", "Stihl", "Roçadeira", "Ano não informado"),
                 ("btn_rev", "Renault", "R 25", "Ano não informado"),
                 ("btn_cam", "Nissan", "Pathfinder III", "Ano não informado"),
                 ("btn_palh", "Chery", "Tiggo", "2016")]
        for botao, marca, modelo, ano in casos:
            with self.subTest(modelo=modelo):
                at = self.abrir(botao)
                self.assertFalse(at.warning)
                self.assertFalse(at.expander)
                for campo, valor in [("sel_montadora", marca), ("sel_modelo", modelo), ("sel_ano", ano)]:
                    at.selectbox(campo).select(valor).run()
                versao = at.selectbox("sel_versao")
                versao.select(versao.options[1]).run()
                self.assertTrue(at.get("html"))
                self.assertFalse(at.exception)

    def test_erro_de_arquivo_sem_excecao_na_interface(self):
        with tempfile.TemporaryDirectory() as folder:
            app = Path(folder) / "app.py"
            shutil.copy(ROOT / "app.py", app)
            at = AppTest.from_file(str(app), default_timeout=20).run()
            # Um arquivo local inválido tem prioridade sobre a pasta de dados.
            (Path(folder) / "catalogo.csv").write_text("Nome_Modelo;Ano_Inicio\nA;2000")
            at.button("btn_rev").click().run()
            self.assertFalse(at.exception)
            self.assertTrue(at.error)
            self.assertIn("Colunas ausentes", at.error[0].value)
