import csv
import os
from datetime import datetime
from time import time

with open('short_category_names.txt', encoding='UTF-8') as f:
    raw_short_category_names = [l.strip().split(' | ') for l in f.readlines()]
    modNomeReduzido = {k.lower(): v for v, k in raw_short_category_names}
    
    assert(len(raw_short_category_names) == len(modNomeReduzido))

class Modalidade:
    def __init__(self, m):
        self.modNome, self.vagas, self.nota, self.bonus, self.dataNota = m

        # Reduces modality names based on the modNomeReduzido dict
        modNomeKey = self.modNome.lower()
        if modNomeKey in modNomeReduzido:
            self.modNome = modNomeReduzido[modNomeKey]

    def __str__(self):
        s = [
             "\t{}{}:".format(self.modNome, " (+{}%)".format(self.bonus) if self.bonus and self.bonus != ".00" else ""),
             "\t\tVagas: {} | Nota de Corte: {}".format(self.vagas, self.nota)
            ]

        return "\n".join(s)

class Curso:
    def __init__(self, l):
        self.codigo, self.cursoNome, self.cursoGrau, self.cursoTurno, self.vagasTotais = l[:5]
        self.campusNome, self.campusCidade, self.campusUF, self.iesNome, self.iesSG = l[5:10]
        self.pesNAT, self.pesHUM, self.pesLIN, self.pesMAT, self.pesRED = l[10:15]
        self.minNAT, self.minHUM, self.minLIN, self.minMAT, self.minRED, self.minTOT = l[15:21]

        self.modalidades = [Modalidade(l[i:i+5]) for i in range(21, len(l), 5)]

    def __str__(self):
        s = [
             "{} ({}) - {}, {}, {}".format(self.iesNome, self.iesSG, self.campusNome, self.campusCidade, self.campusUF),
             "{}, {}, {}".format(self.cursoNome, self.cursoGrau, self.cursoTurno),
             "Total de Vagas: {}".format(self.vagasTotais),
             "Pesos: NAT={}, HUM={}, LIN={}, MAT={}, RED={} | Mínimo: NAT={}, HUM={}, LIN={}, MAT={}, RED={}, TOTAL={}".format(self.pesNAT, self.pesHUM, self.pesLIN, self.pesMAT, self.pesRED, self.minNAT, self.minHUM, self.minLIN, self.minMAT, self.minRED, self.minTOT)
            ]

        # Sort by grade needed
        self.modalidades = sorted(self.modalidades, key=lambda x: (x.nota, x.modNome), reverse=True)

        mods = [str(m) for m in self.modalidades]

        return "\n".join(s+mods)

directory = "data"
filename = input("Filename (without extension): /{}/".format(directory)).strip()

t0 = time()

##################################################

# Read csv and process strings (via class constructors)
try:
    with open(os.path.join(directory, filename + ".csv"), "r", encoding="UTF-8") as csvFile:
        csvFileReader = csv.reader(csvFile, delimiter=";")
        cursos = [Curso(l) for l in csvFileReader]
except FileNotFoundError:
    print("File /{}/{}.csv not found.".format(directory, filename))
    exit()

# Sort lexicographically
cursos = sorted(cursos, key=lambda x: (x.campusUF, x.iesNome, x.campusCidade, x.campusNome, x.cursoNome))

# Write to .txt
with open(os.path.join(directory, filename + ".txt"), "w+", encoding="UTF-8") as humanFile:
    for i, curso in enumerate(cursos):
        nl = str(curso).index("\n")

        # Only write iesNome if it's the first occurence
        if i == 0 or (str(curso)[:nl] != str(cursos[i-1]).split("\n")[0]):
            humanFile.write("="*50 + "\n")
            humanFile.write(str(curso)[:nl] + "\n")
            humanFile.write("="*50 + "\n")
        humanFile.write(str(curso)[nl+1:] + "\n")
        humanFile.write("\n")

print("Written {} courses to '{}.txt' in {:.1f}s.".format(len(cursos), directory+"/"+filename, time()-t0))