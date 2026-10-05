# Antônio Pedro (55456) — Votos no Acre

Painel interativo com os dados completos do Excel: **2.270 seções, 5.118 votos e 1.332 seções com votos**, no primeiro turno de 04/10/2026. Fotografia da coleta em 05/10/2026.

## Abrir no computador

Abra `index.html` em um navegador. Os dados, o mapa e o código da aplicação estão embutidos no HTML: filtros, gráficos e exportação CSV funcionam sem internet, sem instalação e sem servidor. Os links dos boletins do TSE exigem internet. O botão Excel usa o arquivo da pasta `downloads`.

## Publicar no GitHub Pages

1. Crie um repositório no seu GitHub, por exemplo `votos-antonio-pedro-acre`.
2. Envie `index.html`, `.nojekyll` e a pasta `downloads` para a raiz do repositório. Você pode enviar o restante do projeto também, mas não é necessário para o painel funcionar.
3. No repositório, abra **Settings → Pages**.
4. Em **Build and deployment**, escolha **Deploy from a branch**.
5. Selecione a branch **main** e a pasta **/(root)**. Clique em **Save**.
6. Aguarde a publicação. O GitHub mostrará o endereço, normalmente `https://SEU-USUARIO.github.io/votos-antonio-pedro-acre/`.

O painel usa caminhos relativos e funciona no endereço de um projeto do GitHub Pages. O botão **Compartilhar filtros** copia o endereço com os filtros selecionados. Compartilhe somente um endereço público publicado, não o endereço local do seu computador.

## Recursos

- Filtros combinados por município, zona, código do local, presença de votos, busca e limites mínimo/máximo de votos por seção.
- Resumo da seleção e gráficos por município, zona e local, com barras clicáveis.
- Distribuição da quantidade de votos por seção e cobertura de seções com/sem votos.
- Mapa interativo dos 22 municípios, com cores atualizadas pelos filtros, seleção por clique ou teclado e zoom.
- Tabela com todas as colunas da planilha, ordenação, paginação e link para o boletim original de cada seção. O nome do arquivo é exibido ao passar o mouse sobre “Abrir BU”.
- CSV da seleção e download da planilha Excel completa. Os códigos de zona, seção e município preservam zeros à esquerda no Excel.
- Layout adaptável a celular e computador, sem bibliotecas ou fontes externas.

## O que o mapa representa

Os votos são agrupados **por município**. A planilha contém o código do local de votação, mas não endereço, latitude ou longitude. Portanto, não é possível localizar as seções com precisão usando somente esta base. As áreas do mapa são limites municipais oficiais simplificados do IBGE. Não são localizações individuais de eleitores. A busca por um código de seção também considera seções agregadas, quando informadas.

Seções agregadas têm seus votos contabilizados no boletim da seção principal. Não é possível separar esses votos na base. Um código de local de votação só identifica corretamente um local em conjunto com município e zona.

Os percentuais do ranking usam os votos da seleção como denominador. A cobertura usa o número de seções da seleção. Os votos mínimos e máximos filtram os **votos por seção**, não o total de um município. Valores vazios não impõem limite. Filtros incompatíveis mostram seleção vazia; não substituem dados ausentes por votos inventados.

## Fontes e conferência

- Votação: planilha `antonio_pedro_55456_acre.xlsx`, produzida a partir dos boletins oficiais do TSE, eleição 6259, deputado estadual, Acre.
- [Total oficial estadual do TSE](https://resultados.tse.jus.br/oficial/ele2026/6259/dados/ac/ac-c0007-e006259-u.json).
- [Geometria municipal do IBGE](https://servicodados.ibge.gov.br/api/v3/malhas/estados/12?formato=application/vnd.geo+json&qualidade=minima&intrarregiao=municipio), API de malhas versão 3, qualidade mínima.
- [Cadastro de municípios do IBGE](https://servicodados.ibge.gov.br/api/v1/localidades/estados/12/municipios).

O processo de extração original comparou as somas nominais dos 222 candidatos aos totais oficiais estadual e dos 22 municípios. O painel lê os registros da aba **Todas as seções** do Excel; o gerador verifica novamente o número de registros, a unicidade das seções, as 1.332 seções com votos e o total de 5.118. Os 22 municípios são associados à geometria do IBGE por nome normalizado e código oficial, sem atribuir coordenadas fictícias.

Este é um painel independente, não um site oficial do TSE. Os dados não são atualizados automaticamente. O mapa pode usar uma malha administrativa de período diferente do ano da votação, conforme a versão disponibilizada pela API do IBGE; essa geometria serve à visualização municipal e não modifica os resultados eleitorais.

## Alterar o painel

Os arquivos legíveis de interface e comportamento estão em `src/index.html`, `src/styles.css` e `src/app.js`. O arquivo publicado é o `index.html` da raiz, já compilado com todos os dados.

`build.py` é o gerador usado neste workspace. Ele depende das fontes de Excel e IBGE indicadas no código e de Python 3, usando somente a biblioteca padrão. Não precisa ser executado para publicar ou abrir a aplicação. Para mudanças rápidas, também é possível editar diretamente o `index.html` da raiz.

Código do painel sob licença MIT; os dados eleitorais e geográficos mantêm suas respectivas fontes e condições de uso.
