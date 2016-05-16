from reader import Reader
from writer import Writer


class CollabFactory(object):
    @staticmethod
    def instanciateCollaborator(collaborator, client_id, rg, url):
        if collaborator == "Reader":
            return Reader(client_id, rg, url)
        else:
            return Writer(client_id, rg, url)
