# Banco de dados para Semântica e Pragmática da Atração de Caso em Grego Antigo

**Autor:** Caio Borges Aguida Geraldes

Este pacote contém os scripts utilizados para a preparação, coleta e agregação dos dados a serem utilizados na pesquisa de doutorado "Semântica e Pragmática da Atração de Caso em Grego Antigo", realizada no PPG - Letras Clássicas (DLCV - FFLCH - USP), financiado pela FAPESP, nº2021/06027-4.


## Descrição da pipeline

### Preparação do ambiente

Instalar:
- `python`, `pip`, `poetry`, `MongoDB`

Baixar:
- [Diorisis](https://www.crs.rm.it/diorisissearch/) (Vatri, A. and McGillivray, B. 2020)

Criar:
- arquivo de texto `.env` na raiz do projeto com a estrutura:

```{bash}
DIORISIS_PATH = "/path/to/diorisis-resources/json/"
PROC_DATA_PATH = "/path/to/output//data/"
MONGO="mongodb://000.0.0.0:00000/" # Connection to a MongoDB database
```


### Preparação dos dados

1. Conversão do banco de dados  em um documento `stanza` (`src/doc_data/processor.py`). 
    1. Extração das formas dos tokens.
    2. Conversão de betacode para unicode e normalização (com apoio do pacote `cltk`).
    3. Análise
