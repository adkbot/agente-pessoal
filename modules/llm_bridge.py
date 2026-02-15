import os
import google.genai as genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

class LLMBridge:
    """
    Ponte para que os módulos (Browser, Planner, Coder) possam chamar o Gemini
    diretamente para seus loops de raciocínio.
    """
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY não encontrada no .env")
        self.client = genai.Client(api_key=self.api_key)
        self.model = "gemini-2.5-flash" # Modelo disponível no ambiente do usuário

    def chat(self, prompt: str, system_instruction: str = None) -> str:
        """Envia um prompt simples e retorna a resposta texto."""
        try:
            config = types.GenerateContentConfig(
                temperature=0.7,
                system_instruction=system_instruction
            )
            
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=config
            )
            
            return response.text
        except Exception as e:
            print(f"[LLMBridge] Erro: {e}")
            return f"Erro ao chamar LLM: {e}"
