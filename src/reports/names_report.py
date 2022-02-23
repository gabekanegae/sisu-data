import csv
import sys
import os

with open('short_category_names.txt', encoding='UTF-8') as f:
    raw_short_category_names = [l.strip().split(' | ') for l in f.readlines()]
    short_category_names = {k.lower(): v for v, k in raw_short_category_names}
    
    assert(len(raw_short_category_names) == len(short_category_names))

class Aluno:
    def __init__(self, m):
        self.codigo, self.nome, self.posicao, self.nota, self.mod_nome, self.bonus = m

        # Reduce category names based on the short_category_names dict
        key = self.mod_nome.lower()
        if key in short_category_names:
            self.mod_nome = short_category_names[key]

    def __str__(self):
        s = [
             f'\t{self.mod_nome}:',
             '\t\t{:>3}: {:>6} - {}'.format(self.posicao, self.nota, self.nome)
            ]

        return '\n'.join(s)

class Curso:
    def __init__(self, info, alunos):
        self.campus_uf, self.ies_nome, self.ies_sg, self.campus_cidade = info[:4]
        self.campus_nome, self.curso_nome, self.curso_grau, self.curso_turno, self.vagas_totais = info[4:]
        self.alunos = [Aluno(alunos[i:i+6]) for i in range(0, len(alunos), 6)]

    def __str__(self):
        s = [
             f'{self.ies_nome} ({self.ies_sg}) - {self.campus_nome}, {self.campus_cidade}, {self.campus_uf}',
             f'{self.curso_nome.strip()}, {self.curso_grau}, {self.curso_turno}'
            ]

        alunos = [str(m) for m in self.alunos]

        # Only print modality name if it's the first occurence
        last = alunos[0].split('\n')[0]
        for i in range(1, len(alunos)):
            if alunos[i].split('\n')[0] == last:
                alunos[i] = alunos[i].split('\n')[1]
            else:
                last = alunos[i].split('\n')[0]

        return '\n'.join(s + alunos)

if len(sys.argv) == 1:
    print(f'Usage: py {sys.argv[0]} (year)')
    exit()

year = sys.argv[1]

all_courses_csv = os.path.abspath(os.path.join('..', '..', 'data', year, 'scraping', 'all_courses.csv'))
names_csv = os.path.abspath(os.path.join('..', '..', 'data', year, 'scraping', 'names.csv'))
output_txt = os.path.abspath(os.path.join('..', '..', 'reports', year, 'names.txt'))

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

# Sort lexicographically
cursos.sort(key=lambda x: (x.campus_uf, x.ies_nome, x.ies_sg, x.campus_cidade, x.campus_nome, x.curso_nome))

# Write to .txt
print(f'Writing to \'{output_txt}\'...')
with open(output_txt, 'w+', encoding='UTF-8') as f:
    for i, curso in enumerate(cursos):
        nl = str(curso).index('\n')

        # Only write ies_nome if it's the first occurence
        if i == 0 or (str(curso)[:nl] != str(cursos[i-1]).split('\n')[0]):
            f.write('='*50 + '\n')
            f.write(str(curso)[:nl] + '\n')
            f.write('='*50 + '\n')
        f.write(str(curso)[nl+1:] + '\n')
        f.write('\n')

print(f'Finished.')