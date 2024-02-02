import requests
import csv
import os
from time import sleep

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

# base_url = 'https://sisu-api.apps.mec.gov.br/api/v1/oferta/{}/selecionados' # 2020
# base_url = 'https://sisu-api-pcr.apps.mec.gov.br/api/v1/oferta/{}/selecionados' # 2021, 2022, 2023
base_url = 'https://sisu-api.sisu.mec.gov.br/api/v1/oferta/{}/selecionados' # 2024

year = '2024'

output_path = os.path.join('..', '..', 'data', year, 'scraping')
try: os.makedirs(output_path)
except: pass

all_courses_csv = os.path.abspath(os.path.join(output_path, 'all_courses.csv'))
output_csv = os.path.abspath(os.path.join(output_path, 'names.csv'))

##################################################

# Get all course info from .csv file
try:
    print(f'Reading file \'{all_courses_csv}\'...')
    with open(all_courses_csv, mode='r', encoding='UTF-8') as f:
        csv_file_reader = csv.reader(f, delimiter=';')
        ofertas = list(map(tuple, csv_file_reader))
except FileNotFoundError:
    print(f'File \'{all_courses_csv}\' not found.')
    exit()

print(f'Will write to file \'{output_csv}\'.')

print('Requesting {} courses...'.format(len(ofertas)))

csv_lines = []

for i, oferta in enumerate(ofertas):
    campus_uf, ies_nome, ies_sg, campus_cidade, campus_nome, curso_nome, curso_grau, curso_turno, vagas_totais, codigo = oferta

    while True:
        try:
            response = requests.get(base_url.format(codigo), headers=headers)
            if response.status_code != 200:
                print(f'   Status code: {response.status_code}')
                raise Exception
            break
        except:
            print('[{}] An exception occured, retrying...'.format(codigo))
            sleep(1)

    if response.status_code != 200:
        print('[{}] Error {}'.format(codigo, response.status_code))
        errors.append((codigo, response.status_code))
        continue

    response = response.json()

    csv_line = [codigo]
    for r in response:
        codigo_aluno = r['co_inscricao_enem']
        nome = r['no_inscrito']
        classificacao = r['nu_classificacao']
        nota = r['nu_nota_candidato']
        modalidade = r['no_mod_concorrencia']
        bonus = r['qt_bonus_perc']

        csv_line += [codigo_aluno, nome, classificacao, nota, modalidade, bonus]

    print(f'[{i+1:>4}/{len(ofertas)}] [{codigo}] {ies_nome} ({ies_sg}) - {curso_nome} - {curso_turno}')

    csv_lines.append(csv_line)

with open(output_csv, 'w+', encoding='UTF-8') as f:
    csv_file_writer = csv.writer(f,  delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')
    for csv_line in csv_lines:
        csv_file_writer.writerow(tuple(csv_line))

print('Finished.')