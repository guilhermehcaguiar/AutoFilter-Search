# 🔧 Sistema de Filtros Automotivos

Sistema de consulta de filtros automotivos desenvolvido para uso interno em oficina mecânica. Desenvolvido com Python e Streamlit, roda localmente no notebook do balcão sem necessidade de internet.

---

## 📋 Funcionalidades

- **Menu Multi-Módulos**: Navegação centralizada entre diferentes catálogos de peças.
- **Módulo Revisão Básica**: Busca rápida por códigos de **Filtros de Ar, Óleo, Combustível e Cabine**.
- **Módulo Palhetas**: Busca de palhetas **Dianteiras (Condutor/Passageiro), Traseiras e Tipos de Encaixe**.
- **Módulo Câmbio**: *(Em desenvolvimento)* Preparado para consulta de filtros de transmissão
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
│   ├── catalogo.csv    # Base de dados dos filtros (Revisão)
│   ├── palhetas.csv    # Base de dados de limpadores (Palhetas)
│   └── cambio.csv      # Base de dados de transmissão (Em breve)
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

Os arquivos dentro da pasta data/ (ou na raiz) devem usar ; como separador. As 5 primeiras colunas são padrão para o sistema de funil.

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

---

## 🛠️ Tecnologias

- [Python 3](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)

---

## 🚀 Atalho para a Oficina (Windows)

Para facilitar o uso no dia a dia, o projeto inclui um arquivo `.bat` que permite criar o ambiente, instalar as bibliotecas e abrir o sistema com apenas dois cliques, sem precisar abrir o terminal manualmente.

1. Localize o arquivo `INICIAR.bat` na pasta raiz.
2. (Opcional) Clique com o botão direito e selecione **Enviar para > Área de trabalho (criar atalho)**.
3. Basta clicar no ícone para o sistema ativar o ambiente virtual e abrir o navegador automaticamente.

---

## 👨‍💻 Autor

Desenvolvido por Guilherme Aguiar
