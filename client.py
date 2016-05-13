import requests
import pika
import uuid
import json

# RabbitMQ Server
HOST = '40.117.234.24'
PORT = 5672
EXCHANGE = 'broker'

# Server
URL = 'http://localhost:5000'


class Client(object):
    """docstring for Client"""
    def __init__(self):
        self.__id = uuid.uuid4()
        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(HOST, PORT))
        self.__channel = self.__connection.channel()

    def register(self):
        msg = json.dumps({'id': str(self.__id)})
        response = requests.post(URL + '/registration', data=msg)
        try:
            content = json.loads(response.content)
        except Exception, e:
            raise e
