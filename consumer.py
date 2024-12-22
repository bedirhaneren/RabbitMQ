import pika
import json
import time

WORKING = "working"
STOPPED = "stopped"

current_state = WORKING

def callback(ch, method, properties, body):
    
    global current_state
    if current_state == WORKING:
        received_data = json.loads(body.decode())
        print(f"Takım Numarası : ",received_data['takim_numarasi']) 
        print(f"IHA Enlem : ",received_data['iha_enlem'])
        print(f"IHA Boylam : ",received_data['iha_boylam'])
        print(f"IHA Irtifa : ",received_data['iha_irtifa'])
        print(f"IHA Dikilme : ",received_data['iha_dikilme'])
        print(f"IHA Yonelme : ",received_data['iha_yonelme'])
        print(f"IHA Yatis : ",received_data['iha_yatis'])
        print(f"Zaman Farki : ",received_data['zaman_farki'])
        print("\n\n\n")
    else:
        print("Consumer is stopped.")


def set_state(channel,new_state):
   
    global current_state
    current_state = new_state
    print(f"State changed to: {new_state.upper()}")
    channel.basic_publish(exchange='', routing_key='stateBox', body=new_state)

def start():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='messageBox')
    channel.queue_declare(queue='stateBox')

    channel.basic_consume(queue='messageBox', on_message_callback=callback, auto_ack=True)
    print(f"Initial State: {current_state.upper()}")
    print("Waiting for messages. To exit press CTRL+C or enter 'STOP' to pause.")
    try:
        while True:
            if current_state == WORKING:
                connection.process_data_events(time_limit=1)
                
            else:
                
                user_input = input("Enter 'START' to resume or CTRL+C to exit: ").strip().upper()
                
                if user_input == "START":
                    set_state(channel,WORKING)
    except KeyboardInterrupt:
        print("Exiting...")
        set_state(channel,STOPPED)
        print(current_state)
        time.sleep(2)
    finally:
        connection.close()
        print("Connection closed.")

if __name__ == '__main__' : 
    start()
