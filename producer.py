import pika , json

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue="queue")

data = {
        "file_path" : "AMCdata.csv",
        "save_file_path" : "FormattedData.xlsx"

}

channel.basic_publish(exchange="",
                      routing_key="queue",
                      body=json.dumps(data))

print('Message sent')
connection.close()

