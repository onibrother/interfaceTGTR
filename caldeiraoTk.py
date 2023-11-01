from tkinter import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt 
import time
import matplotlib.animation as animation
from paho.mqtt import client as mqtt_client
import concurrent.futures

janela = Tk()
fig,axs = plt.subplots(2)
axs[0].set_xlabel("tempo(ms)")
axs[0].set_ylabel("temperatura(°C)")

axs[1].set_xlabel("tempo(ms)")
axs[1].set_ylabel("umidade Relativa(%)")

start=time.time()

x1=[]
y1=[]

x2=[]
y2=[]


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
    # axs[0].set_title("temperatura em tempo real")

    axs[1].clear()
    axs[1].plot(x2,y2,"-o")
    axs[1].set_xlabel("tempo (s)")
    axs[1].set_ylabel("Umidade relativa (%)")
    # axs[1].set_title("umidade relatica em tempo real")

    y1.clear()
    y2.clear()

def connect_mqtt() -> mqtt_client: 
    def on_connect(client,userdata, flags, rc):
        if rc ==0:
            print("Conexao com o broker feita com sucesso!")
        else:
            print("Nao foi possivel estabelecer conexao com o broker")
    client = mqtt_client.Client("interfacePrototipo_LabLux")
    client.on_connect = on_connect
    client.connect("127.0.0.1",1883)
    return client
def subscribe(client: mqtt_client, topic):
    def on_message(client,userdata,msg):
        print(f"Recebida `{msg.payload.decode()}` from `{msg.topic}` topic")

        if msg.topic == "telemetriaTemp":
            with open("logTemp.txt", "a") as arquivo1:
                arquivo1.write(msg.payload.decode())
                arquivo1.write("\n")
        elif msg.topic == "telemetriaUmi":
            with open("logUmi.txt", "a") as arquivo2:
                arquivo2.write(msg.payload.decode())
                arquivo2.write("\n")
        
    client.subscribe(topic)
    client.on_message = on_message

client = connect_mqtt()
subscribe(client, "telemetriaTemp")
subscribe(client,"telemetriaUmi")


class app():
    def __init__(self):    
        self.janela = janela
        self.tela()
        self.frames_janela() 
        self.widgets()
        # a = animation.FuncAnimation(fig,atualiza,interval=1)
        janela.mainloop() 

        
        
    
    def tela(self):
        self.janela.title("Prototico interface LabLux")
        self.janela.minsize(1000,500)
        self.janela.resizable(False,False)
        self.janela.configure(background="#4682B4")

    def frames_janela(self):
        self.frameGrafico = Frame(self.janela,bd=4,bg="#DEB887")
        self.frameGrafico.place(relx=0.01,rely=0.05,relwidth=0.62, relheight=0.85)
        
        self.frameInterface = Frame(self.janela)
        self.frameInterface.place(relx=0.66,rely=0.05, relwidth=0.32,relheight=0.85)

    def widgets(self):
        #botoes----
        self.botao_conecta = Button(self.frameInterface,text="conectar")
        self.botao_conecta.place(relx=0.2,rely=0.1,relheight=0.05,relwidth=0.2)
        
        self.botao_desconecta = Button(self.frameInterface,text="desconectar")
        self.botao_desconecta.place(relx=0.5,rely=0.1,relheight=0.05,relwidth=0.2)
        
        self.botao_atualiza= Button(self.frameInterface,text="atualizar")
        self.botao_atualiza.place(relx=0.1,rely=0.8,relheight=0.05,relwidth=0.2)
        #botoes-----

        #labels-----
        self.label_broker=Label(self.frameInterface, text="broker: ")
        self.label_broker.place(relx=0.1,rely=0.2,relheight=0.05,relwidth=0.2)

        self.label_topico1=Label(self.frameInterface, text="topico1: ")
        self.label_topico1.place(relx=0.1,rely=0.25,relheight=0.05,relwidth=0.2)

        self.label_topico2 = Label(self.frameInterface, text="topico2: ")
        self.label_topico2.place(relx=0.1,rely=0.3,relheight=0.05,relwidth=0.2)

        self.label_medida = Label(self.frameInterface, text="_Intervalo de aquisição_")
        self.label_medida.place(relx=0.1,rely=0.75)
        #labels-----

        #caixas de texto-----
        self.ent_tempoMedida = Entry(self.frameInterface)
        self.ent_tempoMedida.place(relx=0.3,rely=0.8,relheight=0.05,relwidth=0.2)

        self.ent_broker = Entry(self.frameInterface)
        self.ent_broker.place(relx=0.29,rely=0.2,relheight=0.05,relwidth=0.5)

        self.ent_topico1 = Entry(self.frameInterface)
        self.ent_topico1.place(relx=0.29,rely=0.25,relheight=0.05,relwidth=0.5)

        self.ent_topico2 = Entry(self.frameInterface)
        self.ent_topico2.place(relx=0.29,rely=0.3,relheight=0.05,relwidth=0.5)
        #caixas de texto-----
           
        serieT = FigureCanvasTkAgg(fig, self.frameGrafico)
        serieT.get_tk_widget().pack(side=LEFT, fill=X)





a = animation.FuncAnimation(fig,atualiza,interval=1)
# janela.mainloop() 
app()








print("feito")




