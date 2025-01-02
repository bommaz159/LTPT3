import pika
import json

class MessageBus:
    def __init__(self, host='rabbitmq'):
        self.host = host

    def publish(self, message: dict):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
            channel = connection.channel()

            channel.queue_declare(queue='inventory_queue')

            channel.basic_publish(
                exchange='',
                routing_key='inventory_queue',
                body=json.dumps(message)
            )

            print(f"Message sent to queue: {message}")
            channel.close()
            connection.close()
        except Exception as e:
            print(f"Failed to send message: {e}")
            raise
