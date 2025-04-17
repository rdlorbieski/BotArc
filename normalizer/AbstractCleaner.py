from abc import ABC, abstractmethod
from typing import TypeVar, Generic
import pandas as pd

# Definindo um TypeVar que pode ser substituído por qualquer tipo
T = TypeVar('T')

class AbstractCleaner(ABC, Generic[T]):
    @abstractmethod
    def clean(self, data: T) -> T:
        """
        Método abstrato que recebe um dado do tipo T e retorna o dado limpo.
        """
        pass