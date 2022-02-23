import requests
import csv
import os
from time import time, sleep

directory = "data"
filename = input("Filename (without extension): /{}/".format(directory)).strip()

baseURL = "https://sisu-api.apps.mec.gov.br/api/v1/oferta/{}/selecionados"

t0 = time()
errors = []

##################################################

# Read course list
try:
    with open("all_courses.csv", "r", encoding="UTF-8") as csvFile:
        csvFileReader = csv.reader(csvFile, delimiter=";")
        ofertas = [tuple(l) for l in csvFileReader]
except FileNotFoundError:
    print("File /all_courses.csv not found.")
    exit()

print("Will write to file '/{}/{}.csv'.".format(directory, filename))

csvFile = open(os.path.join(directory, filename + ".csv"), "w+", encoding="UTF-8")
csvFileWriter = csv.writer(csvFile,  delimiter=";", quotechar="\"", quoting=csv.QUOTE_ALL, lineterminator="\n")

print("Reading {} courses...".format(len(ofertas)))

for oferta in ofertas:
    campusUF, iesNome, iesSG, campusCidade, campusNome, cursoNome, cursoGrau, cursoTurno, vagasTotais, codigo = oferta

    while True:
        try:
            response = requests.get(baseURL.format(codigo))
            break
        except:
            print("[{}] An exception occured, retrying...".format(codigo))
            sleep(1)

    if response.status_code != 200:
        print("[{}] Error {}".format(codigo, response.status_code))
        errors.append((codigo, response.status_code))
        continue
    response = response.json()

    csvLine = [codigo]
    for r in response:
        codigo_aluno = r["co_inscricao_enem"]
        nome = r["no_inscrito"]
        classificacao = r["nu_classificacao"]
        nota = r["nu_nota_candidato"]
        modalidade = r["no_mod_concorrencia"]
        bonus = r["qt_bonus_perc"]

        csvLine += [codigo_aluno, nome, classificacao, nota, modalidade, bonus]

    print("[{}] {} ({}) - {}".format(codigo, iesNome, iesSG, cursoNome))

    # Write to .csv
    csvFileWriter.writerow(tuple(csvLine))

print("Parsed {} courses to '{}/{}.csv' in {:.1f}s with {} errors.".format(len(ofertas), directory, filename, time()-t0, len(errors)))
if errors:
    print("Errors:")
    for e in errors:
        print("\t{} - Error {}".format(e[0], e[1]))