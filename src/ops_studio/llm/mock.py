from typing import List
from .base import BaseLLMProvider, LLMMessage, LLMResponse


class MockLLMProvider(BaseLLMProvider):
    async def generate(self, messages):

    async def generate_with_tools(self, messages, tools):
