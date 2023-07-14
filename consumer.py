import pika


class RabbitMQConsumer:
    def __init__(self, callback) -> None:
        self.__host = 'localhost'
        self.__port = 5672
        self.__password = 'guest'
        self.__queue = 'data_queue'
        self.__callback = callback
        self.__channel = self.create_channel()

    def create_channel(self):
        connection_parameters = pika.ConnectionParameters(
            host=self.__host,
            port=self.__port,
            credentials=pika.PlainCredentials(
                username='guest',
                password=self.__password
            )
        )

        channel = pika.BlockingConnection(connection_parameters).channel()
        channel.queue_declare( 
            queue='data_queue',
            durable=True
        )

        channel.basic_consume(
            queue='data_queue',
            auto_ack= True,
            on_message_callback= self.__callback
        )
        return channel
    

    def start(self):
        print(f'Listen rabbitMQ on port 5672')
        self.__channel.start_consuming()


def minha_callback(ch, method, properties, body):
    print(body)


rabbitmq_consumer = RabbitMQConsumer(minha_callback)
rabbitmq_consumer.start()