import pika
import logging
import json

PORT = 5672
EXCHANGE = 'broker'


logging.basicConfig(filename=__name__ + '.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class RMQCommunication(object):
    """docstring for RMQCommunication"""
    def __init__(self, controller, rabbitmq_address):
        self.__controller = controller
        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(rabbitmq_address, PORT))
        self.__channel = self.__connection.channel()
        self.__channel.exchange_declare(exchange=EXCHANGE, type="fanout")

        result = self.__channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        self.__channel.queue_bind(exchange=EXCHANGE, queue=queue_name)
        self.__channel.basic_consume(self.__handler,
                                     queue=queue_name,
                                     no_ack=True)

    def __handler(self, channel, method, properties, body):

        content = json.loads(body.decode("UTF-8"))
        print(content)

        if(str(content['recipient']) == self.__controller.id or
           str(content['recipient']) == "all"):

            if str(content['body']) == "start":
                logger.debug("=== Experience is starting ===")
                self.__controller.start()
            else:
                logger.warning("=== Unknown messages ===")

    def startConsuming(self):
        self.__channel.start_consuming()
