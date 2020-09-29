import random
from joblib.numpy_pickle_utils import xrange
import numpy as np
import aluno as a

nInd = 10
cromLin = 30

def newpop(linhas, colunas):
    id_aluno = 0
    populacao = []

    for i in range(0, linhas):
        turma = []
        for j in range(0, colunas):
            id_aluno += 1
            notas = montar_notas()
            aluno = a.Aluno(id_aluno, notas)
            turma.append(aluno)
        populacao.append(turma)

    return populacao

def montar_notas():
    nota = []

    for j in range(0, 5):
        aux = random.uniform(0, 10)
        aluno = round(aux, 1)
        nota.append(aluno)

    return nota

def code(populacao):

    for turmas in populacao:
        for alunos in turmas:
            alunos.id = np.binary_repr(int(alunos.id))

    return populacao

def decode(populacao):

    for turmas in populacao:
        for alunos in turmas:
            aux = int(str(alunos.id), 2)
            alunos.id = aux
    return populacao

def funcao_fitness(pop):
    fitness_valores = {}

    for i in range(0, len(pop)):
        fitness = funcao_objetivo(pop[i])
        fitness_valores[i] = fitness

    return fitness_valores

def funcao_objetivo(turma):
    notas_aluno = []
    media_alunos = []

    for aluno in turma:
        for nota in aluno.notas:
            notas_aluno.append(nota)

        media = round(float(np.mean(notas_aluno)), 1)
        media_alunos.append(media)

    dp = round(float(np.std(media_alunos)), 3)
    return dp

def descobrir_probabilidade_fitness(fitness_valores):
    fitness = fitness_valores.values()
    total_fit = float(sum(fitness))
    fitness_relativo = []
    for i in fitness:
        fitness_relativo.append(i / total_fit)

    probabilidades = []
    for i in range(len(fitness_relativo)):
        probabilidades.append(sum(fitness_relativo[:i + 1]))
    return probabilidades

def metodo_roleta(populacao, probabilidade, numero):
    escolhidos = []
    for n in xrange(numero):
        r = random.random()
        for (i, individual) in enumerate(populacao):
            if r <= probabilidade[i]:
                escolhidos.append(list(individual))
                break
    return escolhidos

def cruzamento(pais):
    pai = pais[0]
    mae = pais[1]

    lInd = int(len(pais[0]))
    cp = np.random.randint(lInd - 1) + 1

    aleatorio = np.random.randint(2)
    if aleatorio == 0:
        filho = pai[0:cp] + mae[cp:lInd]
    else:
        filho = mae[0:cp] + pai[cp:lInd]

    return filho

def mutacao(filho, taxa_mutacao, dominio):
    flag = 0
    alunos_id = []

    for aluno in filho:
        for aluno in filho: alunos_id.append(int(str(aluno.id), 2))
        if random.random() < taxa_mutacao:
            individuo = list(str(aluno.id))

            while flag == 0:
                valorRepetido = 0
                mutado = trocar_valor(individuo)
                mutado_decimal = int(str(mutado), 2)

                if (mutado_decimal > dominio) or (mutado_decimal in alunos_id):
                    flag = 0
                else:
                    flag = 1
            aluno.id = mutado

    return filho

def trocar_valor(valor):
    pos = random.randint(0, len(valor) - 1)
    if (valor[pos] == '0'):
        valor[pos] = '1'
    else:
        valor[pos] = '0'

    novo = "".join(valor)
    return novo

def maior_fitness(fitness):
    maior = max(fitness.values())
    turma = -1
    for key in fitness:
        if fitness[key] == maior:
            turma = key

    return turma

def main():
    populacao_inicial = newpop(nInd, cromLin)
    geracao_atual = code(populacao_inicial)
    fitness = funcao_fitness(populacao_inicial)

    for i in range(0, 50):

        fitness = funcao_fitness(geracao_atual)

        nova_populacao = []
        for k in range(0, nInd):
            prob = descobrir_probabilidade_fitness(fitness)
            pais = metodo_roleta(geracao_atual, prob, 2)
            filho_gerado = cruzamento(pais)
            filho_mutado = mutacao(filho_gerado, 0.1, nInd * cromLin)
            nova_populacao.append(filho_mutado)

        geracao_atual = nova_populacao

    fitness = funcao_fitness(geracao_atual)
    print("\n-=-=-=--=-=-=--=-=-=- MELHOR TURMA -=-=-=--=-=-=--=-=-=-\n")
    for alunos in geracao_atual[maior_fitness(fitness)]:
        print('Aluno {aluno}  => Nota {nota}'.format(aluno = int(str(alunos.id), 2), nota = alunos.notas))

    print("\n\n-=-=-=--=-=-=--=-=-=- TODAS AS TURMAS -=-=-=--=-=-=--=-=-=-\n")

    cont = 0
    for turma in geracao_atual:
        cont += 1
        print('Turma {}  =>  '.format(cont), end='')
        for aluno in turma:
            print(f' {int(str(aluno.id),2) :^3}', end='')
        print()





main()

