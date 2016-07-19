from http_communication import HTTPCommunication
from rmq_communication import RMQCommunication
from editor import Editor
import time
import os
import uuid
import logging


logging.basicConfig(filename=__name__ + '.log', level=logging.DEBUG)
logger = logging.getLogger(__name__)


class Controller(object):
    """docstring for Controller"""
    def __init__(self):
        server_address = os.getenv('SERVER_ADDRESS', '127.0.0.1')
        rabbitmq_address = os.getenv('RABBITMQ_ADDRESS', '127.0.0.1')

        self.id = uuid.uuid4()
        self.handshake = False

        self.__http_communication = HTTPCommunication(self, server_address)
        self.__rmq_communication = RMQCommunication(self, rabbitmq_address)
        self.__duration = 0
        self.__collab = None

    def launchClient(self):
        self.__http_communication.register()

    def waitingInstructions(self):
        logger.debug("=== Waiting instructions ===")
        self.handshake = True
        self.__rmq_communication.startConsuming()

    def start(self):
        if self.handshake:
            self.__collab.start()
            time.sleep(self.__duration)

            self.__collab.getResults()
            self.__collab.kill()

    def applyingConfiguration(self, body):
        print(body)
        typing_speed = int(body['config']['typing_speed'])
        target = body['config']['target']
        word_to_type = body['word']

        self.__duration = int(body['config']['duration'])
        self.__collab = Editor(self, target, typing_speed, word_to_type)
        self.__http_communication.acknowledgeRegistration()

    def sendResults(self, results):
        self.__http_communication.sendResults(results)
