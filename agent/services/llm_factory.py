from typing import Optional, List, Dict, Any
import os
import subprocess
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import ChatOllama
from langchain_core.language_models.chat_models import BaseChatModel
from services.vault import vault

class LLMFactory:
    """
    Factory class to instantiate and manage different LLM providers.
    Supports: OpenAI, Anthropic, Gemini, and Ollama (Local).
    """
    
    @staticmethod
    def get_model(provider: str, model_name: str, temperature: float = 0.7) -> BaseChatModel:
        # Automatic Fallback Logic
        if provider != "ollama":
            api_key = vault.get_secret(f"{provider.upper()}_API_KEY")
            if not api_key:
                print(f"[LLM] Warning: {provider} key missing. Falling back to Ollama/Llama3.")
                provider = "ollama"
                model_name = "llama3"

        if provider == "openai":
            return ChatOpenAI(model=model_name, temperature=temperature, api_key=api_key)
            
        elif provider == "anthropic":
            if not api_key: raise ValueError("Anthropic API Key not found in Vault")
            return ChatAnthropic(model=model_name, temperature=temperature, api_key=api_key)
            
        elif provider == "gemini":
            if not api_key: raise ValueError("Gemini API Key not found in Vault")
            return ChatGoogleGenerativeAI(model=model_name, temperature=temperature, google_api_key=api_key)
            
        elif provider == "ollama":
            base_url = vault.get_secret("OLLAMA_BASE_URL") or "http://localhost:11434"
            return ChatOllama(model=model_name, temperature=temperature, base_url=base_url)
            
        else:
            raise ValueError(f"Unsupported provider: {provider}")

class OllamaManager:
    """
    Manages local Ollama instances, model pulling, and status checks.
    """
    
    @staticmethod
    def is_installed() -> bool:
        try:
            subprocess.run(["ollama", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    @staticmethod
    def list_models() -> List[str]:
        if not OllamaManager.is_installed(): return []
        try:
            result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
            lines = result.stdout.strip().split('\n')[1:] # Skip header
            return [line.split()[0] for line in lines]
        except Exception as e:
            print(f"Error listing Ollama models: {e}")
            return []

    @staticmethod
    def pull_model(model_name: str):
        if not OllamaManager.is_installed():
            raise RuntimeError("Ollama is not installed")
        
        print(f"Pulling model: {model_name}...")
        process = subprocess.Popen(
            ["ollama", "pull", model_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return process

    @staticmethod
    def ensure_default_models():
        """Ensures Llama 3.2 and other defaults are present."""
        required = ["llama3.2", "llama3"] # Prioritize 3.2 as requested
        installed = OllamaManager.list_models()
        
        for model in required:
            if not any(model in m for m in installed):
                print(f"[Ollama] Auto-installing required model: {model}")
                OllamaManager.pull_model(model)

llm_factory = LLMFactory()
ollama_manager = OllamaManager()
