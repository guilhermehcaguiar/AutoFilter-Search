import csv
import io
import unittest

from catalogos import COLUNAS, normalizar_catalogo
from scripts.importar_cilindradas import complementar, ler_aplicacoes


def resposta(motor="2.0 - Gasolina - 16V - 200 cv", ano="06 -- 13"):
    return {"success": True, "data": f'''<ul class="conteudo elemento mostrar espacamento">
        <li>Leve</li><li>Passeio</li><li>Audi</li>
        <li><a href="https://www.wegamotors.com/busca-veiculo/?CodModelo=A86644&amp;motor=2.0">A3</a></li>
        <li>TFSI - (Sport / Sportback) - AT. / MT.</li><li>{motor}</li><li>{ano}</li></ul>'''}


def catalogo():
    return normalizar_catalogo(
        "Audi;A3;TFSI ‐ (Sport / Sportback) ‐ gasolina ‐ automático / mecânico;06;13;FAP6012;WO592;FCI1304;AKX1100\n".encode(),
        "catalogo.csv")


def complemento(registros):
    s = io.StringIO()
    w = csv.DictWriter(s, fieldnames=COLUNAS["cilindradas.csv"], delimiter=";")
    w.writeheader()
    w.writerows(registros)
    return s.getvalue().encode()


class ImportarCilindradasTest(unittest.TestCase):
    def test_associacao_por_versao_periodo_e_combustivel(self):
        entradas = ler_aplicacoes(resposta())
        registros = complementar(catalogo(), entradas)
        self.assertEqual(len(registros), 1)
        self.assertEqual(registros[0]["Litragem_Motor"], "2.0")
        self.assertIn("Motor_Fonte", registros[0])
        self.assertIn("&motor=2.0", registros[0]["Fonte"])
        self.assertFalse(complementar(catalogo(), ler_aplicacoes(resposta(ano="14 -- 20"))))
        self.assertFalse(complementar(catalogo(), ler_aplicacoes(resposta(motor="2.0 - Diesel"))))

    def test_cilindradas_ambiguas_nao_sao_atribuidas(self):
        entradas = ler_aplicacoes(resposta()) + ler_aplicacoes(resposta(motor="1.8 - Gasolina"))
        self.assertFalse(complementar(catalogo(), entradas))

    def test_complemento_exige_mesmos_codigos_de_pecas(self):
        registros = complementar(catalogo(), ler_aplicacoes(resposta()))
        df = catalogo()
        bruto = (";".join(COLUNAS["catalogo.csv"]) + "\n"
                 + ";".join(df.iloc[0][COLUNAS["catalogo.csv"]].tolist()) + "\n").encode()
        enriquecido = normalizar_catalogo(bruto, "catalogo.csv", complemento=complemento(registros))
        self.assertEqual(enriquecido.iloc[0].Litragens_Motor, ("2.0",))
        outro = normalizar_catalogo(bruto.replace(b"FAP6012", b"FAP9025"), "catalogo.csv", complemento=complemento(registros))
        self.assertEqual(outro.iloc[0].Litragens_Motor, ())

    def test_resposta_invalida_nao_e_importada(self):
        with self.assertRaises(ValueError):
            ler_aplicacoes({"success": False, "data": "Erro"})
