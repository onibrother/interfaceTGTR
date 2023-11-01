import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import time 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from paho.mqtt import client as mqtt_client
import concurrent.futures


broker="192.168.1.45"
client_id = "interface generica"
porta = 1883
topico1 = "telemetriaTemp"
topico2 = "telemetriaUmi"

fig, axs=plt.subplots(2)
fig.suptitle("interface generica tempo-real")

axs[0].set_title("temperatura")
axs[0].set_xlabel("tempo (s)")
axs[0].set_ylabel("temperatura (°C)")

axs[1].set_title("Umidade")
axs[1].set_xlabel("tempo (s)")
axs[1].set_ylabel("umidade relativa (%)")

x1=[]
y1=[]

x2=[]
y2=[]

start=time.time()


def connect_mqtt() -> mqtt_client: 
    def on_connect(client,userdata, flags, rc):
        if rc ==0:
            print("Conexao com o broker feita com sucesso!")
        else:
            print("Nao foi possivel estabelecer conexao com o broker")
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker,porta)
    return client
def subscribe(client: mqtt_client, topic):
    def on_message(client,userdata,msg):
        print(f"Recebida `{msg.payload.decode()}` from `{msg.topic}` topic")

        if msg.topic == topico1:
            with open("logTemp.txt", "a") as arquivo1:
                arquivo1.write(msg.payload.decode())
                arquivo1.write("\n")
        elif msg.topic == topico2:
            with open("logUmi.txt", "a") as arquivo2:
                arquivo2.write(msg.payload.decode())
                arquivo2.write("\n")
    
    client.subscribe(topic)
    client.on_message = on_message

def atualiza(i):
    dados1 = open("logTemp.txt").read()
    dados2 = open("logUmi.txt").read()
    linhas1=dados1.split("\n")
    for j in linhas1:
        if len(j)>0:
            y1.append(float(j))
            if len(x1)==0:
                x1.append(time.time()-start)
            if len(y1)>len(x1):
                x1.append(time.time()-start)
    linhas2=dados2.split("\n")
    for j in linhas2:
        if len(j)>0:
            y2.append(float(j))
            if len(x2)==0:
                x2.append(time.time()-start)
            if len(y2)>len(x2):
                x2.append(time.time()-start)
    axs[0].clear()
    axs[0].plot(x1,y1,"r-o")
    axs[0].set_xlabel("tempo (s)")
    axs[0].set_ylabel("temperatura (º C)")
    axs[0].set_title("temperatura em tempo real")

    axs[1].clear()
    axs[1].plot(x2,y2,"-o")
    axs[1].set_xlabel("tempo (s)")
    axs[1].set_ylabel("Umidade relativa (%)")
    axs[1].set_title("umidade relatica em tempo real")

    y1.clear()
    y2.clear()
def worker1():
    root = tk.Tk()
    serieT = FigureCanvasTkAgg(fig, root)
    serieT.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH)

    a = animation.FuncAnimation(fig,atualiza,interval=1)
    root.mainloop()

def worker2():
    client.loop_forever()


pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)

client=connect_mqtt()
subscribe(client,topico1)
subscribe(client,topico2)


pool.submit(worker2)
pool.submit(worker1)

pool.shutdown(wait=True)
print("feito")