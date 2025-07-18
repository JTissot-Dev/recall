from fastapi import Depends
from typing import Annotated
from app.protocols.i_ollama_provider import IOllamaProvider
from app.providers.ollama_provider import OllamaProvider


def get_ollama_provider(temperature: float = 0.7) -> IOllamaProvider:
    """
    Factory function to create an instance of OllamaProvider.
    """
    return OllamaProvider(temperature=temperature)

OllamaProviderDep = Annotated[IOllamaProvider, Depends(get_ollama_provider)]