#!/usr/bin/env python3
from collab_factory import CollabFactory
import requests
import time
import pika
import uuid
import json
import sys

# RabbitMQ Server
# HOST = '40.117.234.24'
HOST = '152.81.12.192'
PORT = 5672
EXCHANGE = 'broker'


class Client(object):
    """docstring for Client"""
    def __init__(self, server_address):
        self.__id = uuid.uuid4()
        self.__connection = pika.BlockingConnection(
            pika.ConnectionParameters(HOST, PORT))
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
        url = self.__server_address + '/registration'
        response = requests.post(url, data=msg)
        content = json.loads(response.text)
        if content['status'] == 'OK':
            self.__setConfiguration(content['body']['config'])
            self.__appLyingConfiguration(content['body']['role'])
            if self.__isReady:
                url = self.__server_address + '/acknowledgement'
                response = requests.post(url, data=msg)
                self.__channel.start_consuming()
        else:
            print("=== Registration failed ===")

    def __setConfiguration(self, content):
        self.exp_name = content['exp_name']
        self.writers = content['writers']
        self.readers = content['readers']
        self.typing_speed = content['typing_speed']
        self.duration = content['duration']
        self.target = content['target']

    def __appLyingConfiguration(self, role):
        self.__collab = CollabFactory.instanciateCollaborator(role,
                                                              self.target,
                                                              self.typing_speed
                                                              )
        self.__isReady = True

    def __callback(self, channel, method, properties, body):
        content = json.loads(body.decode("UTF-8"))
        if(str(content['recipient']) == self.__id or
           str(content['recipient']) == "all"):
            if str(content['body']) == "start":

                self.__startExperimentation()

    def __sendResults(self):
        msg = {'id': str(self.__id), 'payload': self.__collab.returnResults()}
        url = self.__server_address + '/saveresults'
        response = requests.post(url, data=msg)
        content = json.loads(response.text)
        if content['status'] != 'OK':
            print("=== Results are not saved ===")

    def __startExperimentation(self):
        self.__collab.start()

        time.sleep(self.duration)  # Waite the end of the experimentation

        self.__sendResults()
        self.__collab.stop()
        self.__collab.join()

        self.__channel.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Usage: %s SERVER_IP:SERVER_PORT' % sys.argv[0])

    server_adress = sys.argv[1]
    client = Client(server_address)
    client.register()
