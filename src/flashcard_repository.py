import os
import logging

log = logging.getLogger(__name__)


class FlashcardRepository:
    def __init__(self, fc_path):
        self.fc_path = fc_path

    def add_flashcard(self, front, back):
        log.info("Saving new flashcard.")
        try:
            if not os.path.exists(self.fc_path):
                log.warning(f"Flashcard repository not found at {self.fc_path}!")

            with open(self.fc_path, "a", encoding="utf-8") as file:
                file.writelines(front + ";" + back + "\n")
            log.info(f"Flashcard: {front + ';' + back + '\n'}, successfully added.")
        except FileNotFoundError:
            log.error(f"File not found: {self.fc_path}!")
            return []
