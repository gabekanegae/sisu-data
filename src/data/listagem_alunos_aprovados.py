import requests
import shutil
import csv
import os

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}

def write_to_file(directory, filename, filecontent):
    if directory:
        try: os.mkdir(directory)
        except: pass
    else:
        directory = ''

    with open(os.path.join(directory, filename), 'wb') as f:
        filecontent.raw.decode_content = True
        shutil.copyfileobj(filecontent.raw, f)

year = '2022'
directory = os.path.abspath(os.path.join('..', '..', 'data', year, 'listagem_alunos_aprovados_csv'))

# instituicoes_url = 'https://sisu-api.apps.mec.gov.br/api/v1/oferta/instituicoes' # 2020
instituicoes_url = 'https://sisu-api-pcr.apps.mec.gov.br/api/v1/oferta/instituicoes'

response = requests.get(instituicoes_url, headers=headers).json()
instituicoes = [r['co_ies'] for r in response]

base_url = 'https://sisu.mec.gov.br/static/listagem-alunos-aprovados-portal/'
base_filename = 'listagem-alunos-aprovados-ies-{}-{}.csv'
for i, instituicao in enumerate(instituicoes):
        termo_adesao_url = 'https://sisu-api-pcr.apps.mec.gov.br/api/v1/oferta/instituicao/{}'.format(instituicao)
        response = requests.get(termo_adesao_url, headers=headers).json()

        termo_adesao = response['0']['co_termo_adesao']

        filename = base_filename.format(instituicao, termo_adesao)

        url = base_url + filename
        file = requests.get(url, headers=headers, stream=True)
        if file.status_code != 200:
            print(f'[{i+1:>4}/{len(instituicoes)}] [ERROR {file.status_code}] {filename}')
        else:
            write_to_file(directory, filename, file)
            print(f'[{i+1:>4}/{len(instituicoes)}] Saved to \'{os.path.abspath(filename)}\'')