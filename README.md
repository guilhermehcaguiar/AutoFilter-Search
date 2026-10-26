# 🔧 Sistema de Filtros Automotivos

Sistema de consulta de filtros automotivos desenvolvido para uso interno em oficina mecânica. Desenvolvido com Python e Streamlit, roda localmente no notebook do balcão sem necessidade de internet.

---

## 📋 Funcionalidades

- **Menu Multi-Módulos**: Navegação centralizada entre diferentes catálogos de peças.
- **Módulo Revisão Básica**: Busca rápida por códigos de **Filtros de Ar, Óleo, Combustível e Cabine**.
- **Módulo Palhetas**: Busca de palhetas **Dianteiras (Condutor/Passageiro), Traseiras e Tipos de Encaixe**.
- **Módulo Câmbio**: Consulta de filtros de transmissão **Filtros, Código da transmissão**.
- **Função de conversão**: Informa as referências cruzadas dos filtros (Wega -- Tecfil).
- **Busca Encadeada Inteligente**: O assistente filtra em 4 etapas lógicas: **Montadora → Modelo Base → Ano → Versão/Geração**.
- **Tratamento de Dados**: 
  - Converte anos de 2 dígitos automaticamente (ex: `95` → `1995`).
  - Identifica modelos sem "ano de fim" como fabricados até ao ano atual.
  - Oculta o menu padrão do Streamlit para manter o visual limpo

---

## 📁 Estrutura do Projeto

```
AutoFilter-Search/
│
├── app.py              # Código fonte principal do sistema
│
├── data/
│   ├── cambio.csv      # Base de dados de transmissão (Câmbio)
|   ├── catalogo.csv    # Base de dados dos filtros (Revisão)
|   ├── conversao       # Base de dados para conversão de referências entre wega e tecfil
│   ├── palhetas.csv    # Base de dados de limpadores (Palhetas)
│
├── .gitignore          # Arquivos ignorados pelo Git 
├── requirements.txt    # Bibliotecas dependentes do projeto
├── INICIAR.bat         # Script inteligente de inicialização para Windows
└── README.md           # Este arquivo
```

---

## ⚙️ Instalação

**1. Clone o repositório**
```bash
git clone https://github.com/guilhermehcaguiar/AutoFilter-Search
cd AutoFilter-Search
```

Requer Python **3.11 ou superior**. No Linux, use `./INICIAR.sh`; no Windows, abra `INICIAR.bat`. Os atalhos criam ou reparam o ambiente `.venv` quando necessário. A instalação das dependências precisa de internet; as consultas funcionam offline.

**2. Instale as dependências manualmente (opcional)**
```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows:
# .venv\Scripts\activate
python -m pip install -r requirements.txt
```

**3. Rode o sistema**
```bash
python -m streamlit run app.py
```

O sistema abrirá automaticamente no navegador em `http://localhost:8501`.

---

## 🗂️ Formato do CSV

Os arquivos dentro da pasta `data/` (ou na raiz) devem usar `;` como separador. São aceitos UTF-8 (com ou sem BOM) e Windows-1252. Com cabeçalhos, as colunas podem estar em qualquer ordem. Exportações sem cabeçalhos usam a ordem das tabelas abaixo; colunas extras ao final são preservadas. No câmbio, a versão vem depois dos anos.

Anos podem ter dois ou quatro dígitos, inclusive datas como `12/06`. Um intervalo como `14 – 16` na coluna inicial é interpretado como 2014–2016 quando o fim estiver vazio. Com início informado, fim vazio significa o ano atual. Registros sem início confirmado aparecem na opção **Ano não informado**, sem presumir 1990 nem misturar a aplicação com anos conhecidos. Registros com períodos inválidos são ignorados na consulta e identificados nos avisos do módulo. Erros de estrutura do CSV são apresentados na interface. As correções dos dados e suas fontes estão em [Correções dos catálogos](docs/correcoes-dados.md).

Alterações nos CSVs são lidas na próxima interação com a aplicação. Quando uma seleção corresponde a várias aplicações de peças, todas são exibidas separadamente como “Aplicação possível”, mantendo a associação entre os códigos e os encaixes. Essas opções não confirmam configurações distintas do veículo: a interface orienta conferir o código do motor, o chassi ou a referência da peça instalada antes de escolher. Versões vazias aparecem como “Versão Única / Padrão”.

Após selecionar montadora, modelo e ano, o campo **Cilindrada do motor** aparece diretamente nos módulos Revisão ou Câmbio e filtra as versões e os resultados por valores como 1.6 ou 2.0 L. “Todas as cilindradas” mantém a consulta completa; “Não informada” consulta os registros sem esse dado. Trocar a cilindrada limpa a versão e a transmissão anteriores. Por exemplo: **Revisão → Audi → A3 → 2010 → 2.0 L**; **Revisão → Chevrolet/GM → Corsa → 2010** permite escolher entre 1.4 L e 1.6 L.

Em CSVs com cabeçalhos, a coluna opcional `Litragem_Motor` pode informar a cilindrada (`1.6`, `1,6`, `2.0` ou `1.6 / 1.8`). Sem essa coluna, são aproveitados valores explícitos na versão; na exportação sem cabeçalhos de câmbio, também é lida a primeira coluna extra. Valores como XJ 6/8/12, V6 ou 16V não são tratados como cilindrada.

Na revisão, `data/cilindradas.csv` complementa 1.776 registros com cilindradas obtidas do catálogo online oficial da Wega. A associação exige montadora, modelo, versão e período correspondentes, combustível compatível e uma única cilindrada encontrada. Casos ambíguos ficam sem atribuição automática. O complemento mantém o motor original, a URL da fonte e a data da consulta, e funciona offline. A aplicação só utiliza a associação se todos os campos originais da linha, incluindo os códigos das peças, continuarem iguais.

### 1. Revisão (catalogo.csv)
| Coluna | Descrição |
|---|---|
| `Nome_Montadora` | Fabricante (ex: Ford, Volkswagen) |
| `Nome_Modelo` | Modelo do veículo (ex: Gol, Fiesta) |
| `Classificacao_Modelo` | Versão/motor específico |
| `Ano_Inicio` | Ano inicial de vigência (2 ou 4 dígitos) |
| `Ano_Fim` | Ano final (vazio = vigente até hoje) |
| `Filtro_Ar` | Código do filtro de ar |
| `Filtro_Oleo` | Código do filtro de óleo |
| `Filtro_Combustivel` | Código do filtro de combustível |
| `Filtro_Cabine` | Código do filtro de cabine |

### 2. Palhetas (palhetas.csv)
| Coluna | Descrição |
|---|---|
| `Nome_Montadora` | Fabricante (ex: Ford, Volkswagen) |
| `Nome_Modelo` | Modelo do veículo (ex: Gol, Fiesta) |
| `Classificacao_Modelo` | Geração ou Carroçaria |
| `Ano_Inicio` | Ano inicial de vigência (2 ou 4 dígitos) |
| `Ano_Fim` | Ano final (vazio = vigente até hoje) |
| `Palheta_Motorista` | Código(s) lado do condutor |
| `Palheta_Passageiro` | Código(s) lado do passageiro |
| `Palheta_Traseira` | Código(s) vidro traseiro |
| `Tipo_Gancho` | Padrão do encaixe (ex: G, TL1, SL1) |

### 3. Câmbio (cambio.csv)
| Coluna | Descrição |
|---|---|
| `Nome_Montadora` | Fabricante | `Audi`, `BMW`, `Toyota` |
| `Nome_Modelo` | Modelo do veículo (ex: A3, Corolla, Golf) |
| `Ano_Inicio` | Ano inicial de vigência (2 ou 4 dígitos) |
| `Ano_Fim` | Ano final (vazio = vigente até hoje) |
| `Classificacao_Modelo` | Versão/motor específico |
| `Filtro_Cambio` | Códigos de referência técnica do filtro (ex: WOEC-003, WOEC-005) |
| `Codigo_Cambio` | Código oficial ou família da transmissão (ex: DSG, ZF 8HP)

### 4. Conversão (conversao.csv)
| Coluna | Descrição |
|---|---|
| `Tipo_Filtro` | Tipo de filtro (ex: Óleo, Combustível) |
| `Codigo_Wega` | Referência pela Wega (ex: WO120, FAP3286) |
| `Codigo_Tecfil` | Referência pela Tecfil (ex: PSL55, ARL8830) |



---

## 🛠️ Tecnologias

- [Python 3](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)

## Verificação

Com o ambiente virtual ativado:

```bash
python -m unittest discover -s tests -v
python -m pip check
```

Os testes cobrem leitura dos catálogos, datas, conversões e os fluxos de consulta, troca de seleção, limpeza e resultados alternativos dos módulos Streamlit.

---

## 🚀 Atalho para a Oficina (Windows)

Para facilitar o uso no dia a dia, o projeto inclui um arquivo `.bat` que permite criar o ambiente, instalar as bibliotecas e abrir o sistema com apenas dois cliques, sem precisar abrir o terminal manualmente.

1. Localize o arquivo `INICIAR.bat` na pasta raiz.
2. (Opcional) Clique com o botão direito e selecione **Enviar para > Área de trabalho (criar atalho)**.
3. Basta clicar no ícone para o sistema ativar o ambiente virtual e abrir o navegador automaticamente.

---

## 👨‍💻 Autor

Desenvolvido por Guilherme Aguiar
