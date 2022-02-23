import csv
import sys
import os
from time import time

class Curso:
    def __init__(self, info, alunos):
        self.campus_uf, self.ies_nome, self.ies_sg, self.campus_cidade = info[:4]
        self.campus_nome, self.curso_nome, self.curso_grau, self.curso_turno, self.vagas_totais = info[4:]
        self.alunos = [Aluno(alunos[i:i+6], self) for i in range(0, len(alunos), 6)]

    def __str__(self):
        return f'{self.ies_nome} ({self.ies_sg}) - {self.curso_nome} - {self.campus_cidade}, {self.campus_uf}'

class Aluno:
    def __init__(self, m, curso):
        self.codigo, self.nome, self.posicao, self.nota, self.mod_nome, self.bonus = m
        self.curso = curso
        self.nota = float(self.nota) / (1 + float(self.bonus)/100) # Remove any bonus they might have

    def __str__(self):
        return '{:>6.2f} - {} - {} (#{})'.format(self.nota, self.nome, self.curso, self.posicao)

if len(sys.argv) == 1:
    print(f'Usage: py {sys.argv[0]} (year)')
    exit()

year = sys.argv[1]

all_courses_csv = os.path.abspath(os.path.join('..', '..', 'data', year, 'scraping', 'all_courses.csv'))
names_csv = os.path.abspath(os.path.join('..', '..', 'data', year, 'scraping', 'names.csv'))
output_txt = os.path.abspath(os.path.join('..', '..', 'reports', year, 'names_ranking.txt'))

##################################################

# Get all course info from .csv file
try:
    print(f'Reading file \'{all_courses_csv}\'...')
    with open(all_courses_csv, mode='r', encoding='UTF-8') as f:
        csv_file_reader = csv.reader(f, delimiter=';')
        cursos_info = {oferta[-1]: oferta[:-1] for oferta in map(tuple, csv_file_reader)}
except FileNotFoundError:
    print(f'File \'{all_courses_csv}\' not found.')
    exit()

# Read csv and process strings (via class constructors)
print(f'Reading file \'{names_csv}\'...')
try:
    with open(names_csv, mode='r', encoding='UTF-8') as f:
        csv_file_reader = csv.reader(f, delimiter=';')
        cursos = [Curso(cursos_info[c[0]], c[1:]) for c in csv_file_reader]
except FileNotFoundError:
    print(f'File \'{names_csv}\' not found.')
    exit()

alunos = []
for c in cursos:
    alunos += c.alunos

alunos.sort(key=lambda x: (x.nota), reverse=True)

# Write to .txt
print(f'Writing to \'{output_txt}\'...')
with open(output_txt, 'w+', encoding='UTF-8') as f:
    for i, aluno in enumerate(alunos):
        pct = (1-(i+1)/len(alunos))*100
        f.write("{:>6}: {:>7.3f}% - {}\n".format(i+1, pct, aluno))

print(f'Finished.')