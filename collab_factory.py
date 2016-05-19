from reader import Reader
from writer import Writer


class CollabFactory(object):
    @staticmethod
    def instanciateCollaborator(collaborator, client_id, rk, url,
                                typing_speed):
        if collaborator == 'r':
            return Reader(client_id, rk, url, typing_speed)
        else:
            return Writer(client_id, rk, url, typing_speed)
