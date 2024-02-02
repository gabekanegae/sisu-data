import requests
import csv
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

# base_url = 'https://sisu-api.apps.mec.gov.br/api/v1/oferta/' # 2020
# base_url = 'https://sisu-api-pcr.apps.mec.gov.br/api/v1/oferta/' # 2021, 2022, 2023
base_url = 'https://sisu-api.sisu.mec.gov.br/api/v1/oferta/' # 2024

year = '2024'

output_path = os.path.join('..', '..', 'data', year, 'scraping')
try: os.makedirs(output_path)
except: pass

output_csv = os.path.abspath(os.path.join(output_path, 'all_courses.csv'))

print(f'Will write to file \'{output_csv}\'.')

instituicoes_url = base_url + 'instituicoes'
response = requests.get(instituicoes_url, headers=headers).json()
instituicoes = [r['co_ies'] for r in response]

ofertas = []
for i, instituicao in enumerate(instituicoes):
    print('[{:>3}/{}] Scanning ID #{}...'.format(i+1, len(instituicoes), instituicao))

    instituicao_url = base_url + 'instituicao' + '/' + instituicao
    response = requests.get(instituicao_url, headers=headers).json()

    for i in range(len(response)-1):
        r = response[str(i)]

        codigo = r['co_oferta']
        curso_nome = r['no_curso']
        curso_grau = r['no_grau']
        curso_turno = r['no_turno']
        vagas_totais = str(int(r['qt_vagas_sem1']) + int(r['qt_vagas_sem2']))

        campus_nome = r['no_campus']
        campus_cidade = r['no_municipio_campus']
        campus_uf = r['sg_uf_campus']
        ies_nome = r['no_ies']
        ies_sg = r['sg_ies']

        oferta = (campus_uf, ies_nome, ies_sg, campus_cidade, campus_nome, curso_nome, curso_grau, curso_turno, vagas_totais, codigo)
        ofertas.append(oferta)

ofertas.sort()

print(f'Writing to file \'{output_csv}\'...')
with open(output_csv, 'w+', encoding='UTF-8') as f:
    csv_file_writer = csv.writer(f,  delimiter=';', quotechar='"', quoting=csv.QUOTE_ALL, lineterminator='\n')

    for oferta in ofertas:
        csv_file_writer.writerow(tuple(oferta))

print('Finished.')