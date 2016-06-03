class Logger(object):
    """docstring for Logger"""
    def __init__(self):
        self.__buffer = []

    def bufferize(self, role, content):
        self.__buffer.append(role + ' ' + content)

    def genResult(self):
        return '\n'.join(self.__buffer)
