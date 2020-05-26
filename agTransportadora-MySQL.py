# ========== Limpa o terminal para uma melhor visualização ====================
import os
os.system('cls' if os.name == 'nt' else 'clear')

# ==================== ALGORITMO GENÉTICO ====================
from random import *
import matplotlib.pyplot as plt
import pymysql

class Produto():
    def __init__(self, nome, espaco, valor):
        self.nome = nome
        self.espaco = espaco
        self.valor = valor

class Individuo():
    def __init__(self, espacos, valores, limiteEspacos, geracao = 0):
        self.espacos = espacos
        self.valores = valores
        self.limiteEspacos = limiteEspacos
        self.geracao = geracao

        self.notaAvaliacao = 0      # 'Nota de Avaliação' é a soma dos valores do caregamento do caminhão
        self.espacoUsado = 0

        self.cromossomo = []

        for i in range(len(espacos)):
            # ---------- Gerando valores binários aleatórios ----------
            if random() < 0.5:      # random() retorna um valor entre 0 e 1
                self.cromossomo.append("0")
            else:
                self.cromossomo.append("1")
    
    def avaliacao(self):
        nota = 0
        somaEspacos = 0

        for i in range(len(self.cromossomo)):
            if self.cromossomo[i] == '1':
                nota += self.valores[i]
                somaEspacos += self.espacos[i]
        
        if somaEspacos > self.limiteEspacos:
            nota = 1        # Atribuir uma nota baixa por este indivíduo exceder o limite de carga
        
        self.notaAvaliacao = nota
        self.espacoUsado = somaEspacos

    def crossover(self, outroIndividuo):
        corte = round(random() * len(self.cromossomo))      # Arredonda para um valor inteiro o ponto de corte
        # print("Ponto de Corte: %i" % corte)

        filho1 = outroIndividuo.cromossomo[0:corte] + self.cromossomo[corte::]      # Cromossomo do Filho 1
        filho2 = outroIndividuo.cromossomo[corte::] + self.cromossomo[0:corte]      # Cromossomo do Filho 2

        filhos = [
            Individuo(self.espacos, self.valores, self.limiteEspacos, self.geracao + 1),
            Individuo(self.espacos, self.valores, self.limiteEspacos, self.geracao + 1)
        ]

        filhos[0].cromossomo = filho1 
        filhos[1].cromossomo = filho2

        return filhos

    def mutacao(self, taxaMutacao):
        # print("Antes da Mutação: %s" % self.cromossomo)
        
        for i in range(len(self.cromossomo)):
            if random() < taxaMutacao:
                if self.cromossomo[i] == '1':
                    self.cromossomo[i] = '0'
                else:
                    self.cromossomo[i] = '1'
        
        # print("Depois da Mutação: %s" % self.cromossomo)
        return self

class AlgoritmoGenetico():
    def __init__(self, tamanhoPopulacao):
        self.tamanhoPopulacao = tamanhoPopulacao
        self.populacao = []
        self.geracao = 0
        self.melhorSolucao = 0
        self.listaSolucoes = []
    
    def inicializarPopulacao(self, espacos, valores, limiteEspacos):
        for i in range(tamanhoPopulacao):
            self.populacao.append(Individuo(espacos, valores, limiteEspacos))
        
        self.melhorSolucao = self.populacao[0]

    def ordenaPopulacao(self):
        self.populacao = sorted(
            self.populacao,
            key = lambda populacao: populacao.notaAvaliacao,
            reverse = True
        )

    def melhorIndividuo(self, individuo):
        if individuo.notaAvaliacao > self.melhorSolucao.notaAvaliacao:
            self.melhorSolucao = individuo

    def somaAvaliacoes(self):
        soma = 0
        
        for individuo in self.populacao:
            soma += individuo.notaAvaliacao
        
        return soma

    def selecionaPai(self, somaAvaliacao):
        pai = -1
        soma = 0
        i = 0

        valorSorteado = random() * somaAvaliacao

        while i < len(self.populacao) and soma < valorSorteado:
             soma += self.populacao[i].notaAvaliacao
             pai +=  1
             i += 1
        
        return pai

    def visualizaGeracao(self):
        melhor = self.populacao[0]
        print(" ----- Melhor da Geração %s ----------" % melhor.geracao)
        print("Valor (notaAvaliacao): R$%s" % melhor.notaAvaliacao)
        print("Espaco: %s" % melhor.espacoUsado)
        print("Cromossomo: %s\n" % melhor.cromossomo)

    def resolver(self, taxaMutacao, numeroGeracoes, espacos, valores, limiteEspacos):
        self.inicializarPopulacao(espacos, valores, limiteEspacos)
        
        for individuo in self.populacao:
            individuo.avaliacao()

        self.ordenaPopulacao()

        melhorSolucao = self.populacao[0]
        self.listaSolucoes.append(self.melhorSolucao.notaAvaliacao)

        # self.visualizaGeracao()

        for geracao in range(numeroGeracoes):
            somaAvaliacao = self.somaAvaliacoes()
            novaPopulacao = []

            for individuosGerados in range(0, self.tamanhoPopulacao, 2):
                pai1 = self.selecionaPai(somaAvaliacao)
                pai2 = self.selecionaPai(somaAvaliacao)
                
                filhos = self.populacao[pai1].crossover(self.populacao[pai2])

                novaPopulacao.append(filhos[0].mutacao(taxaMutacao))
                novaPopulacao.append(filhos[1].mutacao(taxaMutacao))

            self.populacao = list(novaPopulacao)

            for individuo in self.populacao:
                individuo.avaliacao()

            self.ordenaPopulacao()

            # self.visualizaGeracao()

            melhor = self.populacao[0]
            self.listaSolucoes.append(melhor.notaAvaliacao)
            self.melhorIndividuo(melhor)

        print(" ==================== Melhor Solução de Todas ==================== ")
        print("> Valor (notaAvaliacao): %s" % self.melhorSolucao.notaAvaliacao)
        print("> Espaço: %s" % self.melhorSolucao.espacoUsado)
        print("> Cromossomo: %s" % self.melhorSolucao.cromossomo)
        print("> Geração: %s\n" % self.melhorSolucao.geracao)

        return self.melhorSolucao.cromossomo

if __name__ == '__main__':      # Ajuste para o uso de módulos no Python
    listaProdutos = []      # Criando o vetor 'listaProdutos'

    # Criando a Conexão com o MySQL
    conexao = pymysql.connect(
        host = 'localhost',
        user = 'root',
        passwd = 'root',
        db = 'transportadora'
    )

    cursor = conexao.cursor()    # Necessário para efetuar as consultas ao banco de dados
    cursor.execute('SELECT nome, espaco, valor, quantidade FROM produtos')
    
    # print(" -------------------- Produtos --------------------")
    # for produto in cursor:
    #     print("Nome: %s" % produto[0])       # Imprime o 'nome' recebido pelo SELECT
    #     print("Espaco: %s" % produto[1])       # Imprime o 'espaco' recebido pelo SELECT
    #     print("Valor: %s" % produto[2])       # Imprime o 'valor' recebido pelo SELECT
    #     print("Quantidade: %s\n" % produto[3])       # Imprime a 'quantidade' recebida pelo SELECT

    # # Gerando lista de produtos para o Algoritmo Genético com os valores recebidos através da consulta ao BD
    # for produto in cursor:
    #     listaProdutos.append(Produto(produto[0], produto[1], produto[2]))

    # Gerando lista de produtos para o Algoritmo Genético com os valores recebidos através da consulta ao BD
    for produto in cursor:
        for i in range(produto[3]):
            listaProdutos.append(Produto(produto[0], produto[1], produto[2]))

    # for produto in listaProdutos:
    #     print(produto.nome)

    cursor.close()
    conexao.close()

    # ---------- Criando vetores ----------
    espacos = []
    valores = []
    nomes = []

    # ---------- Armazena espaco, valor e nome de cada produto nos vetores acima ----------
    for produto in listaProdutos:
        espacos.append(produto.espaco)
        valores.append(produto.valor)
        nomes.append(produto.nome)

    # ---------- Algoritmo Genético ----------
    limite = 10      # Limite de carga do caminhão em m³
    tamanhoPopulacao = 20
    taxaMutacao = 0.01
    numeroGeracoes = 200

    ag = AlgoritmoGenetico(tamanhoPopulacao)
    resultado =  ag.resolver(taxaMutacao, numeroGeracoes, espacos, valores, limite)

    for i in range(len(listaProdutos)):
        if resultado[i] == '1':
            print("Nome: %s \t\t Valor: R$%s" % (listaProdutos[i].nome, listaProdutos[i].valor))

    # for valor in ag.listaSolucoes:
    #     print(valor)

    # Impressao do Gráfico para Acompanhamento dos Valores
    plt.plot(ag.listaSolucoes)
    plt.title("Acompanhamento dos Valores")
    plt.show()