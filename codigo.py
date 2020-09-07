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

def decode(pop):
    for i in range(0, pop.shape[0]):
        for j in range(0, pop.shape[1]):
            valor = str(pop[i][j])
            aux = int(valor,2)
            pop[i][j] = aux

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

#teste
populacao = newpop(10,10)
#print(populacao)
#valor = funcao_fitness(populacao)
#teste = descobrir_probabilidade_fitness(valor)
#print(metodo_roleta(populacao,teste, 2))
#print(dic)
#print("\npreenchido ->\n %s" %populacao)
#code(populacao)
#print("\ncode ->\n %s" %populacao)
#decode(populacao)
#print("\ndecode ->\n %s" %populacao)
