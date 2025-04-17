import os
import google.generativeai as genai
from dotenv import load_dotenv


class GeminiClient:
    def __init__(self, model: str = "gemini-1.5-flash"):
        """
        Inicializa o cliente Gemini da Google.

        :param model: Nome do modelo a ser utilizado (padrão: gemini-1.5-pro)
        """
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("A chave da API (GEMINI_API_KEY) não foi encontrada no .env.")

        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)

    def send_request(self, prompt: str) -> str:
        """
        Envia um prompt de texto ao modelo Gemini.

        :param prompt: Pergunta ou conteúdo textual a ser enviado.
        :return: Resposta gerada pelo modelo.
        """
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            return f"Erro ao gerar conteúdo: {str(e)}"


    def send_pdf(self, pdf_path: str, prompt: str) -> str:
        """
        Envia um arquivo PDF junto com um prompt para o modelo Gemini.

        :param pdf_path: Caminho para o arquivo PDF.
        :param prompt: Pergunta ou comando relacionado ao conteúdo do PDF.
        :return: Resposta gerada pelo modelo.
        """
        try:
            with open(pdf_path, "rb") as f:
                pdf_data = f.read()

            contents = [
                {
                    "mime_type": "application/pdf",
                    "data": pdf_data
                },
                prompt
            ]

            response = self.model.generate_content(contents)
            return response.text.strip()
        except Exception as e:
            return f"Erro ao processar o PDF: {str(e)}"

if __name__ == "__main__":
    cliente = GeminiClient()

    resposta = cliente.send_pdf(
        pdf_path="../data_files/artigo_temas.pdf",
        prompt="Qual o tema principal deste pdf?"
    )

    print(resposta)