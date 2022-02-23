import csv
import os
from datetime import datetime
from time import time

with open('short_category_names.txt', encoding='UTF-8') as f:
    raw_short_category_names = [l.strip().split(' | ') for l in f.readlines()]
    modNomeReduzido = {k.lower(): v for v, k in raw_short_category_names}
    
    assert(len(raw_short_category_names) == len(modNomeReduzido))

class Aluno:
    def __init__(self, m):
        self.codigo, self.nome, self.posicao, self.nota, self.modNome, self.bonus = m

        # Reduces modality names based on the modNomeReduzido dict
        modNomeKey = self.modNome.lower()
        if modNomeKey in modNomeReduzido:
            self.modNome = modNomeReduzido[modNomeKey]

    def __str__(self):
        s = [
             "\t{}:".format(self.modNome),
             "\t\t{:>3}: {:>6} - {}".format(self.posicao, self.nota, self.nome)
            ]

        return "\n".join(s)

class Curso:
    def __init__(self, info, alunos):
        self.campusUF, self.iesNome, self.iesSG, self.campusCidade = info[:4]
        self.campusNome, self.cursoNome, self.cursoGrau, self.cursoTurno, self.vagasTotais = info[4:]
        self.alunos = [Aluno(alunos[i:i+6]) for i in range(0, len(alunos), 6)]

    def __str__(self):
        s = [
             "{} ({}) - {}, {}, {}".format(self.iesNome, self.iesSG, self.campusNome, self.campusCidade, self.campusUF),
             "{}, {}, {}".format(self.cursoNome, self.cursoGrau, self.cursoTurno),
            ]

        alunos = [str(m) for m in self.alunos]

        # Only print modality name if it's the first occurence
        last = alunos[0].split("\n")[0]
        for i in range(1, len(alunos)):
            if alunos[i].split("\n")[0] == last:
                alunos[i] = alunos[i].split("\n")[1]
            else:
                last = alunos[i].split("\n")[0]

        return "\n".join(s+alunos)

directory = "data"
filename = input("Filename (without extension): /{}/".format(directory)).strip()

t0 = time()

##################################################

# Get all course info from .csv file
try:
    with open("all_courses.csv", "r", encoding="UTF-8") as csvFile:
        csvFileReader = csv.reader(csvFile, delimiter=";")
        cursosInfo = {oferta[-1]: oferta[:-1] for oferta in [tuple(l) for l in csvFileReader]}
except FileNotFoundError:
    print("File /all_courses.csv not found.")
    exit()

# Read csv and process strings (via class constructors)
try:
    with open(os.path.join(directory, filename + ".csv"), "r", encoding="UTF-8") as csvFile:
        csvFileReader = csv.reader(csvFile, delimiter=";")
        cursos = [Curso(cursosInfo[c[0]], c[1:]) for c in csvFileReader]
except FileNotFoundError:
    print("File /{}/{}.csv not found.".format(directory, filename))
    exit()

# Sort lexicographically
cursos = sorted(cursos, key=lambda x: (x.campusUF, x.iesNome, x.iesSG, x.campusCidade, x.campusNome, x.cursoNome))

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