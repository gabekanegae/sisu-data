import requests
import csv
from time import time

baseURL = "https://sisu-api.apps.mec.gov.br/api/v1/oferta/"

filename = "all_courses"

t0 = time()

print("Will write to file '{}.csv'.".format(filename))

csvFile = open(filename + ".csv", "w+", encoding="UTF-8")
csvFileWriter = csv.writer(csvFile,  delimiter=";", quotechar="\"", quoting=csv.QUOTE_ALL, lineterminator="\n")

response = requests.get(baseURL+"instituicoes").json()
instituicoes = [r["co_ies"] for r in response]

ofertas = []
for i, instituicao in enumerate(instituicoes):
    print("[{:>3}/{}] Scanning ID #{}...".format(i+1, len(instituicoes), instituicao))

    response = requests.get(baseURL+"instituicao/"+instituicao).json()
    for i in range(len(response)-1):
        r = response[str(i)]

        codigo = r["co_oferta"]
        cursoNome = r["no_curso"]
        cursoGrau = r["no_grau"]
        cursoTurno = r["no_turno"]
        vagasTotais = r["qt_vagas_sem1"]

        campusNome = r["no_campus"]
        campusCidade = r["no_municipio_campus"]
        campusUF = r["sg_uf_campus"]
        iesNome = r["no_ies"]
        iesSG = r["sg_ies"]

        oferta = (campusUF, iesNome, iesSG, campusCidade, campusNome, cursoNome, cursoGrau, cursoTurno, vagasTotais, codigo)
        ofertas.append(oferta)

ofertas = sorted(ofertas)

# Write to .csv
for oferta in ofertas:
    csvFileWriter.writerow(tuple(oferta))

print("Written {} courses to '{}.csv' in {:.1f}s.".format(len(ofertas), filename, time()-t0))