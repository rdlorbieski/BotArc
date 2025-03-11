import sys
import os
# Adiciona o diretório raiz ao sys.path para encontrar os módulos corretamente
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bots.EquationOptmizerBot import EquationOptimizerBot
import chainlit as cl
from configs.Config import Config
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

# Configuração do bot
configs = Config(
    gpt_key=os.getenv("GPT_KEY"),
    pdf_path=os.getenv("PDF_FILE_PATH")
)

# Inicializa o bot base
#bot = PdfSubjectBot(configs)
bot = EquationOptimizerBot(configs)

@cl.on_message
async def handle_message(message: cl.Message):
    """
    Recebe uma mensagem do usuário, processa com o PdfSubjectBot e retorna a resposta.
    """
    user_input = message.content.strip()

    if user_input.lower() == "sair":
        await cl.Message(content="🚪 Saindo do chat.").send()
        return

    resposta = bot.process_message(user_input)

    await cl.Message(content=resposta).send()

# Iniciar o Chainlit
if __name__ == "__main__":
    cl.run()
