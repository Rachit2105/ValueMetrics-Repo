import pika
from all_required_functions import format_data

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue= "queue")

def callback(ch, method, properties, body):
    file_path = body.decode()  
    format_data(file_path, "FormattedData.xlsx")    

channel.basic_consume(queue= "queue",
                       on_message_callback= callback,
                       auto_ack= True)

print('waiting for the message...')
channel.start_consuming()