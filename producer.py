import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue="queue")

channel.basic_publish(exchange="",
                      routing_key="queue",
                      body="AMCdata.csv")

print('Message sent')
connection.close()

