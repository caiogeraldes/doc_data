# Banco de dados para Semântica e Pragmática da Atração de Caso em Grego Antigo

**Autor:** Caio Borges Aguida Geraldes

Este pacote contém os scripts utilizados para a preparação, coleta e agregação dos dados a serem utilizados na pesquisa de doutorado "Semântica e Pragmática da Atração de Caso em Grego Antigo", realizada no PPG - Letras Clássicas (DLCV - FFLCH - USP), financiado pela FAPESP, nº2021/06027-4.


## Descrição da pipeline

### Preparação do ambiente

Instalar:
- `python`, `pip`, `poetry`, `MongoDB`

Baixar:
- [Diorisis](https://www.crs.rm.it/diorisissearch/) ([Vatri, A. and McGillivray, B. 2020](https://brill.com/view/journals/jgl/20/2/article-p179_4.xml))

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
            "_id": "8c2976b6df70db489068dd3d67eb0b79",
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
            "sid_id": [1, 1],
            "sid_hid": [1, 3]
        }
        ```
        As entradas adicionais em relação ao resultado da pipeline de NLP são:
        1. `doc_name`: armazena o nome do texto com sua numeração;
        2. `author`: armazena o nome do autor com sua numeração;
        3. `text_id`: identificação única gerada a partir do autor e nome do texto, hasheado com `hashlib.md5`
        4. `sent_id`: armazena o índice da sentença em um dado documento;
        5. `sid_id`: armazena o índice da sentença e do token em uma tupla;
        6. `sid_hid`: armazena o índice da sentença e do token analisado como `head`.
        7. `_id`: identificação única gerada a partir do autor, nome do texto e `sid_id`, hasheado com `hashlib.md5`
    - [ ] mvi (collection): coleção de verbos principais de interesse com características centrais (lemma, valência, regência, semântica)

### Coleta de amostras

- [ ] As amostras são coletadas por meio de uma Pipeline de queries e agregações definidas em `./src/doc_data/searchpipeline.py`. Sendo assim, elas são específicas para este trabalho.
    - [ ] Separação por textos.
    - [ ] Seleção de sentenças contendo os verbos de `mvi`.
    - [ ] Filtragem de sentenças contendo infinitivo subordinado ao verbo principal;
    - [ ] Filtragem de sentenças contendo dativo ou genitivo subordinado ao verbo principal (caso a partir de `mvi`).
    - [ ] Filtragem de sentenças contendo predicado secundário subordinado ou ao VP ou ao Inf.
    - [ ] Revisão manual dos dados.
    - [ ] Reformulação da pipeline se necessário.
- [ ] Uma vez coletadas, as amostras serão salvas em uma coleção no database `phd`, usando a estrutura:
    ```json
    {}
    ```
