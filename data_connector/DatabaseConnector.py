from sqlalchemy import create_engine
import pandas as pd

from data_connector.BaseDataConnector import BaseDataConnector


class DatabaseConnector(BaseDataConnector):
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.engine = None

    def connect(self):
        self.engine = create_engine(self.connection_string)

    def read_data(self, query):
        with self.engine.connect() as connection:
            return pd.read_sql(query, connection)

    def write_data(self, data, table_name):
        data.to_sql(table_name, self.engine, if_exists='append', index=False)

    def disconnect(self):
        self.engine.dispose()
