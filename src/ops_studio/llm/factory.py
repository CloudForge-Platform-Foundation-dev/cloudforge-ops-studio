from typing import Dict, Type
from .base import BaseLLMProvider
from .mock import MockLLMProvider


PROVIDERS: Dict[str, Type[BaseLLMProvider]] = {}

def get_provider(name: str) -> BaseLLMProvider:    provider_class = PROVIDERS.get(name)    if not provider_class:    return provider_class()
