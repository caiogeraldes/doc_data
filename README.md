# Banco de dados para Semântica e Pragmática da Atração de Caso em Grego Antigo

**Autor:** Caio Borges Aguida Geraldes

Este pacote contém os scripts utilizados para a preparação, coleta e agregação dos dados a serem utilizados na pesquisa de doutorado "Semântica e Pragmática da Atração de Caso em Grego Antigo", realizada no PPG - Letras Clássicas (DLCV - FFLCH - USP).


## Descrição da pipeline

### Preparação dos dados

1. Conversão do banco de dados [Diorisis](https://www.crs.rm.it/diorisissearch/) (Vatri, A. and McGillivray, B. 2020) em um documento `stanza` (`src/doc_data/processor.py`).
    1. Extração das formas dos tokens.
    2. Conversão de betacode para unicode e normalização (com apoio do pacote `cltk`).
