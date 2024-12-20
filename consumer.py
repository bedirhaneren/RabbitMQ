import pika

WORKING = "working"
STOPPED = "stopped"

current_state = WORKING

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='messageBox')

def callback(ch, method, properties, body):
    
    
    current_state
    if current_state == WORKING:
        print(f"Received message: {body.decode()}")
    else:
        print("Consumer is stopped.")

channel.basic_consume(queue='messageBox', on_message_callback=callback, auto_ack=True)

def set_state(new_state):
   
    current_state
    current_state = new_state
    print(f"State changed to: {new_state.upper()}")

print("Waiting for messages. To exit press CTRL+C or enter 'STOP' to pause.")
try:
    while True:
        if current_state == WORKING:
            connection.process_data_events(time_limit=1)
        else:
            user_input = input("Enter 'START' to resume or CTRL+C to exit: ").strip().upper()
            if user_input == "START":
                set_state(WORKING)
except KeyboardInterrupt:
    print("Exiting...")
finally:
    connection.close()
    print("Connection closed.")
