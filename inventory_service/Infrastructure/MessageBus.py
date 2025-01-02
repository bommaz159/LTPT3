import pika
import json
from UseCases.UpdateInventory import UpdateInventoryUseCase

class MessageBus:
    def __init__(self, host='rabbitmq'):
        self.host = host

    def start_listening(self):
        try:
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self.host,
                    connection_attempts=10,
                    retry_delay=5 
                )
            )
            channel = connection.channel()

            channel.queue_declare(queue='inventory_queue')

            def callback(ch, method, properties, body):
                print(f"Received message: {body}")
                message = json.loads(body)

                update_inventory_use_case = UpdateInventoryUseCase()
                update_inventory_use_case.execute(
                    product_id=message["product_id"],
                    quantity_change=-message["quantity"]
                )

            channel.basic_consume(
                queue='inventory_queue',
                on_message_callback=callback,
                auto_ack=True
            )

            print("Listening to inventory queue...")
            channel.start_consuming()
        except Exception as e:
            print(f"Failed to listen to RabbitMQ: {e}")
            raise
