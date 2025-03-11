from normalizer.AbstractCleaner import AbstractCleaner


class TextCleaner(AbstractCleaner[str]):
    def clean(self, data: str) -> str:
        # Exemplo simples: converter para minúsculas e remover espaços extras
        data = data.lower().strip()
        return " ".join(data.split())