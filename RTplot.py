#!/usr/bin/python3
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

fig=plt.figure()
grafico=fig.add_subplot(111)

start=time.time()

x=[]
y=[]

def atualiza(i):
    dados = open("log.txt").read()
    linhas=dados.split("\n")
    for j in linhas:
        if len(j)>0:
            y.append(float(j))
            if len(x)==0:
                x.append(time.time()-start)
            if len(y)>len(x):
                x.append(time.time()-start)
    grafico.clear()
    grafico.plot(x,y,"-o")
    plt.xlabel("tempo (s)")
    plt.ylabel("valor digitado")
    plt.title("teste leitura em tempo real")
    y.clear()


a = animation.FuncAnimation(fig,atualiza,interval=1)
plt.show()

