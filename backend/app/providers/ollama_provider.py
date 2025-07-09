import ollama
from typing import List
from app.schemas.chat import ChatMessage, ChatResponse
from app.core.config import settings
from app.protocols.i_ollama_provider import IOllamaProvider


class OllamaProvider(IOllamaProvider):
    def __init__(
        self, 
        temperature: float = 0.7
    ):
        self.model = settings.OLLAMA_MODEL
        self.temperature = temperature
        self.num_predict = settings.OLLAMA_NUM_PREDICT
        self.ollama_host = settings.OLLAMA_HOST
        self.client = ollama.Client(host=self.ollama_host)
    
    def process_chat_message(self, message: str, history: List[ChatMessage] = None) -> ChatResponse:
        if history is None:
            history = []
        
        history.append(ChatMessage(role="user", content=message))
        
        try:
            response = self.client.chat(
                model=self.model,
                messages=history,
                options={"temperature": self.temperature, "num_predict": self.num_predict}
            )
            
            bot_reply = response['message']['content']
            history.append(ChatMessage(role="assistant", content=bot_reply))
            
            return ChatResponse(
                response=bot_reply,
                updated_history=history
            )
        except Exception as e:
            print(f"Error connecting to Ollama: {e}")
            raise e