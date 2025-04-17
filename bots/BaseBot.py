import requests

class BaseBot:
    """
    Base class for all specialized bots.

    This class provides a foundational structure for creating different types of bots.
    It includes properties and methods required for managing conversation history,
    logging interactions, and providing default responses. Specialized bots are
    intended to inherit from this class and implement the `process_message` method
    to define their behavior.

    :ivar config: Configuration object for the bot.
    :ivar bot_name: Name of the bot.
    :ivar bot_type: Type of the bot (e.g., "generic", "specialized").
    :ivar conversation_history: Strings list to store conversation messages between users and bots.
    :ivar max_history: Maximum number of messages to retain in conversation history.
    """
    def __init__(self, config, bot_name="BaseBot", bot_type="generic", max_history=5):
        """Define a estrutura base para todos os bots especializados."""
        self.config = config
        self.bot_name = bot_name
        self.bot_type = bot_type
        self.conversation_history = []
        self.max_history = max_history  # Número máximo de mensagens no histórico

    def process_message(self, message):
        """Método abstrato que deve ser implementado pelos bots especializados."""
        raise NotImplementedError("O bot especializado deve implementar este método.")

    def store_message(self, role, message):
        """Armazena mensagens no histórico e remove as mais antigas se necessário."""
        self.conversation_history.append(f"{role}: {message}")
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)  # Remove o mais antigo para manter o tamanho máximo

    def get_conversation_history(self):
        """Retorna o histórico formatado da conversa."""
        return "\n".join(self.conversation_history)

    def clear_history(self):
        """Limpa o histórico da conversa."""
        self.conversation_history = []

    def log_activity(self, user_id, message, response):
        """Registra logs de interações para monitoramento e depuração."""
        print(f"[{user_id}] Pergunta: {message} → Resposta: {response}")

    def default_response(self):
        """Retorna uma resposta padrão caso o bot não compreenda a mensagem."""
        return "Desculpe, não entendi. Poderia reformular?"
