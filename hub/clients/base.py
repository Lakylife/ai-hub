# grok4_cli/clients/base.py
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List


class BaseClient(ABC):
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    @abstractmethod
    def chat(self, message: str, system_prompt: Optional[str] = None) -> str:
        pass
    
    @abstractmethod
    def chat_stream(self, message: str, system_prompt: Optional[str] = None):
        pass
    
    @property
    @abstractmethod
    def model_name(self) -> str:
        pass
    
    @property
    @abstractmethod
    def max_tokens(self) -> int:
        pass