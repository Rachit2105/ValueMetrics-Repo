import pika , json
from all_required_functions import format_data

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue= "queue")

def callback(ch, method, properties, body):
    data = json.loads(body)
    file_path = data["file_path"]
    save_file_path = data["save_file_path"]
    format_data(file_path, save_file_path)    

channel.basic_consume(queue= "queue",
                       on_message_callback= callback,
                       auto_ack= True)

print('waiting for the message...')
channel.start_consuming()
print('File has been Formatted')
