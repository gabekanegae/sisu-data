import csv
import sys
import os

with open('short_category_names.txt', encoding='UTF-8') as f:
    raw_short_category_names = [l.strip().split(' | ') for l in f.readlines()]
    short_category_names = {k.lower(): v for v, k in raw_short_category_names}
    
    assert(len(raw_short_category_names) == len(short_category_names))

class Modalidade:
    def __init__(self, m):
        self.mod_nome, self.vagas, self.nota, self.bonus, self.dataNota = m

        # Reduce category names based on the short_category_names dict
        key = self.mod_nome.lower()
        if key in short_category_names:
            self.mod_nome = short_category_names[key]

    def __str__(self):
        s = [
             '\t{}{}:'.format(self.mod_nome, ' (+{}%)'.format(self.bonus) if self.bonus and self.bonus != '.00' else ''),
             f'\t\tVagas: {self.vagas} | Nota de Corte: {self.nota}'
            ]

        return '\n'.join(s)

class Curso:
    def __init__(self, l):
        self.codigo, self.curso_nome, self.curso_grau, self.curso_turno, self.vagas_totais = l[:5]
        self.campus_nome, self.campus_cidade, self.campus_uf, self.ies_nome, self.ies_sg = l[5:10]
        self.pes_nat, self.pes_hum, self.pes_lin, self.pes_mat, self.pes_red = l[10:15]
        self.min_nat, self.min_hum, self.min_lin, self.min_mat, self.min_red, self.min_tot = l[15:21]

        self.modalidades = [Modalidade(l[i:i+5]) for i in range(21, len(l), 5)]

    def __str__(self):
        s = [
             '{} ({}) - {}, {}, {}'.format(self.ies_nome, self.ies_sg, self.campus_nome, self.campus_cidade, self.campus_uf),
             f'{self.curso_nome}, {self.curso_grau}, {self.curso_turno}',
             f'Total de Vagas: {self.vagas_totais}',
             f'Pesos: NAT={self.pes_nat}, HUM={self.pes_hum}, LIN={self.pes_lin}, MAT={self.pes_mat}, RED={self.pes_red} | Mínimo: NAT={self.min_nat}, HUM={self.min_hum}, LIN={self.min_lin}, MAT={self.min_mat}, RED={self.min_red}, TOTAL={self.min_tot}'
            ]

        # Sort by grade needed
        self.modalidades = sorted(self.modalidades, key=lambda x: (x.nota, x.mod_nome), reverse=True)

        mods = [str(m) for m in self.modalidades]

        return '\n'.join(s + mods)

if len(sys.argv) == 1:
    print(f'Usage: py {sys.argv[0]} (year)')
    exit()

year = sys.argv[1]

names_csv = os.path.abspath(os.path.join('..', '..', 'data', year, 'scraping', 'grades.csv'))
output_txt = os.path.abspath(os.path.join('..', '..', 'reports', year, 'grades.txt'))

##################################################

# Read csv and process strings (via class constructors)
print(f'Reading file \'{names_csv}\'...')
try:
    with open(names_csv, mode='r', encoding='UTF-8') as f:
        csv_file_reader = csv.reader(f, delimiter=';')
        cursos = [Curso(l) for l in csv_file_reader]
except FileNotFoundError:
    print(f'File \'{names_csv}\' not found.')
    exit()

# Sort lexicographically
cursos.sort(key=lambda x: (x.campus_uf, x.ies_nome, x.campus_cidade, x.campus_nome, x.curso_nome))

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