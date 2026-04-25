# 🔧 Sistema de Filtros Automotivos

Sistema de consulta de filtros automotivos desenvolvido para uso interno em oficina mecânica. Desenvolvido com Python e Streamlit, roda localmente no notebook do balcão sem necessidade de internet.

---

## 📋 Funcionalidades

- Busca encadeada em 4 etapas: **Montadora → Modelo → Ano → Versão**
- Exibe os códigos de **Filtro de Ar, Óleo, Combustível e Cabine**
- Base com **2.519 entradas** e **56 montadoras**
- Converte anos de 2 dígitos automaticamente (ex: `95` → `1995`)
- Modelos sem ano de fim são considerados vigentes até hoje
- Interface escura otimizada para uso em balcão

---

## 📁 Estrutura do Projeto

```
filtros-auto/
│
├── app.py              # sistema principal (Streamlit)
│
├── data/
│   └── catalogo.csv    # base de dados dos filtros
│
├── .gitignore          # arquivos ignorados pelo Git
├── requirements.txt    # dependências do projeto
└── README.md           # este arquivo
```

---

## ⚙️ Instalação

**1. Clone o repositório**
```bash
git clone https://github.com/guilhermehcaguiar/AutoFilter-Search
cd AutoFilter-Search
```

**2. Instale as dependências**
```bash
pip install -r requirements.txt
```

**3. Rode o sistema**
```bash
streamlit run app.py
```

O sistema abrirá automaticamente no navegador em `http://localhost:8501`.

---

## 🗂️ Formato do CSV

O arquivo `data/catalogo.csv` usa `;` como separador e deve conter as colunas:

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

---

## 🛠️ Tecnologias

- [Python 3](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)

---

## 🚀 Atalho para a Oficina (Windows)

Para facilitar o uso no dia a dia, o projeto inclui um arquivo `.bat` que permite abrir o sistema com apenas dois cliques, sem precisar abrir o terminal manualmente.

1. Localize o arquivo `Iniciar_Sistema.bat` na pasta raiz.
2. (Opcional) Clique com o botão direito e selecione **Enviar para > Área de trabalho (criar atalho)**.
3. Basta clicar no ícone para o sistema ativar o ambiente virtual e abrir o navegador automaticamente.

---

## 👨‍💻 Autor

Desenvolvido por Guilherme Aguiar
