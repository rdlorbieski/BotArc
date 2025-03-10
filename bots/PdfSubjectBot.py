from bots.BaseBot import BaseBot
from data_connector.PdfConnector import PdfConnector
from apis.OpenAIClient import OpenAIClient

class PdfSubjectBot(BaseBot):
    def __init__(self, config):
        super().__init__(config)
        self.pdf_connector = PdfConnector(config.pdf_path)
        self.openai_client = OpenAIClient(api_key=config.gpt_key, model="gpt-4o")
        self.chat_history = []
        self.max_history = 5

        # Conectar ao PDF apenas uma vez
        self.pdf_connector.connect()
        self.pdf_text = self.pdf_connector.read_data()
        self.pdf_connector.disconnect()

    def process_message(self, message=None):
        """Processa uma mensagem considerando o histórico de conversa."""

        try:
            if not self.pdf_text.strip():
                return "O PDF está vazio ou não contém texto extraível."

            # Adiciona a nova entrada ao histórico
            self.chat_history.append(f"Usuário: {message}")
            if len(self.chat_history) > self.max_history:
                self.chat_history.pop(0)  # Remove a conversa mais antiga

            # Criar o prompt com contexto da conversa
            historico = "\n".join(self.chat_history)
            prompt = (
                f"Este é o conteúdo de um documento PDF:\n\n{self.pdf_text[:2000]}\n\n"
                f"Histórico da conversa até agora:\n{historico}\n\n"
                f"Agora responda à última pergunta considerando o contexto."
            )

            resposta = self.openai_client.send_request(prompt=prompt)

            # Adiciona a resposta da IA ao histórico
            self.chat_history.append(f"Bot: {resposta}")

            return resposta
        except Exception as e:
            return f"Erro ao processar a mensagem: {str(e)}"

