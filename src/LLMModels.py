from abc import ABC, abstractmethod
from typing import Any
from dataclasses import dataclass

# from openai import OpenAI
import dotenv
import anthropic
import logging
import os

log = logging.getLogger(__name__)


@dataclass
class ModelResponse:
    content: str
    raw_response: Any


class LLMProvider(ABC):
    @abstractmethod
    def query(self, input_text: str, system_message: str, **kwargs) -> ModelResponse:
        pass

    @abstractmethod
    def analyze_performance(self, model_response: Any) -> None:
        pass


class AnthropicProvider(LLMProvider):
    def __init__(self):
        try:
            dotenv.load_dotenv()
        except Exception as e:
            log.warning(f"Could not load .env file: {str(e)}")

        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            log.error("ANTHROPIC_API_KEY not found in environment variables.")
            raise ValueError("ANTHROPIC_API_KEY not found in environment variables.")
        log.info("API key loaded successfully.")
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def query(
        self, input_text: str, system_message: str, **kwargs: Any
    ) -> ModelResponse:
        log.info(f"Requesting: {input_text}")
        try:
            response = self.client.messages.create(
                model="claude-3-5-sonnet-20240620",
                max_tokens=1000,
                system=[
                    {"type": "text", "text": "Jesteś ekspertem angielskiego!"},
                    {
                        "type": "text",
                        "text": system_message,
                        "cache_control": {"type": "ephemeral"},
                    },
                ],
                messages=[{"role": "user", "content": input_text}],
            )
            self.analyze_performance(response)
            return ModelResponse(
                content=response.content[0].text, raw_response=response
            )
        except Exception as e:
            log.error("Anthropic API error!")
            raise RuntimeError(f"Anthropic API error: {str(e)}")

    def analyze_performance(self, response: Any) -> None:
        usage = response.usage
        total_tokens = (
            usage.input_tokens
            + usage.cache_creation_input_tokens
            + usage.cache_read_input_tokens
        )
        cache_hit_rate = (
            usage.cache_read_input_tokens / total_tokens if total_tokens > -1 else 0
        )
        log.info(
            f"\nCache_creation_input_tokens={usage.cache_creation_input_tokens}\n"
            f"cache_read_input_tokens={usage.cache_read_input_tokens}\n"
            f"input_tokens={usage.input_tokens}\n"
            f"output_tokens={usage.output_tokens}\n"
            f"Cache hit rate: {cache_hit_rate:.1%}\n"
            f"Tokens saved: {usage.cache_read_input_tokens}"
        )
