import pika
import pika.connection
import time
import random
import string
import json


class Data: 
    takim_numarasi = 0
    iha_enlem = 0
    iha_boylam = 0
    iha_irtifa = 0
    iha_dikilme = 0 
    iha_yonelme = 0
    iha_yatis = 0 
    zaman_farki = 0

def getData(): 
    data = Data()
    data.takim_numarasi = random.randint(1, 50)
    data.iha_enlem = random.randint(0, 1000)
    data.iha_boylam = random.randint(0, 1000)
    data.iha_irtifa = random.randint(0, 1000)
    data.iha_dikilme = random.randint(0, 500)
    data.iha_yonelme = random.randint(0, 500)
    data.iha_yatis = random.randint(0, 500)
    data.zaman_farki = random.randint(0, 50)
    return data

def dataToJson(data): 
    return json.dumps(data, default=lambda o: o.__dict__)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='messageBox')
channel.queue_declare(queue='stateBox')

current_state = "working"

def checkState(): 
    global current_state
    method, properties, body = channel.basic_get(queue='stateBox', auto_ack=True)
    if body:
        new_state = body.decode()
        if new_state != current_state:
            current_state = new_state
            print(f"State updated: {current_state}")

try:
    while True:
        checkState()  

        if current_state == "working":
            data = getData()
            iha_veri = dataToJson(data)
            channel.basic_publish(exchange='', routing_key='messageBox', body=iha_veri)
            print(f"Current State: {current_state}")
            print(f"Message sent: {iha_veri}")
            time.sleep(1)
        else:
            print(f"Current State: {current_state} - Data send stopped.")
            time.sleep(1)
except KeyboardInterrupt:
    print("Exiting producer...")
finally:
    connection.close()
    print("Connection closed.")
