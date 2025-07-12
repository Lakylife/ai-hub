# grok4_cli/clients/grok.py
import openai
from typing import Optional, Generator
from .base import BaseClient


class GrokClient(BaseClient):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url="https://api.x.ai/v1"
        )
    
    @property
    def model_name(self) -> str:
        return "grok-beta"
    
    @property
    def max_tokens(self) -> int:
        return 131072
    
    def chat(self, message: str, system_prompt: Optional[str] = None) -> str:
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": message})
        
        try:
            response = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            raise Exception(f"Grok API error: {str(e)}")
    
    def chat_stream(self, message: str, system_prompt: Optional[str] = None) -> Generator[str, None, None]:
        messages = []
        
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        
        messages.append({"role": "user", "content": message})
        
        try:
            stream = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=0.7,
                stream=True
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        
        except Exception as e:
            raise Exception(f"Grok API error: {str(e)}")