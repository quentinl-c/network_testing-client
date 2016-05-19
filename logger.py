class Logger(object):
    """docstring for Logger"""
    def __init__(self, role):
        self.role = role
        self.__buffer = []

    def bufferize(self, content):
        self.__buffer.append(role + ' ' + content)

    def genResult(self):
        return '\n'.join(self.__buffer)
