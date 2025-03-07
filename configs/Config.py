class Config:
    def __init__(self, gpt_key=None, pdf_path=None, google_key=None):
        """
        Configuração do bot.

        :param pdf_path: Caminho do arquivo PDF.
        :param gpt_key: Chave da API do OpenAI.
        :param google_key: Chave da API do Google.
        """
        if not gpt_key:
            raise ValueError("A chave 'gpt_key' é obrigatória e não foi fornecida.")

        self.gpt_key = gpt_key
        self.pdf_path = pdf_path
        self.google_key = google_key

