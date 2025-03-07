from bots.PdfSubjectBot import PdfSubjectBot
from configs.Config import Config
from dotenv import load_dotenv
import os
load_dotenv()


if __name__ == '__main__':
    configs = Config(gpt_key=os.getenv("GPT_KEY"), pdf_path=os.getenv("PDF_FILE_PATH"))
    print(configs.pdf_path)
    bot = PdfSubjectBot(configs)
    print("\n💬 PDF Subject Bot iniciado!")
    print("Digite uma pergunta sobre o PDF ou 'sair' para encerrar.\n")

    while True:
        user_input = input("📝 Pergunta: ")

        if user_input.lower() == "sair":
            print("🚪 Saindo do bot.")
            break

        resposta = bot.process_message(user_input)
        print(f"\n🤖 Resposta: {resposta}\n")