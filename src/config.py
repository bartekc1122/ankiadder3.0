from enum import Enum, auto
from pathlib import Path
from typing import Dict

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
        self.DATABASE_PATH = Path("./data/word_database.txt")
        self.FLASHCARDS_PATH = Path("./data/anki_flashcards.txt")
        self.ICON_PATH = Path("./static/folder.png")

        self.PROMPT_PATHS: Dict[ConfigKey, Path] = {
            ConfigKey.TRANSLATION: Path("./data/prompts/translation_prompt.txt"),
            ConfigKey.SENTENCE: Path("./data/prompts/sentence_prompt.txt"),
            ConfigKey.FIND_WORD: Path("./data/prompts/find_word_prompt.txt"),
            }
        
        self.BACKGROUND_COLOR = "black"
        self.FOREGROUND_COLOR = "white"
        self.TEXT_COLOR = "white"
        self.FONT_FAMILY = "Segoe UI"
        self.FONT_SIZE_LARGE = 13
        self.FONT_SIZE_NORMAL = 11
        self.FONT_SIZE_LABEL = 14
        self.FONT_WEIGHT_BOLD = "bold"

        self.TAG_CONFIG = {
            "bold_large": {"font": (self.FONT_FAMILY, self.FONT_SIZE_LARGE, "bold")},
            "normal": {"font": (self.FONT_FAMILY, self.FONT_SIZE_NORMAL)},
            "indent": {"lmargin1": 20, "lmargin2": 20},
        }