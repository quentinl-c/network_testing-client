from reader import Reader
from writer import Writer


class CollabFactory(object):
    @staticmethod
    def instanciateCollaborator(collaborator, url,
                                typing_speed):
        if collaborator == 'r':
            return Reader(url, typing_speed)
        else:
            return Writer(url, typing_speed)
