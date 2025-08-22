from gui.main_window import MainWindow
from events import EventManager, Event, EventDataKey, EventType
from word_repository import WordRepository
from flashcard_repository import FlashcardRepository
from config import Config
import logging
from queris import Query, ResponseField
import os

log = logging.getLogger(__name__)


class AnkiAdder:
    def __init__(self):
        log.info("AnkiAdder init.")
        self.config = Config()
        if self.config.GOOGLE_DRIVE_ACTIVATION == True:
            log.info("Activation of google drive")
            self._google_drive_activatoin()
        self.event_manager = EventManager()
        self.main_window = MainWindow(self.event_manager)
        self.word_repository = WordRepository(self.config.DATABASE_PATH)
        self.flashcard_repository = FlashcardRepository(self.config.FLASHCARDS_PATH)
        self.query = Query()

        # True - translation will be done on initialization
        # False - will not do translation on initialization(saves tokens)
        self.refresh_gui(False)

        self._setup_events_handlers()
        self.main_window.root.mainloop()

    def _google_drive_activatoin(self) -> None:
        try:
            if not os.path.exists(self.config.GOOGLE_DRIVE_PATH):
                log.error(f"Error: path {self.config.GOOGLE_DRIVE_PATH} do not exsists")
                return 
            if not os.path.isdir(self.config.GOOGLE_DRIVE_PATH):
                log.error(f"Error: Path '{self.config.GOOGLE_DRIVE_PATH}' is not a directory.")
                return 
            content = os.listdir(self.config.GOOGLE_DRIVE_PATH)
            log.info(f"Google Drive activated. Found {len(content)} items in the root directory.")
            return
        except OSError as e:
            log.error(f"Failed to activate Google Drive. Error: {e}")
            log.error("Please ensure the drive is correctly mounted and you have permissions.")
            return 
        except Exception as e:
            log.error(f"An unexpected error occurred during drive activation: {e}")
            return 

    def _setup_events_handlers(self) -> None:
        self.event_manager.subscribe(
            EventType.WORD_SUBMIT_FRONT, self._handle_word_submit_front
        )
        self.event_manager.subscribe(
            EventType.WORD_SUBMIT_BACK, self._handle_word_submit_back
        )
        self.event_manager.subscribe(
            EventType.SENTENCE_CORRECTIONS, self._handle_get_sentence_corrections
        )
        self.event_manager.subscribe(
            EventType.ADD_FLASHCARD, self._handle_add_flashcard
        )
        self.event_manager.subscribe(
            EventType.SHOW_REPOSITORY, self._handle_show_repository
        )
        self.event_manager.subscribe(
            EventType.DELETE_WORD, self._handle_repository_delete
        )
        self.event_manager.subscribe(EventType.EDIT_WORD, self._handle_repository_edit)
        self.event_manager.subscribe(
            EventType.LANGUAGE_CHANGED, self._handle_language_change
        )

    def _handle_language_change(self, event: Event) -> None:
        log.debug("Changing language")
        new_language = event.data.get(EventDataKey.SELECTED_LANGUAGE)
        if new_language not in self.config.languages:
            log.error(f"There is no language {new_language} in the list")
            return
        self.word_repository.save_words()
        self.word_repository.words.clear()
        self.config.current_language = new_language
        self.config.refresh_paths()
        self.word_repository.db_path = self.config.DATABASE_PATH
        self.flashcard_repository.fc_path = self.config.FLASHCARDS_PATH
        self.query.load_messages_from_file()
        self.word_repository.load_words()
        self.refresh_gui(beginning_word_changed=True)
        log.info("Language changed and gui refreshed")

    def _handle_word_submit_front(self, event: Event) -> None:
        log.debug("Word submit front")
        word = event.data.get(EventDataKey.WORD)
        if not word:
            log.warning("Word is empty!")
            return
        beginning_word_changed = self.word_repository.push_front(word)
        self.refresh_gui(beginning_word_changed)

    def _handle_word_submit_back(self, event: Event) -> None:
        log.debug("Word submit back")
        word = event.data.get(EventDataKey.WORD)
        if not word:
            log.warning("Word is empty!")
            return
        beginning_word_changed = self.word_repository.push_back(word)
        self.refresh_gui(beginning_word_changed)

    def _handle_get_sentence_corrections(self, event: Event) -> None:
        sentence = event.data.get(EventDataKey.SENTENCE)
        if not sentence:
            log.warning("Sentence is empty!")
            return
        top_word = self.word_repository.get_top_word()
        if not top_word:
            log.error("No top word")
            return
        log.debug("Getting sentence corrections")
        sentence_corrections = self.query.get_sentence_corrections(sentence)

        self.main_window.flashcard_creator.corrections_insert(
            sentence_corrections.parts
        )
        log.debug("Creating flashcard")
        query_response = self.query.get_flashcard(
            sentence_corrections.data[ResponseField.SENTENCE], top_word
        )
        log.debug("Inserting flashcard")
        self.main_window.sentence_input.front_insert(
            query_response.data[ResponseField.FRONT]
        )
        self.main_window.sentence_input.back_insert(
            query_response.data[ResponseField.BACK]
        )

    def _handle_add_flashcard(self, event: Event) -> None:
        log.info("Add flashcard.")
        front = event.data.get(EventDataKey.FRONT)
        back = event.data.get(EventDataKey.BACK)

        if not front or not back:
            log.error(f"No front or back of the flashcard. Front: {front}, back:{back}")

        self.flashcard_repository.add_flashcard(front, back)
        top_word = self.word_repository.get_top_word()
        beginning_word_changed = self.word_repository.delete_word(top_word)
        self.refresh_gui(beginning_word_changed)
        self.main_window.flashcard_creator.clear()

    def get_new_translation(self) -> None:
        log.info("Getting new translation")
        word = self.word_repository.get_top_word()
        if not word:
            log.warning("No word to translate")
            self.main_window.translation_view.clear()
            self.main_window.translation_view.word_label_change("No words added")
            self.main_window.sentence_input.delete_front_back()
            self.main_window.flashcard_creator.clear()
            return

        self.main_window.translation_view.word_label_change(word)
        query_response = self.query.get_word_translation(word)
        self.main_window.translation_view.translation_insert(query_response.parts)

    def _handle_show_repository(self, event: Event) -> None:
        log.debug("Show repository.")
        self.main_window.repository_window.open_window(self.word_repository.words)

    def _handle_repository_delete(self, event: Event) -> None:
        log.debug("Repository delete.")
        word = event.data.get(EventDataKey.WORD)
        beginning_word_changed = self.word_repository.delete_word(word)
        self.refresh_gui(beginning_word_changed)

    def _handle_repository_edit(self, event: Event) -> None:
        log.debug("Repository edit.")
        old_word = event.data.get(EventDataKey.EDIT_OLD_WORD)
        new_word = event.data.get(EventDataKey.EDIT_NEW_WORD)
        beginning_word_changed = self.word_repository.edit_word(old_word, new_word)
        self.refresh_gui(beginning_word_changed)

    def refresh_gui(self, beginning_word_changed: bool = False) -> None:
        log.debug("Refresh gui.")
        self.main_window.repository_window.reload_list(self.word_repository.words)
        self.main_window.word_input.set_word_count(
            self.word_repository.get_word_count()
        )
        if beginning_word_changed:
            self.get_new_translation()
