# Correções dos catálogos

Revisão de 26/10/2026. As alterações preservam os códigos de peças existentes. Períodos de produção de veículos não foram usados como substitutos do período de aplicação de uma peça.

| Arquivo / registro | Valor anterior | Ajuste | Evidência |
| --- | --- | --- | --- |
| `palhetas.csv` / Chery Tiggo | 2009–2006 | 2009–2016 | O catálogo Dyna de 2021 informa `09 / 16`, conexão G e referência convencional 368. A edição 2025 tem `09 / 06`, um período invertido. |
| `cambio.csv` / Nissan Pathfinder III, WFC-971 | `1`–`96`, interpretados como 2001–1996 | Anos vazios; consulta por **Ano não informado**. Nome padronizado como Pathfinder III. | O catálogo Wega 2023–2024 confirma Pathfinder III 4.0 / 2.5, WFC-971 e as transmissões RE5R05A / A5SR1 / A5SR2, mas não informa anos nessa aplicação. |
| `catalogo.csv` / Renault R 25, WR275 / FCI1105A | 1984–1982 | Anos vazios; consulta por **Ano não informado** | O PDF Wega 2023–2024 também contém `84 -- 82`. Sem confirmação do período dessas peças, não foi presumido um ano final. |
| `catalogo.csv` / Stihl Perfurador de Solo e Roçadeira | Anos vazios, anteriormente tratados como 1990–ano atual | Consulta por **Ano não informado**, preservando os nove equipamentos e suas versões | O PDF Wega fornece a referência FAP1050, sem período de fabricação. |

Fontes:

- [Catálogo Dyna de 2021, edição do fabricante distribuída pelo Canal da Peça](https://s3.sa-east-1.amazonaws.com/bd-sp.canaldapeca.com.br/DYNA/21102021/Cat%C3%A1logo_Dyna.pdf).
- [Catálogo Dyna 2025, com o período invertido](https://dyna.com.br/wp-content/uploads/2025/04/Catalogo-Dyna-2025.pdf).
- [Wega, linha leve 2023–2024](https://www.wegamotors.com/wp-content/uploads/2024/06/catalogo-wega-linha-leve-2023-2024.pdf), também disponível em `docs/catalogos/catalogo-wega-linha-leve-2023-2024.pdf`.
- [Wega, câmbio automático 2023–2024](https://wegaes.sincrosites.com.br/wp-content/uploads/2024/06/catalogo-cambio-aut-wega-2023-2024.pdf), também disponível em `docs/catalogos/catalogo-cambio-aut-wega-2023-2024.pdf`, aplicação WFC-971 na página impressa 19.

Os registros sem período confirmado continuam disponíveis, explicitamente separados das aplicações por ano. O validador continua sinalizando períodos invertidos caso novas inconsistências sejam introduzidas.

## Cilindrada

O filtro usa a coluna opcional `Litragem_Motor`, números explícitos na descrição da versão e a coluna extra da exportação de câmbio. Descrições com vários motores, como `1.6 E 1.8`, participam das duas opções. O valor da coluna extra não elimina motores adicionais presentes na versão.

Na base atual, 390 dos 449 registros de câmbio têm cilindrada explícita. O CSV original da revisão não informa cilindrada: os valores soltos 6, 8, 9 e 12 correspondem a descrições de modelos ou versões, e não são convertidos em litros.

### Complemento da revisão

Em 26/10/2026 foram consultadas as categorias Passeio e SUVs / Pick-Ups / Jipes no [catálogo online oficial Wega](https://www.wegamotors.com/). A pesquisa pública por aplicações retorna montadora, modelo, descrição, motor e ano. O importador em `scripts/importar_cilindradas.py` compara esses campos com a revisão e só atribui uma cilindrada quando a associação é inequívoca e o combustível é compatível.

O arquivo `data/cilindradas.csv` guarda 1.774 associações distintas, que completam 1.776 registros do catálogo (incluindo linhas repetidas). As demais linhas permanecem explicitamente sem cilindrada; não são associadas apenas pelo nome do modelo ou pelo código de um filtro.

Para a consulta da imagem relatada pelo usuário, **Audi A3 2010**, a aplicação `TFSI - (Sport / Sportback) - AT. / MT.` corresponde ao motor **2.0 - Gasolina - 16V - 200 cv**, período 2006–2013. A [aplicação oficial do FAP6012](https://www.wegamotors.com/produto/?cod=FAP6012&countrie=br) também informa esse motor. Na revisão do sistema, a opção passa a aparecer como **2.0 L**.

O seletor de cilindrada fica diretamente abaixo do ano, sem interruptor auxiliar. A cilindrada também é exibida junto aos resultados.

Para reproduzir a importação, salve as respostas JSON de `https://www.wegamotors.com/wp-admin/admin-ajax.php` com os parâmetros GET `action=wega_search`, `search=busca-avancada`, `countrie=br`, `lang=pt` e `categoria=Passeio` ou `categoria=SUVs / Pick-Ups / Jipes`. Execute, com o ambiente ativado:

```bash
python scripts/importar_cilindradas.py passeio.json suvs.json
```

O script não faz requisições durante o uso da aplicação. Mudanças no conteúdo do complemento invalidam o cache assim como mudanças nos catálogos.
