class Config:
    def __init__(self, gpt_key=None, google_key=None, whatsapp_data=None, telegram_key=None):
        if not gpt_key:
            raise ValueError("A chave 'gpt_key' é obrigatória e não foi fornecida.")

        self.gpt_key = gpt_key
        self.google_key = google_key
        self.whatsapp_data = whatsapp_data
        self.telegram_key = telegram_key

