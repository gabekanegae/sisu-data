# Dados SiSU 2021

## Arquivos .csv

**[Lista de Cursos](https://raw.githubusercontent.com/KanegaeGabriel/sisu-2021-data/main/all_courses.csv)**

**Final: [16/04](https://raw.githubusercontent.com/KanegaeGabriel/sisu-2021-data/main/data/grades.csv) | [Lista de Aprovados](https://raw.githubusercontent.com/KanegaeGabriel/sisu-2021-data/main/data/names.csv)**

**[Arquivos "baixar lista de selecionados da instituição"](get_csv)**

## Arquivos .txt

**Final: [16/04](https://raw.githubusercontent.com/KanegaeGabriel/sisu-2021-data/main/data/grades.txt) | [Lista de Aprovados](https://raw.githubusercontent.com/KanegaeGabriel/sisu-2021-data/main/data/names.txt) | [Ranking Geral de Aprovados](https://raw.githubusercontent.com/KanegaeGabriel/sisu-2021-data/main/data/names_ranking.txt)**

## Observações

Os arquivos .csv foram gerados pelos scripts [all_list_courses.py](/all_list_courses.py), [grades_request_data.py](/grades_request_data.py) e [names_request_data.py](/names_request_data.py), e a partir deles, foram gerados os .txt por [grades_parse_csv.py](/grades_parse_csv.py), [names_parse_csv.py](/names_parse_csv.py) e [names_generate_rank.py](names_generate_rank.py) a título de exemplo de uso.

Os arquivos finais contêm 5571 cursos oferecidos pelo SiSU. Os arquivos com os alunos aprovados listam um total de 198957 nomes dentre todos os 5571 cursos.

Todos os dados neste repositório são públicos e estiveram disponíveis nos endereços [http://sisualuno.mec.gov.br/](http://sisualuno.mec.gov.br/) e [https://sisu.mec.gov.br/#/selecionados](https://sisu.mec.gov.br/#/selecionados). Embora coletados destas fontes oficiais, os dados aqui presentes não possuem caráter oficial, e devem ser usados apenas para consulta, estudo e pesquisa.