import pika
import pika.connection
import time
import random
import string

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='messageBox')

while(1) : 
        length = random.randint(5, 15)  
        random_message = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        channel.basic_publish(exchange='', routing_key='messageBox', body=random_message)
        print(f"Message sent: {random_message} ")
        time.sleep(1)
connection.close()
