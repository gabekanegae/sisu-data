# Dados SiSU

Este repositório agrupa os dados de notas de corte e lista de aprovados do [Sistema de Seleção Unificada (SiSU)](https://sisu.mec.gov.br/).

Estão disponíveis dados completos dos anos de [2020](data/2020), [2021](data/2021), [2022](data/2022), [2023](data/2023), [2024](data/2024) e [2025](data/2025), assim como [informações gerais dos anos 2010-2025](data/relatorios).

* `src/data/`: Scripts em Python que coletam dados disponibilizados em APIs não documentadas do SiSU.
* `src/reports/`: Scripts em Python que geram arquivos para leitura humana.
* `data/*/listagem_alunos_aprovados_csv/`: Arquivos `.csv` disponibilizados diretamente pelo SiSU.
* `data/*/scraping/`: Arquivos `.csv` coletados pelos scripts em `src/data`.
* `data/relatorios/`: Arquivos `.xlsx` disponibilizados diretamente pelo SiSU.
* `reports/*/`: Arquivos `.txt` formatados para leitura humana pelos scripts em `src/reports`.

 e estiveram disponíveis nos endereços http://sisualuno.mec.gov.br/, https://sisu.mec.gov.br/#/selecionados e https://sisu.mec.gov.br/#/relatorio

Todos os dados neste repositório são públicos. Embora coletados destas fontes oficiais, os dados aqui presentes não possuem caráter oficial, e devem ser usados apenas para consulta, estudo e pesquisa.