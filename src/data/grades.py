import requests
import csv
import os
from time import sleep

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

# base_url = 'https://sisu-api.apps.mec.gov.br/api/v1/oferta/{}/modalidades' # 2020
base_url = 'https://sisu-api-pcr.apps.mec.gov.br/api/v1/oferta/{}/modalidades'

year = '2023'

output_path = os.path.join('..', '..', 'data', year, 'scraping')
try: os.makedirs(output_path)
except: pass

all_courses_csv = os.path.abspath(os.path.join(output_path, 'all_courses.csv'))
output_csv = os.path.abspath(os.path.join(output_path, 'grades.csv'))

errors = []

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
            break
        except:
            print('[{}] An exception occured, retrying...'.format(codigo))
            sleep(1)

    if response.status_code != 200:
        print('[{}] Error {}'.format(codigo, response.status_code))
        errors.append((codigo, response.status_code))
        continue

    response = response.json()

    pes_nat = response['oferta']['nu_peso_cn']
    pes_hum = response['oferta']['nu_peso_ch']
    pes_lin = response['oferta']['nu_peso_l']
    pes_mat = response['oferta']['nu_peso_m']
    pes_red = response['oferta']['nu_peso_r']

    min_nat = response['oferta']['nu_nmin_cn']
    min_hum = response['oferta']['nu_nmin_ch']
    min_lin = response['oferta']['nu_nmin_l']
    min_mat = response['oferta']['nu_nmin_m']
    min_red = response['oferta']['nu_nmin_r']
    min_tot = response['oferta']['nu_media_minima']

    modalidades = [{campo: m[campo] for campo in ['no_concorrencia', 'qt_vagas', 'nu_nota_corte', 'qt_bonus_perc', 'dt_nota_corte']} for m in response['modalidades']]

    print(f'[{i+1:>4}/{len(ofertas)}] [{codigo}] {ies_nome} ({ies_sg}) - {curso_nome} - {curso_turno}')

    csv_line = [codigo, curso_nome, curso_grau, curso_turno, vagas_totais,
               campus_nome, campus_cidade, campus_uf, ies_nome, ies_sg,
               pes_nat, pes_hum, pes_lin, pes_mat, pes_red,
               min_nat, min_hum, min_lin, min_mat, min_red, min_tot]

    for m in modalidades:
        if int(m['qt_vagas']) > 0: # Remove categories with no available vacancies
            csv_line += list(m.values())
    
    csv_lines.append(csv_line)

with open(output_csv, 'w+', encoding='UTF-8') as f:
    csv_file_writer = csv.writer(f,  delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')
    for csv_line in csv_lines:
        csv_file_writer.writerow(tuple(csv_line))

print('Finished.')

if errors:
    print('Errors:')
    for e in errors:
        print('\t{} - Error {}'.format(e[0], e[1]))