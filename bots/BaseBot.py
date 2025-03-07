class BaseBot:
    def __init__(self, config):
        self.config = config

    def process_message(self, message=None):
        raise NotImplementedError("Método process_message() não implementado.")