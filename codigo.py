import random
import numpy as np
from joblib.numpy_pickle_utils import xrange

def newpop(nInd, cromLin):
    populacao = np.random.choice(nInd*cromLin, size=(nInd,cromLin), replace=False)
    return populacao

def montar_notas(ind):
    todas= {}

    for i in ind:
        nota = []
        for j in range(0,5):
            aux = np.random.uniform(0 , 10)
            aluno = round(aux,1)
            nota.append(aluno)

        todas.update({i:nota})

    return todas

def code(pop):

    for i in range(0, pop.shape[0]):
        for j in range(0, pop.shape[1]):
            aux = np.binary_repr(pop[i][j])
            pop[i,j] = aux
    return pop

def decode(pop, tipo):
    #tipo 1 = matriz
    #tipo 2 = array

    if tipo == 1:
        for i in range(0, pop.shape[0]):
            for j in range(0, pop.shape[1]):
                valor = str(pop[i][j])
                aux = int(valor,2)
                pop[i][j] = aux
    else:
        for i in range(len(pop)):
            valor = str(pop[i])
            aux = int(valor,2)
            pop[i] = aux

    return pop

def funcao_fitness(pop):
    fitness_valores = {}
    for i in range(0, pop.shape[0]):
        fitness = funcao_objetivo(pop[i])
        fitness_valores[i] = fitness

    return fitness_valores

def funcao_objetivo(ind):
    dic_notas = montar_notas(ind)
    notas_aluno = []
    media_alunos = []

    for aluno in dic_notas:
        for i in dic_notas[aluno]:
            notas_aluno.append(i)

        media = round(float(np.mean(notas_aluno)), 1)
        media_alunos.append(media)

    dv = round(float(np.std(media_alunos)), 3)
    return dv

def descobrir_probabilidade_fitness(fitness_valores):
    fitness = fitness_valores.values()
    total_fit = float(sum(fitness))
    fitness_relativo = []
    for i in fitness:
       fitness_relativo.append(i/total_fit)

    probabilidades = []
    for i in range(len(fitness_relativo)):
        probabilidades.append(sum(fitness_relativo[:i+1]))
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
    cp = np.random.randint(lInd-1)+1

    aleatorio = np.random.randint(2)
    if aleatorio == 0:
        filho = pai[0:cp] + mae[cp:lInd]
    else:
        filho = mae[0:cp] + pai[cp:lInd]

    return filho

def mutacao(filhos,taxa_mutacao, dominio):
    flag = 0
    for i in range(len(filhos)):
        if random.random() < taxa_mutacao:
            novo_individuo = list(str(filhos[i]))

            while flag == 0:
                pos = random.randint(0, len(novo_individuo)-1)
                if(novo_individuo[pos] == "0"):
                    novo_individuo[pos] = "1"
                else:
                    novo_individuo[pos] = "0"

                novo = "".join(novo_individuo)
                decode = int(str(novo), 2)
                if decode > dominio:
                    flag = 0
                else:
                    flag = 1

            filhos[i] = novo
    return filhos

#teste
nInd = 10
cromLin = 5
populacao = newpop(nInd,cromLin)
print("\nPopulação ->\n %s" %populacao)
code(populacao)
print("\nPopulação Codificada ->\n %s" %populacao)
fitness = funcao_fitness(populacao)
print("\nFitness -> %s" %fitness)
best_fit = descobrir_probabilidade_fitness(fitness)
print("\nProbabilidade Fitness -> %s" %best_fit)
pais = metodo_roleta(populacao, best_fit, 2)
print("\nPais -> %s" %pais)
filhos = cruzamento(pais)
print("\nFilhos Cruzamento -> %s" %filhos)
filhos = mutacao(filhos, 0.05, nInd*cromLin)
print("\nFilhos Mutação -> %s" %filhos)
#decode(filhos, 2)


decode(populacao, 1)
#print("\nPopulação Decodificada ->\n %s" %populacao)






