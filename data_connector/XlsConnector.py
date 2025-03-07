import os
import pandas as pd

from data_connector import BaseDataConnector


class XlsConnector(BaseDataConnector):
    def __init__(self, file_path):
        """
        Conector para arquivos .csv, .xls ou .xlsx, utilizando pandas.

        :param file_path: Caminho do arquivo a ser lido.
        """
        self.file_path = file_path
        self.data = None
        # Detecta a extensão do arquivo para decidir como carregar e salvar
        self.extension = os.path.splitext(file_path)[1].lower()

    def connect(self):
        """
        Carrega o arquivo para memória usando pandas.
        """
        if self.extension == '.csv':
            self.data = pd.read_csv(self.file_path)
        elif self.extension in ['.xls', '.xlsx']:
            self.data = pd.read_excel(self.file_path)
        else:
            raise ValueError(f"Extensão de arquivo não suportada: {self.extension}")

    def read_data(self, query=None):
        """
        Retorna os dados carregados.
        Caso queira implementar um filtro (query), pode ser feito aqui.
        """
        # Se precisar filtrar, você pode aplicar algo como:
        # return self.data.query(query) se estiver usando pandas e a query for compatível.
        return self.data

    def write_data(self, data):
        """
        Grava (ou sobrescreve) os dados de volta no arquivo,
        respeitando a extensão.

        :param data: Um DataFrame do pandas com os dados a serem salvos.
        """
        if self.extension == '.csv':
            data.to_csv(self.file_path, index=False)
        elif self.extension in ['.xls', '.xlsx']:
            data.to_excel(self.file_path, index=False)
        else:
            raise ValueError(f"Extensão de arquivo não suportada: {self.extension}")

    def disconnect(self):
        """
        Limpa da memória o DataFrame para liberar recursos.
        """
        self.data = None