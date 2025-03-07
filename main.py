from Configs.config import Config
from dotenv import load_dotenv
import os

load_dotenv()
gpt_key = os.getenv("GPT_KEY")

gpt_config = Config(gpt_key=gpt_key)

print(gpt_config.gpt_key)
print("oi")