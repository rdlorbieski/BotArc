from bots.BaseBot import BaseBot
from data_connector.PdfConnector import PdfConnector
from apis.OpenAIClient import OpenAIClient

class PdfSubjectBot(BaseBot):
    def __init__(self, config, connector, pre_processor=None):
        """Inicializa o bot especializado em responder com base em um PDF."""
        super().__init__(config, bot_name="PdfSubjectBot", bot_type="pdf_analysis", max_history=5)
        self.pdf_connector = connector
        self.pre_processor = pre_processor  # Define o pre_processor antes de chamar load_pdf
        self.openai_client = OpenAIClient(api_key=config.gpt_key, model="gpt-4o")
        self.pdf_text = self.load_pdf()

    def load_pdf(self):
        """Lê e armazena o conteúdo do PDF."""
        try:
            self.pdf_connector.connect()
            pdf_text = self.pdf_connector.read_data()
            if self.pre_processor:
                print("Usando pre_processor para limpar o texto do PDF.")
                pdf_text = self.pre_processor.clean(pdf_text)  # Usa o pre_processor se estiver definido
            self.pdf_connector.disconnect()
            return pdf_text if pdf_text.strip() else "O PDF está vazio ou não contém texto extraível."
        except Exception as e:
            return f"Erro ao carregar o PDF: {str(e)}"

    def process_message(self, message=None):
        """Processa uma mensagem considerando o histórico de conversa e o PDF."""
        try:
            if not self.pdf_text or self.pdf_text.startswith("Erro ao carregar"):
                return self.pdf_text  # Retorna o erro se não conseguiu carregar o PDF

            # Armazena a mensagem do usuário no histórico
            self.store_message("Usuário", message)

            # Criar o prompt com contexto da conversa
            historico = self.get_conversation_history()
            prompt = (
                f"Este é um documento PDF:\n\n{self.pdf_text[:2000]}\n\n"
                f"Histórico da conversa:\n{historico}\n\n"
                f"Agora responda à última pergunta considerando o contexto."
            )

            # Envia a requisição para OpenAI
            resposta = self.openai_client.send_request(prompt=prompt)

            # Armazena a resposta no histórico
            self.store_message("Bot", resposta)

            return resposta
        except Exception as e:
            return f"Erro ao processar a mensagem: {str(e)}"
