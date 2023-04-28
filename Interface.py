from tkinter import *
from ImoveisWeb import pesquisar
from pandastable import Table

def commando():
    textoLog.set('Carregando...')
    tabela = pesquisar(entradaText.get())
    textoLog.set('Finalizado')
    botaoBD['state'] = NORMAL
    tela.geometry('600x400')
    tabelaGUI = Table(frame2, dataframe=tabela, showtoolbar=True, showstatusbar=True)
    tabelaGUI.show()

tela = Tk()
tela.geometry('130x200')
frame = Frame(tela)
frame.pack(side=LEFT,padx=6)
frame2 = Frame(tela)
frame2.pack(side=RIGHT)


texto = Label(frame,text='Digite a cidade:')
texto.pack(pady=2)
entradaText = Entry(frame)
entradaText.pack(pady=2)
botao = Button(frame,text='pesquisar',command=commando)
botao.pack(pady=2)
botaoBD = Button(frame,text='Salvando no BD')
botaoBD.pack(pady=2)
botaoBD['state'] = DISABLED
textoLog = StringVar('')
labelLog = Label(frame,textvariable=textoLog)
labelLog.pack(pady=2)
tela.mainloop()

