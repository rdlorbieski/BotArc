from bots.BaseBot import BaseBot
from data_connector.PdfConnector import PdfConnector
from apis.OpenAIClient import OpenAIClient

class PdfSubjectBot(BaseBot):
    def __init__(self, config):
        super().__init__(config)
        self.pdf_connector = PdfConnector(config.pdf_path)
        self.openai_client = OpenAIClient(api_key=config.gpt_key, model="gpt-4o")

        # Conectar ao PDF logo na inicialização
        self.pdf_connector.connect()

    def process_message(self, message=None):
        """Processa uma mensagem enviando o conteúdo do PDF para a OpenAI."""
        # Conectar ao PDF em toda mensagem nova (não tem histórico ainda!)
        self.pdf_connector.connect()
        try:
            # Verifica se a conexão foi feita corretamente
            if not self.pdf_connector.doc:
                return "❌ Erro: O PDF não foi carregado corretamente."

            pdf_text = self.pdf_connector.read_data()
            self.pdf_connector.disconnect()

            if not pdf_text.strip():
                return "O PDF está vazio ou não contém texto extraível."

            prompt = f"Este é o conteúdo de um documento PDF:\n\n{pdf_text[:2000]}\n\nCom base nisso, {message if message else 'resuma o conteúdo'}."
            resposta = self.openai_client.send_request(prompt=prompt)

            return resposta
        except Exception as e:
            return f"Erro ao processar a mensagem: {str(e)}"

