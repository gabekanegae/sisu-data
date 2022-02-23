import csv
import os
from datetime import datetime
from time import time

modNomeReduzido = {
"Ampla concorrência": "AC",
"A3 -  o candidato tenha cursado integralmente todas as séries do 2º ciclo do Ensino Fundamental, ou seja, do 6º ao 9º ano, e todas as séries, do Ensino Médio em escolas públicas de todo o território nacional.": "EP",
"COTAS - Escolas Públicas -  Lei Estadual no 6.542, de 7 de dezembro de 2004": "EP",
"Candidato (s) Oriundos da rede pública de ensino.": "EP",
"Candidato (s) que tenham cursado integral, exclusiva e regularmente os anos finais do Ensino Fundamental (6º ao 9º ano) e todo o Ensino Médio em escolas da rede pública estadual ou municipal, excluindo-se os candidatos que tenham concluído curso de nível superior ainda que pendente a colação de grau.": "EP",
"Candidato (s) que tenham cursado integralmente o Ensino Médio em instituições públicas de ensino": "EP",
"Candidatos que tenham cursado integral e exclusivamente os ensinos fundamental e médio em estabelecimentos da rede pública de ensino.": "EP",
"Candidatos que tenham cursado todo o Ensino Médio e os últimos quatro anos do Ensino Fundamental em Escola Pública  e que não se autodeclararam negros.": "EP",
"Candidatos que tenham cursado todo o Ensino Médio e os últimos quatro anos do Ensino Fundamental em Escola Pública e que se autodeclararam negros.": "EP",
"Candidatos que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "EP",
"Cota Social - Candidatos que frequentaram integralmente todas as séries do Ensino Médio ou equivalente em instituições públicas brasileiras de ensino.": "EP",
"com procedência de no mínimo sete anos de estudos regulares ou que tenham realizado curso supletivo ou outra modalidade de ensino equivalente, em estabelecimento da Rede Pública de Ensino do Brasil, compreendendo parte do ensino fundamental (6º ao 9º ano) e Ensino Médio  completo (incluindo os cursos técnicos com duração de 4 anos) ou ter realizado curso supletivo ou outra modalidade de ensino equivalente.": "EP",
"que cursaram o Ensino Médio, integral e exclusivamente, em escola pública do Brasil, e que não tenham concluído curso de graduação": "EP",
"que frequentaram integralmente as 4 últimas séries do Ensino Fundamental e todas as séries do Ensino Médio em instituições públicas brasileiras de ensino.": "EP",
"que independentemente da renda, tenham cursado integralmente o ensino médio em escolas públicas. (L3)": "EP",
"que tenham cursado integralmente o Ensino Médio em escolas públicas.": "EP",
"que tenham cursado integralmente o Ensino Médio em instituições públicas de ensino ou tenham obtido certificado de conclusão com base no resultado do Exame Nacional do Ensino Médio, ENEM, ou do Exame Nacional de Certificação de Competências de Jovens e Adultos, ENCCEJA, ou de exames de certificação de competência ou de avaliação de jovens e adultos realizados pelos sistemas de ensino e não possuam curso superior concluído ou não estejam matriculados em curso superior.": "EP",
"que tenham cursado integralmente o Ensino Médio em instituições públicas e gratuitas de ensino": "EP",
"que tenham cursado o ensino fundamental e médio integralmente em escola pública": "EP",
"que tenham cursado todo o ensino médio e pelo menos dois anos do Ensino Fundamental II em escola pública": "EP",
"Candidato (s) que cursaram o ensino médio, integral e exclusivamente, em escola pública do Brasil e que não tenham concluído curso de graduação.": "EP",
"CANDIDATOS QUE TENHAM CURSADO, NA REDE PÚBLICA, OS ÚLTIMOS QUATRO ANOS DO ENSINO FUNDAMENTAL E TODO O ENSINO MÉDIO": "EP",
"demais de escola pública": "EP",
"que tenham cursado parcialmente o ensino médio em escola pública (pelo menos um ano com aprovação) ou em escolas de direito privado sem fins lucrativos, cujo orçamento da instituição seja proveniente do poder público, em pelo menos 50%.": "EP",
"membros de grupos indígenas": "INDIGENA",
"Candidato (s) Indígenas": "INDIGENA",
"indígenas aldeados": "INDIGENA",
"indígenas, condição que deve ser comprovada mediante apresentação do RANI (Registro Administrativo de Nascimento de Indígena) ou declaração atestada pela FUNAI.": "INDIGENA",
"Candidato (s) indígena": "INDIGENA",
"Candidatos indígenas": "INDIGENA",
"Indígenas": "INDIGENA",
"Candidatos autodeclarados indígenas que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "INDIGENA + EP",
"INDÍGENAS que cursaram integralmente o Ensino Médio em escolas públicas": "INDIGENA + EP",
"Candidatos Indígenas que tenham cursado todo o 2º Ciclo do Ensino Fundamental e o Ensino Médio exclusivamente em escola pública, que tenham renda bruta familiar mensal inferior ou igual a 04 (quatro) vezes o valor do salário mínimo nacional vigente no ato da matrícula e que não possuam título de graduação.": "INDIGENA + RENDA + EP",
"Candidatos Indígenas, de baixa renda que sejam egressos de escola pública:": "INDIGENA + RENDA + EP",
"Candidatos autodeclarados indígenas, com renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo e  que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "INDIGENA + RENDA + EP",
"Candidato (s) economicamente hipossuficientes indígenas": "INDIGENA + RENDA",
"Candidatos que tenham cursado todo o Ensino Médio e os últimos quatro anos do Ensino Fundamental em Escola Pública e que sejam índios reconhecidos pela FUNAI ou moradores de comunidades remanescentes de quilombos registrados na Fundação Cultural Palmares.": "INDIGENA/QUILOMBOLA + EP",
"Categoria VI - Pessoas com deficiência": "PCD",
"Candidato (s) Pessoas com Deficiências - PCD": "PCD",
"Candidato (s) com deficiência": "PCD",
"Candidato (s) com deficiência.": "PCD",
"Candidatos Candidatos Pessoa com Deficiência independentemente da sua condição acadêmica prévia declarada (pública ou privada)": "PCD",
"Candidatos com deficiência:": "PCD",
"Cota para candidatos com deficiência": "PCD",
"com Deficiência, Transtorno do Espectro Autista, Altas Habilidades/Superdotação e/ou estudantes que sejam público alvo da educação especial": "PCD",
"com deficiência (Denominada A1)": "PCD",
"com deficiência que concluíram o Ensino Médio, independente do percurso de formação.": "PCD",
"com deficiência": "PCD",
"com deficiência: será reservada uma vaga, por curso e turno, qualquer que seja a sua procedência escolar.": "PCD",
"Candidatos com deficiência": "PCD",
"com deficiência PROAAf": "PCD",
"Pessoa com Deficiência": "PCD",
"Reserva de vagas para candidatos com deficiência (PCD)": "PCD",
"Candidatos com deficiência que cursaram todo o ensino médio em escolas públicas.": "PCD + EP",
"Candidatos com deficiência que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PCD + EP",
"com deficiência que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PCD + EP",
"Candidatos com deficiência que tenham renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo e que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PCD + RENDA + EP",
"com deficiência que tenham renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo e que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PCD + RENDA + EP",
"Candidatos com deficiência, transtorno do espectro autista e altas habilidades que tenham cursado todo o 2º Ciclo do Ensino Fundamental e o Ensino Médio exclusivamente em escola pública, que tenham renda bruta familiar mensal inferior ou igual a 04 (quatro) vezes o valor do salário mínimo nacional vigente no ato da matrícula e que não possuam título de graduação.": "PCD + RENDA + EP",
"Candidatos com deficiência autodeclarados pretos ou pardos que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PCD + PRETO/PARDO + EP",
"Candidatos com deficiência autodeclarados pretos ou pardos, que tenham renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo e que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PCD + PRETO/PARDO + RENDA + EP",
"autodeclarados Pretos, Pardos e Indígenas": "PPI",
"A2 - Candidatos negros, indígenas e quilombolas com comprovação de carência socioeconômica": "PPI/QUILOMBOLA + RENDA",
"Candidato (s) NEGROS, INDÍGENAS OU QUILOMBOLAS COM COMPROVAÇÃO DE CARÊNCIA SOCIOECONÔMICA": "PPI/QUILOMBOLA + RENDA",
"Candidatos Negros ou Indígenas ou Quilombolas com comprovação de carência socioeconômica": "PPI/QUILOMBOLA + RENDA",
"Candidatos negros, indígenas ou oriundos de comunidades quilombolas com comprovação de carência socioeconômica.": "PPI/QUILOMBOLA + RENDA",
"Candidatos autodeclarados pretos, pardos ou indígenas que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PPI + EP",
"Candidatos que tenha cursado integral e exclusivamente os ensinos fundamental e médio em estabelecimentos da rede pública de ensino e que se autodeclarem negros.": "PPI + EP",
"NEGROS (pretos e pardos) que cursaram integralmente o Ensino Médio em escolas públicas (Banca avaliadora obrigatória)": "PPI + EP",
"autodeclarados pretos, pardos ou indígenas que, independentemente da renda, tenham cursado integralmente o ensino médio em escolas públicas. (L4)": "PPI + EP",
"A2 - Candidatos negros ou indígenas com comprovação de carência socioeconômica": "PPI + RENDA",
"Candidato (s) negros ou indígenas com comprovação de carência socioeconômica": "PPI + RENDA",
"Candidatos autodeclarados pretos, pardos ou indígenas, com renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo e que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PPI + RENDA + EP",
"autodeclarados pretos, pardos ou indígenas com renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo, que tenham cursado integralmente o ensino médio em escolas públicas. (L2)": "PPI + RENDA + EP",
"Candidatos com deficiência autodeclarados pretos, pardos ou indígenas que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PPI + PCD + EP",
"Candidatos com deficiência autodeclarados pretos, pardos ou indígenas, que tenham renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo e que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012)": "PPI + PCD + RENDA + EP",
"Negros (pretos ou pardos) (Denominada A2)": "PRETO/PARDO",
"Negros": "PRETO/PARDO",
"autodeclarados negros de forma irrestrita, independente do percurso de formação.": "PRETO/PARDO",
"negros, entendidos como candidatos que possuem fenótipo que os caracterizem, na sociedade, como pertencentes ao grupo racial negro": "PRETO/PARDO",
"Candidatos autodeclarados pretos ou pardos que, independentemente da renda (art. 14, II, Portaria Normativa nº 18/2012), tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PRETO/PARDO + EP",
"Cota Sociorracial: candidatos(as) autodeclarados(as) negros(as) e que tenham frequentado integralmente todas as séries do Ensino Médio ou equivalente em instituições públicas brasileiras de ensino.": "PRETO/PARDO + EP",
"autodeclarados negros (somatório das categorias pretos e pardos, segundo classificação étnico-racial adotada pelo IBGE) que tenham cursado o ensino fundamental 2 (do 6º ao 9º ano) e ensino medio completo ( incluindo os cursos técnicos com duração de 4 anos) ou ter realizado curso supletivo ou outra modalidade de ensino equivalente, em estabelecimento da Rede Pública de Ensino do Brasil. Vedado aos portadores de diploma de nível superior": "PRETO/PARDO + EP",
"autodeclarados negros que tenham cursado todo o 2º ciclo do Ensino Fundamental (5ª a 8ª séries) e todo o Ensino Médio, única e exclusivamente, na rede pública de ensino no Brasil.": "PRETO/PARDO + EP",
"que se declararem negros que tenham cursado todo o ensino médio e pelo menos dois anos do Ensino Fundamental II em escola pública seguindo a ordem de classificação": "PRETO/PARDO + EP",
"pretos e pardos, que tenham cursado integralmente o Ensino Médio em escolas públicas.": "PRETO/PARDO + EP",
"Candidato (s) economicamente hipossuficientes negros e pardos": "PRETO/PARDO + RENDA",
"Candidatos Negros, de baixa renda que sejam egresso de escola pública:": "PRETO/PARDO + RENDA + EP",
"Candidatos autodeclarados pretos ou pardos, com renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "PRETO/PARDO + RENDA + EP",
"Categoria I - Candidatos declarados negros, de baixa renda e egressos de escola pública": "PRETO/PARDO + RENDA + EP",
"Candidatos Negros que tenham cursado todo o 2º Ciclo do Ensino Fundamental e o Ensino Médio exclusivamente em escola pública, que tenham renda bruta familiar mensal inferior ou igual a 04 (quatro) vezes o valor do salário mínimo nacional vigente no ato da matrícula e que não possuam título de graduação.": "PRETO/PARDO + RENDA + EP",
"Categoria II - Candidatos declarados quilombolas, de baixa renda e egressos de escola pública": "QUILOMBOLA + RENDA + EP",
"Categoria III - Candidatos declarados indígenas, de baixa renda e egressos de escola pública": "INDIGENA + RENDA + EP",
"Candidato (s) Quilombolas": "QUILOMBOLA",
"membros de comunidade quilombola": "QUILOMBOLA",
"de comunidades remanescentes de quilombos ou comunidades identitárias tradicionais": "QUILOMBOLA",
"Candidato (s) economicamente hipossuficientes": "RENDA",
"Candidato (s) que tenham cursado, na rede pública, os últimos quatro anos do ensino fundamental e todo o ensino médio e com comprovação de carência socioeconômica": "RENDA + EP",
"Candidatos Egressos da Escola Pública, de baixa renda:": "RENDA + EP",
"Candidatos com renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo que tenham cursado integralmente o ensino médio em escolas públicas (Lei nº 12.711/2012).": "RENDA + EP",
"Candidatos que tenham cursado na rede pública os últimos quatro anos do ensino fundamental e todo o ensino médio e com comprovação de carência socioeconômica.": "RENDA + EP",
"Categoria V - Outros candidatos de baixa renda e egressos de escola pública": "RENDA + EP",
"com renda familiar bruta per capita igual ou inferior a 1,5 salário mínimo, que tenham cursado integralmente o ensino médio em escolas públicas. (L1)": "RENDA + EP",
"A3 - Candidatos que tenham cursado na rede pública os últimos quatro anos do ensino fundamental e todo o ensino médio e com comprovação de carência socioeconômica": "RENDA + EP",
"Candidatos que tenham cursado na rede pública os últimos quatro anos do ensino fundamental e todo o ensino médio e com comprovação de carência socioeconômica": "RENDA + EP",
"Pessoas Transgêneras em situação de Vulnerabilidade Econômica.": "TRANS",
"transexuais, travestis e transgêneros": "TRANS",
"Pessoas Transgêneras, independentemente de renda familiar": "TRANS",
"Candidatos Transexuais, travestis e transgêneros que tenham cursado todo o 2º Ciclo do Ensino Fundamental e o Ensino Médio exclusivamente em escola pública, que tenham renda bruta familiar mensal inferior ou igual a 04 (quatro) vezes o valor do salário mínimo nacional vigente no ato da matrícula e que não possuam título de graduação.": "TRANS + RENDA + EP"
}

modNomeReduzido = {k.lower(): v for k, v in modNomeReduzido.items()}

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
filename = input("Filename (without extension): /{}/".format(directory))

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