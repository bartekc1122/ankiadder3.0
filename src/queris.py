from config import Config, ConfigKey
from pathlib import Path
import logging
from typing import Dict, List, Tuple, Any
from LLMModels import AnthropicProvider
from formatter import Formatter
from error_handler import ErrorHandler
from enum import Enum
from dataclasses import dataclass

log = logging.getLogger(__name__)


class ResponseField(Enum):
    IS_WORD_CORRECT = "is_word_correct"
    SENTENCE = "Zdanie"
    POLISH_SENTENCE = "Tłumaczenie zdania"
    FRONT = "Zdanie"
    BACK = "Wyraz"


@dataclass
class QueryResponse:
    parts: List[Tuple[str, str]]
    data: Dict[ResponseField, Any]


class Query:
    def __init__(self):
        self.config = Config()
        self.prompts: Dict[str, str] = {}
        self.translation_prompt: str
        self.sentence_prompt: str
        self.find_word_prompt: str
        self.lmm = AnthropicProvider()
        self.formatter = Formatter()
        self.error_handler = ErrorHandler()

        success = self.load_messages_from_file()
        if not success:
            ErrorHandler.show_fatal_error(
                "Fatal Error", "Can not load required prompts, can not preceed"
            )

    def load_messages_from_file(self) -> bool:
        try:
            for prompt_name, path in self.config.PROMPT_PATHS.items():
                prompt_path = Path(path)

                if not prompt_path.exists():
                    log.error(f"Prompt file not found: {prompt_path}")
                    continue

                try:
                    with open(prompt_path, "r", encoding="utf-8") as file:
                        self.prompts[prompt_name] = file.read()
                        log.info(f"Successfully loaded prompt: {prompt_name}")
                except Exception as e:
                    log.error(f"Cannot read {prompt_name} prompt: {str(e)}")
                    continue

            missing_prompts = set(self.config.PROMPT_PATHS.keys()) - set(
                self.prompts.keys()
            )
            if missing_prompts:
                log.error(f"Failed to load prompts: {missing_prompts}")
                raise FileNotFoundError(f"Missing required prompts: {missing_prompts}")

            self.translation_prompt = self.prompts[ConfigKey.TRANSLATION]
            self.sentence_prompt = self.prompts[ConfigKey.SENTENCE]
            self.find_word_prompt = self.prompts[ConfigKey.FIND_WORD]
            return True
        except Exception as e:
            log.error(f"Error loading prompts: {str(e)}")
            ErrorHandler.show_error(
                "Configuration Error", f"Missing required prompts: {missing_prompts}"
            )
            return False

    def _get_translation_impl(self, word: str) -> QueryResponse:
        model_response = self.lmm.query(word, self.translation_prompt)
        translation_parts = self.formatter.get_formatted_text(model_response.content)

        fields = self.special_field_finder(
            translation_parts, [ResponseField.IS_WORD_CORRECT]
        )

        data: Dict[ResponseField, Any] = {}
        if ResponseField.IS_WORD_CORRECT in fields:
            log.debug(f"There is '{ResponseField.IS_WORD_CORRECT} in fields'")
            for i, (key, value) in enumerate(translation_parts):
                if key == ResponseField.IS_WORD_CORRECT.value:
                    translation_parts.pop(i)
                    log.debug(
                        "Removed validation element 'is_word_correct' from result."
                    )
                    if not value == "ok":
                        data = {ResponseField.IS_WORD_CORRECT.value: value}
                        translation_parts.append(("Czy chodziło o", value))
                    break
        return QueryResponse(parts=translation_parts, data=data)

    def _get_sentence_corrections(self, sentence: str) -> QueryResponse:
        model_response = self.lmm.query(sentence, self.sentence_prompt)
        translation_parts = self.formatter.get_formatted_text(model_response.content)

        fields = self.special_field_finder(
            translation_parts,
            [ResponseField.SENTENCE, ResponseField.POLISH_SENTENCE],
        )
        return QueryResponse(parts=translation_parts, data=fields)

    def _get_flashcard(self, english: str, word: str) -> QueryResponse:
        model_response = self.lmm.query(f"{english}:{word}", self.find_word_prompt)
        translation_parts = self.formatter.get_formatted_text(model_response.content)

        fields = self.special_field_finder(
            translation_parts, [ResponseField.FRONT, ResponseField.BACK]
        )
        log.debug(f"parts: {translation_parts}, data: {fields}")
        return QueryResponse(parts=translation_parts, data=fields)

    def get_word_translation(self, word: str) -> QueryResponse:
        log.debug("Safe execution of get word translaniton")
        return ErrorHandler.safe_execute(
            operation=lambda: self._get_translation_impl(word),
            error_title=f"Word Translation Error for '{word}'",
            allow_retry=True,
            default_return=[],
        )

    def get_sentence_corrections(self, sentence: str) -> QueryResponse:
        log.debug("Safe execution of get sentence corrections")
        return ErrorHandler.safe_execute(
            operation=lambda: self._get_sentence_corrections(sentence),
            error_title=f"Sentence Translation Error for '{sentence}'",
            allow_retry=True,
            default_return=[],
        )

    def get_flashcard(self, english: str, word: str) -> QueryResponse:
        log.debug("Safe execution of get falshcard")
        return ErrorHandler.safe_execute(
            operation=lambda: self._get_flashcard(english, word),
            error_title=f"Flashcard Query Error for '{english}: {word}'",
            allow_retry=True,
            default_return=[],
        )

    def special_field_finder(
        self, parts: List[Tuple[str, str]], seek_list: List[ResponseField]
    ) -> Dict[ResponseField, str]:
        find_dict: Dict[ResponseField, str] = {}
        for key, value in parts:
            for field in seek_list:
                if field.value == key:
                    find_dict[field] = value
                    log.debug(f"Found key {field}, adding to dict")
        return find_dict
