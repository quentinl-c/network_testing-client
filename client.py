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
        self.__isReady = False
        self.__collaborators = []

    def register(self):
        msg = json.dumps({'id': str(self.__id)})
        response = requests.post(URL + '/registration', data=msg)
        try:
            content = json.loads(response.content)
            self.__setConfiguration(content)
            self.__appLyingConfiguration()

            if isReady:
                response = requests.post(URL + '/acknowledgement', data=msg)

        except Exception:
            print("HTTP response cannot be read")

    def __setConfiguration(self, content):
        self.exp_name = content['exp_name']
        self.nodes_nbr = content['nodes_nbr']
        self.typing_speed = content['typing_speed']
        self.duration = content['duration']
        self.browser_by_node = content['browser_by_node']
        self.target = content['target']

    def __appLyingConfiguration(self):
        for i in xrange(1, self.browser_by_node):
            collab = CollabFactory.instanciateCollaborator("writer", self.__id,
                                                           i, self.target)
            self.__collaborators.append(collab)
        self.__isReady = True

    def __startExperimentation(self):
        for c in self.__collaborators:
            c.start()
        time.sleep(self.duration)
        for c in self.__collaborators:
            c.stop()


if __name__ == '__main__':
    client = Client()
    client.register()
