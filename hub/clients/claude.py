# grok4_cli/clients/claude.py
import anthropic
from typing import Optional, Generator
from .base import BaseClient


class ClaudeClient(BaseClient):
    def __init__(self, api_key: str):
        super().__init__(api_key)
        self.client = anthropic.Anthropic(api_key=api_key)
    
    @property
    def model_name(self) -> str:
        return "claude-3-5-sonnet-20241022"
    
    @property
    def max_tokens(self) -> int:
        return 8192
    
    def chat(self, message: str, system_prompt: Optional[str] = None) -> str:
        try:
            response = self.client.messages.create(
                model=self.model_name,
                max_tokens=self.max_tokens,
                system=system_prompt or "You are a helpful AI assistant.",
                messages=[
                    {"role": "user", "content": message}
                ]
            )
            
            return response.content[0].text
        
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")
    
    def chat_stream(self, message: str, system_prompt: Optional[str] = None) -> Generator[str, None, None]:
        try:
            with self.client.messages.stream(
                model=self.model_name,
                max_tokens=self.max_tokens,
                system=system_prompt or "You are a helpful AI assistant.",
                messages=[
                    {"role": "user", "content": message}
                ]
            ) as stream:
                for text in stream.text_stream:
                    yield text
        
        except Exception as e:
            raise Exception(f"Claude API error: {str(e)}")