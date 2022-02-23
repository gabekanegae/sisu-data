import csv
import os
from datetime import datetime
from time import time

modNomeReduzido = {
"Ampla concorrência": "AC",
"Candidato (s) que tenham cursado integralmente o Ensino Médio em instituições públicas e gratuitas de ensino": "EP",
"que tenham cursado parcialmente o ensino médio em escola pública (pelo menos um ano com aprovação) ou em escolas de direito privado sem fins lucrativos, cujo orçamento da instituição seja proveniente do poder público, em pelo menos 50%.": "EP",
"Candidatos Cota Social - Candidatos que frequentaram integralmente todas as séries do Ensino Médio ou equivalente em instituições públicas brasileiras de ensino.": "EP",
"Candidatos que tenham cursado integralmente o Ensino Médio em escolas públicas;": "EP",
"Candidato (s) que tenham cursado todo o Ensino Médio e os últimos quatro anos do Ensino Fundamental em Escola Pública  e que não se autodeclararam negros.": "EP",
"que tenham cursado integralmente os ensinos fundamental e médio em escolas públicas do sistema educacional brasileiro": "EP",
"COTAS - Escolas Públicas -  Lei Estadual no 6.542, de 7 de dezembro de 2004": "EP",
"Candidato (s) Oriundos da rede pública de ensino.": "EP",
"Candidato (s) que tenham cursado integralmente o Ensino Médio em instituições públicas de ensino": "EP",
"Candidatos que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "EP",
"(as) que independentemente da renda, tenham cursado integralmente o ensino médio em escolas públicas brasileiras. (L3)": "EP",
"Demais Estudantes de Escola Pública": "EP",
"que tenham cursado o ensino fundamental e médio integralmente em escola pública": "EP",
"que tenham cursado integralmente o Ensino Médio em instituições públicas de ensino ou tenham obtido certificado de conclusão com base no resultado do Exame Nacional do Ensino Médio, ENEM, ou do Exame Nacional de Certificação de Competências de Jovens e Adultos, ENCCEJA, ou de exames de certificação de competência ou de avaliação de jovens e adultos realizados pelos sistemas públicos de ensino e não possuam curso superior concluído ou em andamento e não estejam com matrícula trancada em curso superior.": "EP",
"Candidato (s) que frequentaram integralmente as 4 últimas séries do Ensino Fundamental e todas as séries do Ensino Médio em instituições públicas brasileiras de ensino.": "EP",
"Candidato (s) que cursaram o ensino médio, integral e exclusivamente, em escola pública do Brasil e que não tenham concluído curso de graduação.": "EP",
"que que tenham cursado todo o ensino médio e pelo menos quatro anos do Ensino Fundamental em escola pública": "EP",
"que tenham cursado integral, exclusiva e regularmente os anos finais do Ensino Fundamental (6º ao 9º ano) e todo o Ensino Médio em escolas da rede pública estadual ou municipal, excluindo-se os candidatos que tenham concluído curso de nível superior ainda que pendente a colação de grau.": "EP",
"membros de grupos indígenas": "INDIGENA",
"Candidato (s) Indígenas": "INDIGENA",
"indígenas aldeados": "INDIGENA",
"Estudantes Indígenas": "INDIGENA",
"indígenas, condição que deve ser comprovada mediante apresentação do RANI (Registro Administrativo de Nascimento de Indígena) ou declaração atestada pela FUNAI.": "INDIGENA",
"Candidatos autodeclarados indígenas que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "INDIGENA + EP",
"Candidatos autodeclarados indígenas, com renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo e  que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "INDIGENA + RENDA + EP",
"Candidato (s) economicamente hipossuficientes indígenas": "INDIGENA + RENDA",
"Candidato (s) que tenham cursado todo o Ensino Médio e os últimos quatro anos do Ensino Fundamental em Escola Pública e que sejam índios reconhecidos pela FUNAI ou moradores de comunidades remanescentes de quilombos registrados na Fundação Cultural Palmares.": "INDIGENA/QUILOMBOLA + EP",
"Candidato (s) com deficiência": "PCD",
"Cota para candidatos com deficiência": "PCD",
"Candidatos PD - Pessoa com deficiência:": "PCD",
"com Deficiência, Transtorno do Espectro Autista, Altas Habilidades/Superdotação e/ou estudantes que sejam público alvo da educação especial": "PCD",
"com deficiência (Denominada A1)": "PCD",
"com deficiência": "PCD",
"Estudantes com Deficiência": "PCD",
"Pessoas com Deficiência": "PCD",
"com deficiência - PROAAF": "PCD",
"Pessoa com Deficiência.": "PCD",
"L15 - Candidatos Pessoa com Deficiência independentemente da sua condição acadêmica prévia declarada (pública ou privada)": "PCD",
"Será reservada uma vaga, por curso e turno, para candidatos com necessidades educacionais especiais.": "PCD",
"Candidato (s) com deficiência, ou filhos de policiais civis, militares, bombeiros militares e inspetores de segurança e administração penitenciária, mortos ou incapacitados em razão do serviço, com comprovação de carência socioeconômica": "PCD",
"com deficiência que cursaram todo o ensino médio em escola pública.": "PCD",
"que comprovem serem pessoas com deficiência": "PCD",
"Reserva de vagas para candidatos com deficiência (PCD)": "PCD",
"Ação Afirmativa 2: 10% (dez por cento) para pessoas com deficiências que tenham cursado integralmente o Ensino Médio em escolas da rede pública de ensino, com renda per capita de até um salário-mínimo e meio (1,5).": "PCD",
"Candidatos com deficiência que concluíram o Ensino Médio, independente do percurso de formação;": "PCD",
"- 5% das vagas destinadas a candidatos com deficiência com execeção das vagas do SISU.": "PCD",
"V3985: Candidatos com deficiência que, independentemente da renda, tenham cursado integralmente o Ensino Fundamental ou Ensino Médio, conforme o caso, em Escolas Públicas": "PCD + EP",
"Candidatos com deficiência que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PCD + EP",
"com deficiência que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PCD + EP",
"Candidatos com deficiência que tenham renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo e que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PCD + RENDA + EP",
"com deficiência que tenham renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo e que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PCD + RENDA + EP",
"Candidatos com deficiência autodeclarados pretos ou pardos que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PCD + PRETO/PARDO + EP",
"Candidatos com deficiência autodeclarados pretos ou pardos, que tenham renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo e que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PCD + PRETO/PARDO + RENDA + EP",
"autodeclarados Pretos, Pardos e Indígenas": "PPI",
"Candidatos autodeclarados pretos, pardos ou indígenas que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PPI + EP",
"(as) autodeclarados pretos, pardos ou indígenas que, independentemente da renda, tenham cursado integralmente o ensino médio em escolas públicas brasileiras. (L4)": "PPI + EP",
"Candidato (s) negros ou indígenas com comprovação de carência socioeconômica": "PPI + RENDA",
"Candidatos negros ou indígenas com comprovação de carência socioeconômica.": "PPI + RENDA",
"(as) autodeclarados pretos, pardos ou indígenas com renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo, que tenham cursado integralmente o ensino médio em escolas públicas brasileiras. (L2)": "PPI + RENDA + EP",
"Candidatos autodeclarados pretos, pardos ou indígenas, com renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo e que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PPI + RENDA + EP",
"Candidatos com deficiência autodeclarados pretos, pardos ou indígenas que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PPI + PCD + EP",
"Candidatos com deficiência autodeclarados pretos, pardos ou indígenas, que tenham renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo e que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012)": "PPI + PCD + RENDA + EP",
"Negros (pretos ou pardos) (Denominada A2)": "PRETO/PARDO",
"Candidato (s) negros, entendidos como candidatos que possuem fenótipo que os caracterizem, na sociedade, como pertencentes ao grupo racial negro": "PRETO/PARDO",
"Estudantes Negros": "PRETO/PARDO",
"Candidatos autodeclarados negros de forma irrestrita, independente do percurso de formação.": "PRETO/PARDO",
"Candidato (s) autodeclarados negros que tenham cursado todo o 2º ciclo do Ensino Fundamental (5ª a 8ª séries) e todo o Ensino Médio, única e exclusivamente, na rede pública de ensino no Brasil.": "PRETO/PARDO + EP",
"que se declararem negros que tenham cursado todo o ensino médio e pelo menos quatro anos do Ensino Fundamental em escola pública": "PRETO/PARDO + EP",
"NEEP - Negros, de baixa renda que sejam egresso de escola pública:": "PRETO/PARDO + EP",
"Candidatos autodeclarados pretos ou pardos que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PRETO/PARDO + EP",
"Candidato (s) que tenham cursado todo o Ensino Médio e os últimos quatro anos do Ensino Fundamental em Escola Pública e que se autodeclararam negros.": "PRETO/PARDO + EP",
"Candidatos pretos e pardos, que tenham cursado integralmente o Ensino Médio em escolas públicas;": "PRETO/PARDO + EP",
"Candidatos Cota Sociorracial: candidatos(as) autodeclarados(as) negros(as) e que tenham frequentado integralmente todas as séries do Ensino Médio ou equivalente em instituições públicas brasileiras de ensino.": "PRETO/PARDO + EP",
"Candidato (s) economicamente hipossuficientes negros e pardos": "PRETO/PARDO + RENDA",
"Candidatos autodeclarados pretos ou pardos, com renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PRETO/PARDO + RENDA + EP",
"Ação Afirmativa 1: 45% (quarenta e cinco por cento) para pessoas negras, quilombolas e indígenas que tenham cursado integralmente o Ensino Médio em escolas da rede pública de ensino, com renda per capita de até um salário mínimo e meio (1,5).": "PPI/QUILOMBOLA + EP + RENDA",
"Candidatos IEEP - Indígena, de baixa renda, egresso de escola pública:": "INDIGENA + RENDA + EP",
"Candidato (s) Quilombolas": "QUILOMBOLA",
"membros de comunidade quilombola": "QUILOMBOLA",
"de comunidades remanescentes de quilombos ou comunidades identitárias tradicionais": "QUILOMBOLA",
"Candidato (s) economicamente hipossuficientes": "RENDA",
"Candidato (s) que tenham cursado, na rede pública, os últimos quatro anos do ensino fundamental e todo o ensino médio e com comprovação de carência socioeconômica": "RENDA + EP",
"Candidatos com renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "RENDA + EP",
"Candidatos que tenham cursado na rede pública os últimos quatro anos do ensino fundamental e todo o ensino médio e com comprovação de carência socioeconômica.": "RENDA + EP",
"(as) com renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo, que tenham cursado integralmente o ensino médio em escolas públicas brasileiras. (L1)": "RENDA + EP",
"Candidatos EEP - Egresso da escola pública, de baixa renda:": "RENDA + EP",
"Ação Afirmativa 3: 45% (quarenta e cinco por cento) para pessoas que tenham estudado integralmente o Ensino Médio em escolas da rede pública de ensino, com renda per capita de até um salário-mínimo e meio (1,5) e que não estejam concorrendo na forma das ações Afirmativas 1 e 2.": "RENDA + EP",
"Pessoas Transgêneras em situação de Vulnerabilidade Econômica": "TRANS",
"Pessoas Transgêneras, independentemente de renda familiar": "TRANS",
"Transexuais, Travestis e Transgêneros": "TRANS"
}

modNomeReduzido = {k.lower(): v for k, v in modNomeReduzido.items()}

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