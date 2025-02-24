import os
from typing import List, Optional
import logging

log = logging.getLogger(__name__)


class WordRepository:
    def __init__(self, db_path: str):
        log.info("WordRepository init.")
        self.db_path = db_path
        self.words: List[str] = []
        self.load_words()

    def load_words(self) -> None:
        log.info(f"Loading words to repository: {self.db_path}")
        if not os.path.exists(self.db_path):
            log.warning(f"Database file not found at {self.db_path}!")
        try:
            with open(self.db_path, "r", encoding="utf-8") as file:
                for line in file:
                    if not line.strip():  # Empty line detect
                        continue
                    self.words.append(line.strip())
            log.debug(self.words)
            log.info("Words loaded successfully.")
        except FileNotFoundError:
            log.warning(f"File not found {self.db_path}, returing empty array.")
            return []

    def save_words(self) -> None:
        log.info(f"Saving words from repository to {self.db_path}.")
        try:
            if not os.path.exists(self.db_path):
                log.warning(f"Database file not found at {self.db_path}!")

            with open(self.db_path, "w", encoding="utf-8") as file:
                log.debug(self.words)
                for word in self.words:
                    file.write(word + "\n")
            log.info("Words saved successfully.")

        except Exception as exception:
            log.warning(f"Failed to save words, {str(exception)}")

    def push_back(self, word: str) -> bool:
        if not word:
            log.error("Word is empty, cannot add to the array!")
            return

        word = word.strip()

        log.info(f"Pushing back {word}.")
        if self.words:
            beginning_word_changed = False
            self.words.append(word)
        else:
            log.info(f"Array is empty, adding {word}.")
            beginning_word_changed = True
            self.words.insert(0, word)

        self.save_words()
        log.info(
            f"Word pushed back successfully. Beginning word changed: {beginning_word_changed}"
        )
        return beginning_word_changed

    def push_front(self, word: str) -> bool:
        if not word:
            log.error("Word is empty, cannot add to the array!")
            return

        word = word.strip()

        log.info(f"Pushing front {word}.")
        beginning_word_changed = True
        self.words.insert(0, word)

        self.save_words()
        log.info(
            f"Word pushed front successfully. Beginning word changed: {beginning_word_changed}"
        )
        return beginning_word_changed

    def delete_word(self, word: str) -> bool:
        word = word.strip()
        if word not in self.words:
            log.error(f"Cannot find: {word} in the arrary to delete!")
            return

        # There must be at least one word in words bc there is word to delete in the array
        beginning_word_changed = self.words[0] == word

        self.words.remove(word)
        self.save_words()

        log.info(
            f"Word {word} deleted successfully. Beginning word changed: {beginning_word_changed}"
        )
        return beginning_word_changed

    def edit_word(self, old_word: str, new_word: str) -> bool:
        old_word = old_word.strip()
        new_word = new_word.strip()

        if not old_word or not new_word:
            log.error("Old word or new word is empty, cannot edit!")
            return False

        if old_word not in self.words:
            log.error(f"Cannot find {old_word} in the array to edit!")
            return False

        beginning_word_changed = self.words[0] == old_word

        index = self.words.index(old_word)
        self.words[index] = new_word

        self.save_words()
        log.info(
            f"Word {old_word} edited to {new_word} successfully. Beginning word changed: {beginning_word_changed}"
        )
        return beginning_word_changed

    def get_top_word(self) -> Optional[str]:
        log.info(f"Getting the top word: {self.words[0] if self.words else None}")
        return self.words[0] if self.words else None

    def get_word_count(self) -> int:
        return len(self.words)
