import requests
import shutil
import csv
import os

def writeToFile(directory, filename, filecontent):
    if directory:
        try: os.mkdir(directory)
        except: pass
    else:
        directory = ""

    with open(os.path.join(directory, filename), 'wb') as f:
        filecontent.raw.decode_content = True
        shutil.copyfileobj(filecontent.raw, f)

directory = "data"

instituicoesURL = "https://sisu-api.apps.mec.gov.br/api/v1/oferta/instituicoes"
response = requests.get(instituicoesURL).json()
instituicoes = [r["co_ies"] for r in response]

baseURL = "https://sisu.mec.gov.br/static/listagem-alunos-aprovados-portal/"
baseFilename = "listagem-alunos-aprovados-ies-{}-{}.csv"
for i, instituicao in enumerate(instituicoes):
        termoAdesaoURL = "https://sisu-api.apps.mec.gov.br/api/v1/oferta/instituicao/{}".format(instituicao)
        response = requests.get(termoAdesaoURL).json()

        termoAdesao = response["0"]["co_termo_adesao"]

        filename = baseFilename.format(instituicao, termoAdesao)
        url = baseURL + filename

        file = requests.get(url, stream=True)
        if file.status_code != 200:
            print("[{}/{}] [ERROR {}] {}".format(i+1, len(instituicoes), file.status_code, filename))
        else:
            writeToFile(directory, filename, file)
            print("[{}/{}] Saved to '{}'".format(i+1, len(instituicoes), filename))