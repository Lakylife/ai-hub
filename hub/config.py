# grok4_cli/config.py
import os
import yaml
from typing import Optional, Dict, Any
from pathlib import Path


class Config:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or self._get_default_config_path()
        self._config_data = self._load_config()
    
    def _get_default_config_path(self) -> str:
        home_dir = Path.home()
        config_dir = home_dir / ".ai-hub"
        config_dir.mkdir(exist_ok=True)
        return str(config_dir / "config.yaml")
    
    def _load_config(self) -> Dict[str, Any]:
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    return yaml.safe_load(f) or {}
            except Exception as e:
                print(f"Warning: Could not load config file {self.config_path}: {e}")
                return {}
        return {}
    
    def save_config(self):
        try:
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            with open(self.config_path, 'w') as f:
                yaml.safe_dump(self._config_data, f, default_flow_style=False)
        except Exception as e:
            print(f"Error saving config file: {e}")
    
    @property
    def grok_api_key(self) -> Optional[str]:
        return (
            os.environ.get("GROK_API_KEY") or
            os.environ.get("XAI_API_KEY") or
            self._config_data.get("grok_api_key")
        )
    
    @property
    def claude_api_key(self) -> Optional[str]:
        return (
            os.environ.get("ANTHROPIC_API_KEY") or
            self._config_data.get("claude_api_key")
        )
    
    @property
    def gemini_api_key(self) -> Optional[str]:
        return (
            os.environ.get("GEMINI_API_KEY") or
            os.environ.get("GOOGLE_API_KEY") or
            self._config_data.get("gemini_api_key")
        )
    
    @property
    def openai_api_key(self) -> Optional[str]:
        return (
            os.environ.get("OPENAI_API_KEY") or
            self._config_data.get("openai_api_key")
        )
    
    @property
    def default_model(self) -> str:
        return self._config_data.get("default_model", "grok")
    
    @property
    def max_tokens(self) -> int:
        return self._config_data.get("max_tokens", 8192)
    
    @property
    def temperature(self) -> float:
        return self._config_data.get("temperature", 0.7)
    
    @property
    def system_prompt(self) -> Optional[str]:
        return self._config_data.get("system_prompt")
    
    def set_grok_api_key(self, key: str):
        self._config_data["grok_api_key"] = key
        self.save_config()
    
    def set_claude_api_key(self, key: str):
        self._config_data["claude_api_key"] = key
        self.save_config()
    
    def set_gemini_api_key(self, key: str):
        self._config_data["gemini_api_key"] = key
        self.save_config()
    
    def set_openai_api_key(self, key: str):
        self._config_data["openai_api_key"] = key
        self.save_config()
    
    def set_default_model(self, model: str):
        self._config_data["default_model"] = model
        self.save_config()
    
    def set_system_prompt(self, prompt: str):
        self._config_data["system_prompt"] = prompt
        self.save_config()