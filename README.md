# Banco de dados para Semântica e Pragmática da Atração de Caso em Grego Antigo

[![Production](https://github.com/caiogeraldes/doc_data/actions/workflows/production-tests.yml/badge.svg)](https://github.com/caiogeraldes/doc_data/actions/workflows/production-tests.yml)
[![Dev](https://github.com/caiogeraldes/doc_data/actions/workflows/dev-tests.yml/badge.svg)](https://github.com/caiogeraldes/doc_data/actions/workflows/dev-tests.yml)

**Autor:** Caio Borges Aguida Geraldes

Este pacote contém os scripts utilizados para a preparação, coleta e agregação dos dados a serem utilizados na pesquisa de doutorado "Semântica e Pragmática da Atração de Caso em Grego Antigo", realizada no PPG - Letras Clássicas (DLCV - FFLCH - USP), financiado pela FAPESP, nº2021/06027-4.


## Descrição da pipeline

### Preparação do ambiente

Instalar:
- `python`, `pip`, `poetry`, `MongoDB`

Baixar:
- [Diorisis](https://figshare.com/articles/dataset/The_Diorisis_Ancient_Greek_Corpus_JSON_/12251468) ([Vatri, A. and McGillivray, B. 2020](https://brill.com/view/journals/jgl/20/2/article-p179_4.xml))

Criar:
- arquivo de texto `.env` na raiz do projeto com a estrutura:

```bash
DIORISIS_PATH = "/path/to/diorisis-resources/json/"
PROC_DATA_PATH = "/path/to/output/data/"
MONGO="mongodb://000.0.0.0:00000/" # Connection to a MongoDB database
```

- Recomendo separar os textos de interesse da pasta principal de `diorisis-resources/json` para uma subpasta.


### Pré-processamento dos dados

Conversão do banco de dados em `DIORISIS_PATH` em um documento `stanza` (`src/doc_data/processor.py`) serializado salvo em `PROC_DATA_PATH`.

1. Extração das formas dos tokens.
2. Conversão de betacode para unicode e normalização (com apoio do pacote `cltk`).
3. Processamento de língua natural utilizando o pacote `stanza` (dados do `perseus`).
4. Serialização em `.pickle`.

### Criação de banco de dados

Para garantir que os dados sejam recuperáveis da maneira mais eficiente o possível, utiliza-se um banco de dados `MongoDB` estruturado da seguinte maneira:

- PhD (database)
    - [x] tokens (collection): coleção de tokens de todos os autores e textos selecionados (`write_pickle_to_mongo` de `./src/doc_data/db.py`). Exemplo de documento:
        ```json
        {
            "_id": "ecc5b9e54146a5af697d578436a32ff6",
            "id": 1,
            "text": "οὐ",
            "lemma": "οὐ",
            "upos": "ADV",
            "xpos": "d--------",
            "head": 3,
            "deprel": "advmod",
            "start_char": 0,
            "end_char": 2,
            "doc_name": "On The Refusal Of A Pension (024)",
            "author": "Lysias (0540)",
            "text_id": "44a283f7e6436806f453929b39fcb8b6",
            "sent_id": 1,
            "ts": "1941f2bec3a79dd3c18b4674d5a3bf8d",
            "tsi": "25850a5d4f9cd86d33a353ee598789b2",
            "tsh": "ed14403c056f3082c38834c86fef7ea9"
        }
        ```
        As entradas adicionais em relação ao resultado da pipeline de NLP são:
        1. `doc_name`: armazena o nome do texto com sua numeração;
        2. `author`: armazena o nome do autor com sua numeração;
        3. `text_id`: identificação única gerada a partir do autor e nome do texto, hasheado com `hashlib.md5`
        4. `sent_id`: armazena o índice da sentença em um dado documento;
        5. `ts`: identificação única da sentença a partir do autor, texto e `sent_id`, hasheada com `hashlib.md5`
        6. `tsi`: identificação do token a partir do nome do autor, texto, índice da sentença e do token em um id hasheado com `hashlib.md5`;
        7. `tsh`: identificação do token a partir do nome do autor, texto, índice da sentença e do head em um id hasheado com `hashlib.md5`;
        8. `_id`: identificação única do token a partir de `tsi` e `tsh`, hasheado com `hashlib.md5`

### Coleta de amostras

- [ ] As amostras são coletadas por meio de uma Pipeline de queries e agregações definidas em `./src/doc_data/query.py`. Sendo assim, elas são específicas para este trabalho.
    - [x] Seleção de sentenças contendo os verbos de `data/mvi.csv`. Resultado salvo em duas collections: `mviquery` e `mviquery:hits`
    - [x] Filtragem de sentenças contendo infinitivo subordinado ao verbo principal;
    - [x] Filtragem de sentenças contendo dativo ou genitivo subordinado ao verbo principal (caso a partir de `mvi`).
    - [ ] Filtragem de sentenças contendo predicado secundário subordinado ou ao VP ou ao Inf.
    - [ ] Revisão manual dos dados.
    - [ ] Reformulação da pipeline se necessário.
- [ ] Uma vez coletadas, as amostras serão salvas em uma coleção no database `phd`, usando a estrutura:
    ```json
    {}
    ```
