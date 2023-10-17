
#! /usr/bin/python3
from paho.mqtt import client as mqtt_client

broker='192.168.1.45'
port=1883
topic="mesa"
client_id="interfaceGenericaTelemetria"


def connect_mqtt() -> mqtt_client: 
    def on_connect(client,userdata, flags, rc):
        if rc ==0:
            print("Conexao com o broker feita com sucesso!")
        else:
            print("Nao foi possivel estabelecer conexao com o broker")
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.connect(broker,port)
    return client
def subscribe(client: mqtt_client):
    def on_message(client,userdata,msg):
        print(f"Recebida `{msg.payload.decode()}` from `{msg.topic}` topic")
        with open("log.txt", "a") as arquivo:
            arquivo.write(msg.payload.decode())
            arquivo.write("\n")
    client.subscribe(topic)
    client.on_message = on_message

def run():
    client=connect_mqtt()
    subscribe(client)
    client.loop_forever()

run()