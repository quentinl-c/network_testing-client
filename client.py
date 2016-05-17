#!/usr/bin/env python3
from collab_factory import CollabFactory
import requests
import pika
import uuid
import json

# RabbitMQ Server
# HOST = '40.117.234.24'
HOST = '127.0.0.1'
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
        self.__channel.exchange_declare(exchange=EXCHANGE, type="fanout")

        result = self.__channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        self.__channel.queue_bind(exchange=EXCHANGE, queue=queue_name)
        self.__channel.basic_consume(self.__callback,
                                     queue=queue_name,
                                     no_ack=True)
        self.__isReady = False
        self.__collaborators = []

    def register(self):
        msg = {'id': str(self.__id)}
        response = requests.post(URL + '/registration', data=msg)
        content = json.loads(response.text)
        if content['status'] == 'OK':
            self.__setConfiguration(content['body'])
            self.__appLyingConfiguration()
            if self.__isReady:
                print("TAGADA")
                response = requests.post(URL + '/acknowledgement', data=msg)
                self.__channel.start_consuming()
        else:
            print("HTTP ERROR")

    def __setConfiguration(self, content):
        self.exp_name = content['exp_name']
        self.nodes_nbr = content['nodes_nbr']
        self.typing_speed = content['typing_speed']
        self.duration = content['duration']
        self.browser_by_node = content['browser_by_node']
        self.target = content['target']
        print("fin de l'initialisation")

    def __appLyingConfiguration(self):
        for i in range(0, self.browser_by_node):
            collab = CollabFactory.instanciateCollaborator("writer", self.__id,
                                                           i, self.target,
                                                           self.typing_speed)
            self.__collaborators.append(collab)
        self.__isReady = True
        print("fin de l'application de la configuration")

    def __callback(self, channel, method, properties, body):
        content = json.loads(body.decode("UTF-8"))
        if(str(content['recipient']) == self.__id or
           str(content['recipient']) == "all"):
            if str(content['body']) == "start":
                self.__startExperimentation

    def __startExperimentation(self):
        for c in self.__collaborators:
            c.start()

        time.sleep(self.duration)

        for c in self.__collaborators:
            c.stop()


if __name__ == '__main__':
    print("TEST")
    client = Client()
    client.register()
