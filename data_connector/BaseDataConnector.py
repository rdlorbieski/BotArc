from abc import ABC, abstractmethod

class BaseDataConnector(ABC):
    @abstractmethod
    def connect(self):
        """Estabelece a conexão ou carrega os dados."""
        pass

    @abstractmethod
    def read_data(self, query=None):
        """Retorna os dados com base em uma consulta ou critério."""
        pass

    @abstractmethod
    def write_data(self, data):
        """Grava ou atualiza os dados na fonte."""
        pass

    @abstractmethod
    def disconnect(self):
        """Fecha a conexão ou libera os recursos utilizados."""
        pass
