#!/usr/bin/env python3
from collab_factory import CollabFactory
from writer import Writer
import requests
import time
import pika
import uuid
import json
import os

# RabbitMQ Server
PORT = 5672
EXCHANGE = 'broker'
SERVER_PORT = 5000
HEADER = 'http://'


class Client(object):
    """docstring for Client"""
    def __init__(self, server_address, rabbitmq_address):
        self.__id = uuid.uuid4()
        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(rabbitmq_address, PORT))
        self.__channel = self.__connection.channel()
        self.__channel.exchange_declare(exchange=EXCHANGE, type="fanout")
        self.__server_address = server_address

        result = self.__channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        self.__channel.queue_bind(exchange=EXCHANGE, queue=queue_name)
        self.__channel.basic_consume(self.__callback,
                                     queue=queue_name,
                                     no_ack=True)
        self.__isReady = False
        self.__collab = None

    def register(self):
        msg = {'id': str(self.__id)}
        seq_url = (HEADER, self.__server_address, ':', str(SERVER_PORT),
                   '/registration')
        url = ''.join(seq_url)
        response = requests.post(url, data=msg)
        print(response)
        content = json.loads(response.text)
        if content['status'] == 'OK':
            self.__setConfiguration(content['body']['config'])
            self.__appLyingConfiguration(content['body'])
            if self.__isReady:
                seq_url = (HEADER, self.__server_address, ':',
                           str(SERVER_PORT), '/acknowledgement')
                url = ''.join(seq_url)
                response = requests.post(url, data=msg)
                self.__channel.start_consuming()
        else:
            print("=== Registration failed ===")

    def __setConfiguration(self, content):
        self.writers = int(content['writers'])
        self.readers = int(content['readers'])
        self.typing_speed = int(content['typing_speed'])
        self.duration = int(content['duration'])
        self.target = content['target']

    def __appLyingConfiguration(self, body):
        self.__collab = CollabFactory.instanciateCollaborator(body['role'],
                                                              self.target,
                                                              self.typing_speed
                                                              )
        if isinstance(self.__collab, Writer):
            self.__collab.__word_to_type = body['word']
        self.__isReady = True

    def __callback(self, channel, method, properties, body):
        content = json.loads(body.decode("UTF-8"))
        if(str(content['recipient']) == self.__id or
           str(content['recipient']) == "all"):
            if str(content['body']) == "start":

                self.__startExperimentation()

    def __sendResults(self):
        msg = {'id': str(self.__id), 'payload': self.__collab.returnResults()}
        seq_url = (HEADER, self.__server_address, ':', str(SERVER_PORT),
                   '/saveresults')
        url = ''.join(seq_url)
        response = requests.post(url, data=msg)
        content = json.loads(response.text)
        if content['status'] != 'OK':
            print("=== Results are not saved ===")

    def __startExperimentation(self):
        self.__collab.start()

        time.sleep(self.duration)  # Waiting the end of the experimentation

        self.__sendResults()
        self.__collab.stop()
        self.__collab.join()

        self.__channel.close()


if __name__ == '__main__':

    server_address = os.getenv('SERVER_ADDRESS', '127.0.0.1')
    rabbitmq_address = os.getenv('RABBITMQ_ADDRESS', '127.0.0.1')
    client = Client(server_address, rabbitmq_address)
    client.register()
