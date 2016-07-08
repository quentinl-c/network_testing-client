import logging
import json
import requests

SERVER_PORT = 5000
HEADER = 'http://'

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class HTTPCommunication(object):
    """docstring for HTTPCommunication"""
    def __init__(self, controller, server_address):
        self.__controller = controller
        self.__server_address = ''.join((HEADER, server_address, ':',
                                         str(SERVER_PORT)))

    def register(self):
        logger.debug("=== Registration to server %s ===",
                     self.__server_address)
        msg = {'id': str(self.__controller.id)}
        path = '/registration'
        url = ''.join((self.__server_address, path))

        try:
            response = requests.post(url, data=msg)
            content = json.loads(response.text)

            if content['status'] is not None:
                if content['status'] == 'OK':
                    logger.debug("=== Registration accepted ===")
                    self.__controller.applyingConfiguration(content['body'])
                    pass
                else:
                    logger.warning("=== Registration failed ===")
            else:
                logger.warning("=== Invalid message : no status available===")
        except requests.exceptions.RequestException as ex:
            logger.exception("=== Client canno't send registration query ===")

    def acknowledgeRegistration(self):
        logger.debug("=== Acknowledgement ===")
        msg = {'id': str(self.__controller.id)}
        path = '/acknowledgement'
        url = ''.join((self.__server_address, path))

        try:
            response = requests.post(url, data=msg)
            content = json.loads(response.text)

            if content['status'] is not None:
                if content['status'] == 'OK':
                    logger.debug("=== Acknowledgement accepted ===")
                    self.__controller.waitingInstructions()
                else:
                    logger.warning("=== Acknowledgement failed ===")
            else:
                logger.warning("=== Invalid message : no status available===")

        except requests.exceptions.RequestException:
            logger.exception(
                "=== Client canno't send acknowledgment query ===")

    def sendResults(self, results):
        logger.debug("=== Results are sending ===")
        msg = {'id': str(self.__controller.id), 'payload': results}
        path = '/saveresults'
        url = ''.join((self.__server_address, path))

        try:
            response = requests.post(url, data=msg)
            content = json.loads(response.text)

            if content['status'] is not None:
                if content['status'] == 'OK':
                    logger.warning("=== Results are saved ===")
                else:
                    logger.warning("=== Results are not saved ===")
            else:
                logger.warning("=== Invalid message : no status available===")

        except requests.exceptions.RequestException:
            logger.exception(
                "=== Client canno't send acknowledgment query ===")
