import csv
import os
from time import time

class Curso:
    def __init__(self, info, alunos):
        self.campusUF, self.iesNome, self.iesSG, self.campusCidade = info[:4]
        self.campusNome, self.cursoNome, self.cursoGrau, self.cursoTurno, self.vagasTotais = info[4:]
        self.alunos = [Aluno(alunos[i:i+6], self) for i in range(0, len(alunos), 6)]

    def __str__(self):
        return "{} ({}) - {} - {}, {}".format(self.iesNome, self.iesSG, self.cursoNome, self.campusCidade, self.campusUF)

class Aluno:
    def __init__(self, m, curso):
        self.codigo, self.nome, self.posicao, self.nota, self.modNome, self.bonus = m
        self.curso = curso
        self.nota = float(self.nota) / (1 + float(self.bonus)/100) # Remove any bonus they might have

    def __str__(self):
        return "{:>6.2f} - {} - {} (#{})".format(self.nota, self.nome, self.curso, self.posicao)

t0 = time()

directory = "data"
filename = input("Filename (without extension): /{}/".format(directory)).strip()

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

alunos = []
for c in cursos:
    alunos += c.alunos

alunos = sorted(alunos, key=lambda x: (x.nota), reverse=True)

# Write to .txt
with open(os.path.join(directory, filename + "_ranking" + ".txt"), "w+", encoding="UTF-8") as humanFile:
    for i, aluno in enumerate(alunos):
        pct = (1-(i+1)/len(alunos))*100
        humanFile.write("{:>6}: {:>7.3f}% - {}\n".format(i+1, pct, aluno))

print("Written {} students to '{}_ranking.txt' in {:.1f}s.".format(len(alunos), directory+"/"+filename, time()-t0))