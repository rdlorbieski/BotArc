import requests
import os
from dotenv import load_dotenv

load_dotenv()


class OpenAIClient:
    def __init__(self, api_key: str, model: str = "gpt-4-turbo"):
        """
        Inicializa o cliente OpenAI.

        :param api_key: Chave da API do OpenAI
        :param model: Modelo a ser usado (padrão: "gpt-4-turbo")
        """
        self.api_key = api_key
        self.model = model
        self.api_url = "https://api.openai.com/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def send_request(self, prompt: str, base64_image: str = None, max_tokens: int = 300):
        """
        Envia uma requisição para a API do OpenAI, podendo conter apenas texto ou texto + imagem.

        :param prompt: Texto enviado ao modelo.
        :param base64_image: String Base64 da imagem (opcional).
        :param max_tokens: Número máximo de tokens para a resposta.
        :return: Resposta do modelo como string.
        """
        # Construção da mensagem do usuário
        message_content = [{"type": "text", "text": prompt}]

        if base64_image:
            message_content.append({
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/png;base64,{base64_image}"
                }
            })

        # Payload para a API
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": message_content}],
            "max_tokens": max_tokens
        }

        # Enviar requisição para a API
        response = requests.post(self.api_url, headers=self.headers, json=payload)

        # Processar a resposta
        if response.status_code == 200:
            response_data = response.json()
            if 'choices' in response_data and len(response_data['choices']) > 0:
                return response_data['choices'][0]['message']['content']
            else:
                return "O retorno da API não contém escolhas válidas."
        else:
            return f"Erro {response.status_code}: {response.json()}"



# api_key = os.getenv("GPT_KEY")
# client = OpenAIClient(api_key=api_key, model="gpt-4o")
# resposta = client.send_request(prompt="Explique o funcionamento de um transformador de sentenças.")
# print(resposta)