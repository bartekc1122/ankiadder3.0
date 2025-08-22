from enum import Enum, auto
from pathlib import Path
from typing import Dict
import os


class ConfigKey(Enum):
    TRANSLATION = auto()
    SENTENCE = auto()
    FIND_WORD = auto()


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance

    def _initialize(self):
        self.languages = ["English", "German", "Russian"]
        self.current_language = self.languages[0]

        self._relative_language_path = Path(f"./data/{self.current_language}")

        self.DATABASE_PATH = Path.joinpath(self._relative_language_path, "word_database.txt")
        self.FLASHCARDS_PATH = Path.joinpath(self._relative_language_path, "anki_flashcards.txt")
        self.ICON_PATH = Path("./static/folder.png")


        self.PROMPT_PATHS: Dict[ConfigKey, Path] = {
            ConfigKey.TRANSLATION: Path.joinpath(self._relative_language_path, "prompts/translation_prompt.txt"),
            ConfigKey.SENTENCE: Path.joinpath(self._relative_language_path, "prompts/sentence_prompt.txt"),
            ConfigKey.FIND_WORD: Path.joinpath(self._relative_language_path,"prompts/find_word_prompt.txt"),
        }

        self.BACKGROUND_COLOR = "white"
        self.FOREGROUND_COLOR = "black"
        self.TEXT_COLOR = "black"
        self.FONT_FAMILY = "Segoe UI"
        self.FONT_SIZE_LARGE = 12
        self.FONT_SIZE_NORMAL = 10
        self.FONT_SIZE_LABEL = 12
        self.FONT_WEIGHT_BOLD = "bold"

        self.TAG_CONFIG = {
            "bold_large": {"font": (self.FONT_FAMILY, self.FONT_SIZE_LARGE, "bold")},
            "normal": {"font": (self.FONT_FAMILY, self.FONT_SIZE_NORMAL)},
            "indent": {"lmargin1": 20, "lmargin2": 20},
        }


    def refresh_paths(self):
        self._relative_language_path = Path(f"./data/{self.current_language}")
        self.DATABASE_PATH = Path.joinpath(self._relative_language_path, "word_database.txt")
        self.FLASHCARDS_PATH = Path.joinpath(self._relative_language_path, "anki_flashcards.txt")

        self.PROMPT_PATHS = {
            ConfigKey.TRANSLATION: Path.joinpath(self._relative_language_path, "prompts/translation_prompt.txt"),
            ConfigKey.SENTENCE: Path.joinpath(self._relative_language_path, "prompts/sentence_prompt.txt"),
            ConfigKey.FIND_WORD: Path.joinpath(self._relative_language_path,"prompts/find_word_prompt.txt"),
        }
