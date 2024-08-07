# -*- coding: utf-8 -*-
"""Sorteio_Loterica

Automatically generated by Colab.


import pandas as pd
import datetime
import statistics as st
import random as rand
import numpy as np
from google.colab import files
#Ajustando para mostrar todas as colunas do dataframe
pd.set_option('display.max_columns', None)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('max_colwidth', -1)

uploaded = files.upload()

"""# Classe Arquivo"""

class Arquivo:

  def __init__(self, nomeArquivo):
    self.__data = pd.read_excel(nomeArquivo)
    excluirCampos = self.__data.loc[(self.__data["Estimativa_Prêmio"] == "0,00") &
                                    (self.__data["Arrecadacao_Total"] == "0,00")]
    self.__data = self.__data.drop(excluirCampos.index)
    self.__data['Estimativa_Prêmio'] = self.tratarCampo("Estimativa_Prêmio")
    self.__data['Arrecadacao_Total'] = self.tratarCampo("Arrecadacao_Total")



  def tratarCampo(self, nomeCampo):
    # Método para tratar campos com valores financeiros
    self.__data[nomeCampo] = self.__data[nomeCampo].str.replace(',', '.')
    self.__data[nomeCampo] = self.__data[nomeCampo].str.replace('.', '')
    self.__data[nomeCampo] = pd.to_numeric(self.__data[nomeCampo])
    self.__data[nomeCampo] = self.__data[nomeCampo] / 100
    return self.__data[nomeCampo]

  def filtrandoColunas(self, data):
    self.__data = self.__data[['Concurso',
                            'Data Sorteio',
                            '1número_Sorteio1',
                            '2número_Sorteio1',
                            '3número_Sorteio1',
                            '4número_Sorteio1',
                            '5número_Sorteio1',
                            '6número_Sorteio1',
                            '1número_Sorteio2',
                            '2número_Sorteio2',
                            '3número_Sorteio2',
                            '4número_Sorteio2',
                            '5número_Sorteio2',
                            '6número_Sorteio2',
                            'Estimativa_Prêmio']]
    return self.__data

  '''Getter e setter'''
  @property
  def getData(self):
    return self.__data

  @getData.setter
  def setData(self, data):
    self.self.__data = data




arquivoInicial = Arquivo('duplaSena.xlsx')
dadosRetornados = arquivoInicial.getData
#dadosRetornados.dtypes
#dadosRetornados.tail(50)

"""# Classe Jogos"""

class Jogos(Arquivo):

  def __init__(self):
    super().__init__('duplaSena.xlsx')
    self.dados = self.filtrandoColunas('duplaSena.xlsx')


  def criarJogoInicioAte2020(self):
    # Método responsável por selecionar os números jogados do primeiro concurso
    # até o último concurso do ano de 2020
    todosJogos = self.filtrandoColunas('duplaSena.xlsx')
    todosJogos['Data Sorteio'] = pd.to_datetime(todosJogos['Data Sorteio'])
    selecao = (todosJogos['Data Sorteio'] >= '01/01/2001') & (todosJogos['Data Sorteio'] <= '31/12/2020')
    dataFiltrada = todosJogos[selecao]

    '''Calculando a moda dos números do sorteio 1'''
    bilheteCandidatoSort1 = self.calcularBilheteCandidatoModa(dataFiltrada,'1')

    '''Calculando a moda dos números do sorteio 2'''
    bilheteCandidatoSort2 = self.calcularBilheteCandidatoModa(dataFiltrada,'2')

    print("Jogos do início até 2020 x resultados de 2021: ")
    print(f"Bilhete Candidato 1: {bilheteCandidatoSort1}")
    print(f"Bilhete Candidato 2: {bilheteCandidatoSort2}")

    '''Separando os jogos de 2021'''
    dataFiltrada21 = self.separarJogos2021()

    '''Verificando se o bilhete formado pela moda dos resultados do primeiro sorteio foi sorteado em 2021'''
    testeBilhete1 = self.comparaBilhetes(bilheteCandidatoSort1,dataFiltrada21,'1')

    '''Verificando se o bilhete formado pela moda dos resultados do primeiro sorteio foi sorteado em 2021'''
    testeBilhete2 = self.comparaBilhetes(bilheteCandidatoSort1,dataFiltrada21,'2')

    '''Verifica se algum bilhete foi premiado ou não'''
    self.verificaBilheteVenceu(testeBilhete1, testeBilhete2)

  def criarJogo2010Ate2020(self):
    # Método responsável por selecionar os números jogados dos anos de 2010 até 2020
    todosJogos = self.filtrandoColunas('duplaSena.xlsx')
    todosJogos['Data Sorteio'] = pd.to_datetime(todosJogos['Data Sorteio'])
    selecao = (todosJogos['Data Sorteio'] >= '01/01/2010') & (todosJogos['Data Sorteio'] <= '31/12/2020')
    dataFiltrada = todosJogos[selecao]
    #print(dataFiltrada)

    '''Calculando a moda dos números do sorteio 1'''
    bilheteCandidatoSort1 = self.calcularBilheteCandidatoModa(dataFiltrada,'1')

    '''Calculando a moda dos números do sorteio 2'''
    bilheteCandidatoSort2 = self.calcularBilheteCandidatoModa(dataFiltrada,'2')

    print("Jogos de 2010 até 2020 x resultados de 2021: ")
    print(f"Bilhete Candidato 1: {bilheteCandidatoSort1}")
    print(f"Bilhete Candidato 2: {bilheteCandidatoSort2}")

    '''Separando os jogos de 2021'''
    dataFiltrada21 = self.separarJogos2021()

    '''Verificando se os números escolhidos pelo usuário foi sorteado em 2021'''
    testeBilhete1 = self.comparaBilhetes(bilheteCandidatoSort1,dataFiltrada21,'1')

    '''Verificando se os números escolhidos pelo usuário foi sorteado em 2021'''
    testeBilhete2 = self.comparaBilhetes(bilheteCandidatoSort1,dataFiltrada21,'2')

    '''Verifica se algum bilhete foi premiado ou não'''
    self.verificaBilheteVenceu(testeBilhete1, testeBilhete2)


  def criarJogo2015Ate2020(self):
    # Método responsável por selecionar os números jogados dos anos de 2015 até 2020
    todosJogos = self.filtrandoColunas('duplaSena.xlsx')
    todosJogos['Data Sorteio'] = pd.to_datetime(todosJogos['Data Sorteio'])
    selecao = (todosJogos['Data Sorteio'] >= '01/01/2015') & (todosJogos['Data Sorteio'] <= '31/12/2020')
    dataFiltrada = todosJogos[selecao]

    '''Calculando a moda dos números do sorteio para criar o bilhete candidato 3'''
    bilheteCandidatoSort1 = self.calcularBilheteCandidatoModa(dataFiltrada,'1')

    '''Calculando a moda dos números do sorteio 2'''
    bilheteCandidatoSort2 = self.calcularBilheteCandidatoModa(dataFiltrada,'2')

    print("Jogos de 2015 até 2020 x resultados de 2021: ")
    print(f"Bilhete Candidato 1: {bilheteCandidatoSort1}")
    print(f"Bilhete Candidato 2: {bilheteCandidatoSort2}")

    '''Separando os jogos de 2021'''
    dataFiltrada21 = self.separarJogos2021()

    '''Compara os números escolhidos pela moda foi sorteado em 2021'''
    testeBilhete1 = self.comparaBilhetes(bilheteCandidatoSort1,dataFiltrada21,'1')

    '''Compara os números escolhidos pela moda foi sorteado em 2021'''
    testeBilhete2 = self.comparaBilhetes(bilheteCandidatoSort1,dataFiltrada21,'2')

    '''Verifica se algum bilhete foi premiado ou não'''
    self.verificaBilheteVenceu(testeBilhete1, testeBilhete2)

  def verificaBilheteVenceu(self,bilhete1,bilhete2):
    if bilhete1.empty and bilhete2.empty:
      print("...Seu bilhete não foi premiado")
      return False
    elif len(bilhete1) > 0 and bilhete2.empty:
      print("Bilhete premiado!!!")
      print(bilhete1)
      return True

    elif len(bilhete2) > 0 and bilhete1.empty:
      print("Bilhete premiado!!!")
      print(bilhete2)
      return True

    else:
      print("Bilhete premiado!!!\n")
      #print(f"O bilhete foi premiado: {contador} vezes")
      print(bilhete1)
      print(bilhete2)
      return True

  def comparaBilhetes(self,bilheteCandidato,dfJogos2021,numSorteio):

    bilhete = dfJogos2021[(dfJogos2021['1número_Sorteio'+numSorteio].isin(bilheteCandidato))
                   & (dfJogos2021['2número_Sorteio'+numSorteio].isin(bilheteCandidato))
                   & (dfJogos2021['3número_Sorteio'+numSorteio].isin(bilheteCandidato))
                   & (dfJogos2021['4número_Sorteio'+numSorteio].isin(bilheteCandidato))
                   & (dfJogos2021['5número_Sorteio'+numSorteio].isin(bilheteCandidato))
                   & (dfJogos2021['6número_Sorteio'+numSorteio].isin(bilheteCandidato))]
    return bilhete

  def calcularBilheteCandidatoModa(self, df, numSorteio):
    numerosSorteados = []
    for i in range(1,7):
      campo = str(i)+'número_Sorteio'+numSorteio
      numerosSorteados.append(df[campo].mode().iloc[0])
      campo = ''
    return numerosSorteados

  def calcularBilheteCandidatoQuantil(self, df, numSorteio):
    numerosSorteados = []
    for i in range(1,7):
      campo = str(i)+'número_Sorteio'+numSorteio
      numerosSorteados.append(df[campo].quantile())
      campo = ''
    return numerosSorteados

  def separarJogos2021(self):
    # Método responsável por guardar todos os jogos de 2021
    todosJogos = self.filtrandoColunas('duplaSena.xlsx')

    todosJogos['Data Sorteio'] = pd.to_datetime(todosJogos['Data Sorteio'])
    selecao = (todosJogos['Data Sorteio'] >= '01/01/2021') & (todosJogos['Data Sorteio'] <= '31/12/2021')
    jogos2021 = todosJogos[selecao]
    return jogos2021


  def verificandoBilheteUsuario(self):
    # Método extra para o usuário testar seus próprios números
    jogos = self.filtrandoColunas('duplaSena.xlsx')


    '''Criando uma lista com os palpites do usuário'''
    bilheteUsuario = []
    while len(bilheteUsuario) < 6:
      x = int(input("Escreva um número: "))
      if x in bilheteUsuario:
        print("O número já foi escolhido.")
      else:
        bilheteUsuario.append(x)
    print(f"\nPalpite: {bilheteUsuario}")

    testeBilhete1 = self.comparaBilhetes(bilheteUsuario,jogos,'1')

    testeBilhete2 = self.comparaBilhetes(bilheteUsuario,jogos,'2')

    '''Verifica se algum bilhete foi premiado ou não'''
    self.verificaBilheteVenceu(testeBilhete1, testeBilhete2)


  def GerarBilheteCandidatoModo1(self):
    # Neste método vamos gerar um bilhete candidato usando moda, media
    # Primeiramente vamos sortear um número de 0 a 100
    # Caso seja par usa moda, ímpar usa media, múltiplo de 5 usa quantil
    listaCampos = [
      '1número_Sorteio1',
      '2número_Sorteio1',
      '3número_Sorteio1',
      '4número_Sorteio1',
      '5número_Sorteio1',
      '6número_Sorteio1',
      '1número_Sorteio2',
      '2número_Sorteio2',
      '3número_Sorteio2',
      '4número_Sorteio2',
      '5número_Sorteio2',
      '6número_Sorteio2']
    bilhete = []
    i = 0
    df = self.getData
    x = int(input("Quantos números deseja jogar? "))
    valorAposta = (x * 2.50)
    numSorteado = 0
    while(x):
      numAleatorio = rand.randrange(1,101)
      if(numAleatorio % 5 == 0 and numAleatorio % 2 != 0):
        numSorteado = int(df[listaCampos[i]].quantile())
      elif(numAleatorio % 2 == 0):
        numSorteado = df[listaCampos[i]].mode().iloc[0]
      elif(numAleatorio % 2 == 1):
        numSorteado = int(df[listaCampos[i]].mean())

      if(numSorteado not in bilhete):
        bilhete.append(numSorteado)
        x-=1
      elif(((numAleatorio // 2) not in bilhete) and ((numAleatorio // 2) > 0) and (i == 10)):
        bilhete.append((numAleatorio // 2))
        x-=1
      i+=1
      if(i == 11):
        i = 0
    return sorted(bilhete)

  def criarPalpitesAleatorios(self):
    # Método responsável por criar dois jogos de forma completamente aleatória
    loop = 0
    jogo1 = []
    jogo2 = []

    while loop < 6:
      numSorteado = rand.randrange(1,51)
      if(numSorteado not in jogo1):
        jogo1.append(numSorteado)
        loop += 1

    loop = 0

    while loop < 6:
      numSorteado = rand.randrange(1,51)
      if(numSorteado not in jogo2 and numSorteado not in jogo1):
        jogo2.append(numSorteado)
        loop += 1

    print(jogo1)
    print(jogo2)
    return jogo1, jogo2



meuJogo = Jogos()
#print(meuJogo.criarJogo())
meuJogo.criarJogo2015Ate2020()
meuJogo.criarJogo2010Ate2020()
meuJogo.criarJogoInicioAte2020()
meuJogo.verificandoBilheteUsuario()

'''
a = meuJogo.GerarBilheteCandidatoModo1()
b = meuJogo.GerarBilheteCandidatoModo1()
print(a,b)
b1 = meuJogo.comparaBilhetes(a,meuJogo.separarJogos2021(),'1')
b2 = meuJogo.comparaBilhetes(b,meuJogo.separarJogos2021(),'2')
meuJogo.verificaBilheteVenceu(b1,b2)
'''

#meuJogo.verificarBilheteModa()
#meuJogo.comparaBilhetes()

meuJogo = Jogos()
#print(meuJogo.criarJogo())
#meuJogo.criarJogo2015Ate2020()
#meuJogo.criarJogo2010Ate2020()
#meuJogo.criarJogoInicioAte2020()
#meuJogo.verificandoBilheteUsuario()


loop = True
contador = 0
while(loop):
  a, b = meuJogo.criarPalpitesAleatorios()
  b1 = meuJogo.comparaBilhetes(a,meuJogo.separarJogos2021(),'1')
  b2 = meuJogo.comparaBilhetes(b,meuJogo.separarJogos2021(),'2')
  teste = meuJogo.verificaBilheteVenceu(b1,b2)
  contador = contador + 1
  if(teste):
    loop = False


valorAposta = (contador * 2.50)

premioTeste = b1.loc[:,'Estimativa_Prêmio'] - valorAposta
premioTeste2 = b2.loc[:,'Estimativa_Prêmio'] - valorAposta

print(f"Valor total gasto: {valorAposta}")
print(f"Prêmio: {premioTeste.to_string(index=False)}")
print(f"Prêmio TESTE: {premioTeste2.to_string(index=False)}")

"""# Classe Estatística"""

class Estatistica(Arquivo):
  def __init__(self):
    super().__init__('duplaSena.xlsx')
    self.dados = self.getData


  def estatisticaDados(self):
    jogosDuplaSena = self.getData

    #Usando describe() para retornar as estatísticas do dataframe
    todasEstatisticas = jogosDuplaSena.describe()

    print(todasEstatisticas)

    mediaEstimPremio = jogosDuplaSena['Estimativa_Prêmio'].mean()
    mediaTotalArrec = jogosDuplaSena['Arrecadacao_Total'].mean()

    '''Ordenando dados para a mediana'''
    jogosDuplaSenaOrd = jogosDuplaSena.sort_values(by=['Ganhadores_Sena_Sorteio1','Ganhadores_Sena_Sorteio2'], ascending=False)

    '''Calculando a mediana'''
    medianaGanhadoresSena1 = jogosDuplaSenaOrd['Ganhadores_Sena_Sorteio1'].median()
    medianaGanhadoresSena2 = jogosDuplaSenaOrd['Ganhadores_Sena_Sorteio2'].median()

    '''Calculando a moda dos números do sorteio 1'''
    modaNum1Sort1 = jogosDuplaSena['1número_Sorteio1'].mode()
    modaNum2Sort1 = jogosDuplaSena['2número_Sorteio1'].mode()
    modaNum3Sort1 = jogosDuplaSena['3número_Sorteio1'].mode()
    modaNum4Sort1 = jogosDuplaSena['4número_Sorteio1'].mode()
    modaNum5Sort1 = jogosDuplaSena['5número_Sorteio1'].mode()
    modaNum6Sort1 = jogosDuplaSena['6número_Sorteio1'].mode()

    '''Calculando a moda dos números do sorteio 2'''
    modaNum1Sort2 = jogosDuplaSena['1número_Sorteio2'].mode()
    modaNum2Sort2 = jogosDuplaSena['2número_Sorteio2'].mode()
    modaNum3Sort2 = jogosDuplaSena['3número_Sorteio2'].mode()
    modaNum4Sort2 = jogosDuplaSena['4número_Sorteio2'].mode()
    modaNum5Sort2 = jogosDuplaSena['5número_Sorteio2'].mode()
    modaNum6Sort2 = jogosDuplaSena['6número_Sorteio2'].mode()


    '''Calculando o quantil dos números do sorteio 1'''
    quantilNum1Sort1 = jogosDuplaSena['1número_Sorteio1'].quantile()
    quantilNum2Sort1 = jogosDuplaSena['2número_Sorteio1'].quantile()
    quantilNum3Sort1 = jogosDuplaSena['3número_Sorteio1'].quantile()
    quantilNum4Sort1 = jogosDuplaSena['4número_Sorteio1'].quantile()
    quantilNum5Sort1 = jogosDuplaSena['5número_Sorteio1'].quantile()
    quantilNum6Sort1 = jogosDuplaSena['6número_Sorteio1'].quantile()

    '''Calculando o quantil dos números do sorteio 2'''
    quantilNum1Sort2 = jogosDuplaSena['1número_Sorteio2'].quantile()
    quantilNum2Sort2 = jogosDuplaSena['2número_Sorteio2'].quantile()
    quantilNum3Sort2 = jogosDuplaSena['3número_Sorteio2'].quantile()
    quantilNum4Sort2 = jogosDuplaSena['4número_Sorteio2'].quantile()
    quantilNum5Sort2 = jogosDuplaSena['5número_Sorteio2'].quantile()
    quantilNum6Sort2 = jogosDuplaSena['6número_Sorteio2'].quantile()

    #print(f"Média do prêmio estimado: {mediaEstimPremio}")
    print('\n\nMédia do prêmio estimado {:.2f}'.format(mediaEstimPremio))
    print('Média do total arrecadado {:.2f}'.format(mediaTotalArrec))
    #print(f"Média do total arrecadado: {mediaTotalArrec}")
    print(f"Mediana dos ganhadores do sorteio 1: {medianaGanhadoresSena1}")
    print(f"Mediana dos ganhadores do sorteio 2: {medianaGanhadoresSena2}")


    print("\nModa Sorteio Um:")
    print(modaNum1Sort1)
    print(modaNum2Sort1)
    print(modaNum3Sort1)
    print(modaNum4Sort1)
    print(modaNum5Sort1)
    print(modaNum6Sort1)

    print("\nModa Sorteio Dois:")
    print(modaNum1Sort2)
    print(modaNum2Sort2)
    print(modaNum3Sort2)
    print(modaNum4Sort2)
    print(modaNum5Sort2)
    print(modaNum6Sort2)


    print("\nQuantil Sorteio Um:")
    print(quantilNum1Sort1)
    print(quantilNum2Sort1)
    print(quantilNum3Sort1)
    print(quantilNum4Sort1)
    print(quantilNum5Sort1)
    print(quantilNum6Sort1)

    print("\nQuantil Sorteio Dois:")
    print(quantilNum1Sort2)
    print(quantilNum2Sort2)
    print(quantilNum3Sort2)
    print(quantilNum4Sort2)
    print(quantilNum5Sort2)
    print(quantilNum6Sort2)

teste = Estatistica()
teste.estatisticaDados()