import tkinter as tk
from tkinter import ttk
import logging
from events import EventManager
from config import Config

from gui.components.word_input import WordInput
from gui.components.translation_view import TranslationView
from gui.components.sentence_input import SentenceInput
from gui.components.flashcard_creator import FlashcardCreator
from gui.components.repository import Repository
from gui.components.language_selector import LanguageSelector

log = logging.getLogger(__name__)


class MainWindow:
    def __init__(self, event_manager: EventManager):
        log.info("MainWindow init.")
        self.config = Config()

        self.root = tk.Tk()
        self.root.config(background=self.config.BACKGROUND_COLOR)
        self.root.title("AnkiAdder 3.0")
        self.root.geometry("1000x650")
        self.event_manager = event_manager
        self.configure_styles()
        self._setup_grid()
        self._init_components()
        self._setup_key_bindings()

    def configure_styles(self):
        style = ttk.Style()
        style.configure("Custom.TFrame", background=self.config.BACKGROUND_COLOR)
        style.configure(
            "Custom.TLabel",
            background=self.config.BACKGROUND_COLOR,
            foreground=self.config.TEXT_COLOR,
            font=(self.config.FONT_FAMILY, self.config.FONT_SIZE_LABEL, "bold"),
        )
        style.configure(
            "Custom.TButton",
            background=self.config.BACKGROUND_COLOR,
            foreground=self.config.TEXT_COLOR,
        )

    def _setup_grid(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

    def _init_components(self):
        self.word_input = WordInput(self.root, self.event_manager)
        self.word_input.grid(row=0, column=1, sticky="news", padx=5, pady=5)

        self.translation_view = TranslationView(self.root)
        self.translation_view.grid(
            row=0, column=0, rowspan=3, sticky="news", padx=5, pady=5
        )

        self.sentence_input = SentenceInput(self.root, self.event_manager)
        self.sentence_input.grid(row=1, column=1, sticky="news", padx=5, pady=5)

        self.flashcard_creator = FlashcardCreator(self.root)
        self.flashcard_creator.grid(row=2, column=1, sticky="news", padx=5, pady=5)

        self.repository_window = Repository(self.root, self.event_manager)

        self.language_change = LanguageSelector(
            self.root,
            self.event_manager,
            self.config.languages,
            self.config.current_language,
        )

    def _setup_key_bindings(self):
        # Input word entry, adding word to the back
        self.word_input.entry.bind(
            "<Return>", lambda event: self.word_input._handle_push_back()
        )

        self.sentence_input.my_sentence_entry.bind(
            "<Return>", lambda event: self.sentence_input._handle_sentence_corrections()
        )

        self.sentence_input.my_sentence_entry.bind(
            "<Up>", lambda event: self.sentence_input._handle_add_flashcard()
        )

        self.sentence_input.front_entry.bind(
            "<Up>", lambda event: self.sentence_input._handle_add_flashcard()
        )

        self.sentence_input.back_entry.bind(
            "<Up>", lambda event: self.sentence_input._handle_add_flashcard()
        )

        self.root.bind("<KeyPress-/>", lambda event: self.language_change.open_window())
