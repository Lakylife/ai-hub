# aic/clients/gemini.py
import google.generativeai as genai
from typing import Optional, Generator
from .base import BaseClient


class GeminiClient(BaseClient):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        genai.configure(api_key=api_key)
        self.client = genai.GenerativeModel('gemini-pro')
    
    @property
    def model_name(self) -> str:
        return "gemini-pro"
    
    @property
    def max_tokens(self) -> int:
        return 8192
    
    def chat(self, message: str, system_prompt: Optional[str] = None) -> str:
        try:
            if system_prompt:
                full_prompt = f"{system_prompt}\n\nUser: {message}"
            else:
                full_prompt = message
            
            response = self.client.generate_content(full_prompt)
            return response.text
        
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    def chat_stream(self, message: str, system_prompt: Optional[str] = None) -> Generator[str, None, None]:
        try:
            if system_prompt:
                full_prompt = f"{system_prompt}\n\nUser: {message}"
            else:
                full_prompt = message
            
            response = self.client.generate_content(full_prompt, stream=True)
            
            for chunk in response:
                if chunk.text:
                    yield chunk.text
        
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")