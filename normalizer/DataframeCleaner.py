from normalizer.AbstractCleaner import AbstractCleaner
import pandas as pd

class DataframeCleaner(AbstractCleaner[pd.DataFrame]):
    def __init__(self, column_to_remove: str):
        self.column_to_remove = column_to_remove

    def clean(self, data: pd.DataFrame) -> pd.DataFrame:
        if self.column_to_remove in data.columns:
            data = data.drop(columns=[self.column_to_remove])
        return data