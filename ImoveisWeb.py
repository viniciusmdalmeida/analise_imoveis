from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd

def retirarDados(listaDados):
    quarto = None
    banheiro = None
    area = None
    for dado in listaDados:
        texto = dado.text.strip().replace('\t','').lower()
        valor = texto.split('\n')[0]
        if 'quarto' in texto:
            quarto = int(valor.split('q')[0])
        if 'banheiro' in texto:
            banheiro = int(valor.split('b')[0])
        if 'útil' in texto:
            area = valor.split(' ')[0]
    return (quarto,banheiro,area)

def alterarValor(text):
    valor = text[2:] #Retirando o R$
    valor = valor.replace('.','') #retirando os pontos
    valor = float(valor)
    return valor

def alterarEnd(text):
    bairro = text.split(',')
    bairro = bairro[0]
    return bairro

def PegarDados(listaCasas):
    listaValores = [] #Lista de valores
    listaBairros = [] #Listas de Bairros
    listaQuartos = []
    listaBanheiros = []
    listaArea = []

    for item in listaCasas:
        casa = item
        valor = casa.find('span',{'class':'aviso-data-price-value'})
        ende = casa.find('span',{'class':'aviso-data-location'})
        dados = casa.findAll('li',{'class':'aviso-data-features-value'}) #Pegar quartos
        quartos,banheiros,area = retirarDados(dados)
        if valor != None and ende != None:
            valor = valor.text
            ende = ende.find('span').text
            valorTratado = alterarValor(valor)
            bairro = alterarEnd(ende)
            listaValores.append(valorTratado) #Adicionando Valor tratado a lista de valores
            listaBairros.append(bairro)       #Adicionando Bairro a lista de bairros
            listaQuartos.append(quartos)      #Adicionando Quartos a lista de Quartos
            listaBanheiros.append(banheiros)  #Adicionando Banheiro a lista de Banheiros
            listaArea.append(area)            #Adicionando Area a lista de area
    return listaValores,listaBairros,listaQuartos,listaBanheiros,listaArea # Retornando os dados

def pegarTodosDados(numPag,driver):
    #Pegando todos os dados
    textoSite = driver.find_element_by_tag_name('html').get_attribute("innerHTML")
    soup = BeautifulSoup(textoSite,'html.parser')
    listaCasas = soup.findAll('li',{'class':'aviso-desktop'})
    listaValores,listaBairros,listaQuartos,listaBanheiros,listaArea = PegarDados(listaCasas) #Usando a função e retornando listaValores e ListaBairros
    #Passar para proxima pagina
    numPag += 1
    #Limitando apenas 20 paginas, pode apagar esse if para pegar todo o site
    if numPag > 40:
        return [],[],[],[],[]
    print(numPag)
    #Procurando nova Pagina caso não houver retorna uma lista vazia
    if soup.find('a',{'href':'/apartamentos-venda-q-sao-paulo-pagina-{}.html'.format(numPag)}) != None:
        botao = driver.find_element_by_link_text(str(numPag))
    else:
        return [],[],[],[],[]
    #Se tiver valores faça um click no botão e chame novamente a função recursivamete
    botao.click()
    # valoresPag2,BairrosPag2,listaQuartos2,listaBanheiros2,listaArea2 = pegarTodosDados(numPag)
    # print(valoresPag2,BairrosPag2)
    # #Pegando retorno da função e adicionando a lista existente
    # listaValores+= valoresPag2
    # listaBairros+= BairrosPag2
    # listaQuartos+= listaQuartos2
    # listaBanheiros+= listaBanheiros2
    # listaArea+= listaArea2
    #retornando nova lista
    return listaValores,listaBairros,listaQuartos,listaBanheiros,listaArea

def pesquisar(cidade):
    driver = webdriver.Chrome()
    link = 'https://www.imovelweb.com.br'
    driver.get(link)
    texto = driver.find_element_by_id('searchbox-home_ubicacion')
    botao = driver.find_element_by_id('submitBtn')
    texto.send_keys(cidade)
    botao.send_keys("\n")
    listaValores,listaBairros,listaQuartos,listaBanheiros,listaArea = pegarTodosDados(1,driver)
    tabela = pd.DataFrame()
    tabela['preço'] = listaValores
    tabela['End'] = listaBairros
    tabela['Quartos'] = listaQuartos
    tabela['Banheiros'] = listaBanheiros
    tabela['Area'] = listaArea
    return tabela