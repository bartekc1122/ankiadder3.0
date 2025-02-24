from tkinter import ttk
import tkinter as tk
from events import EventManager, Event, EventDataKey, EventType
import logging
from config import Config

log = logging.getLogger(__name__)


class WordInput:
    def __init__(self, parent: tk.Widget, event_manager: EventManager):
        log.info("WordInput init.")

        self.event_manager = event_manager
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.config = Config()
        self._setup_ui()

    def _setup_ui(self) -> None:
        self.frame.grid_columnconfigure(0, weight=3)
        self.frame.grid_columnconfigure(1, weight=1)
        self.frame.grid_columnconfigure(2, weight=1)
        self.frame.grid_columnconfigure(3, weight=1)

        self.entry = ttk.Entry(self.frame)
        self.entry.grid(row=0, column=0, sticky="news", padx=5, pady=5)

        self.push_front_button = ttk.Button(
            self.frame,
            text="Push Front",
            command=self._handle_push_front,
        )
        self.push_front_button.grid(row=0, column=1, sticky="news", padx=5, pady=5)

        self.word_count = ttk.Label(self.frame, text="0")
        self.word_count.grid(row=0, column=2, padx=5, pady=5)

        self.icon = tk.PhotoImage(file=self.config.ICON_PATH)
        self.icon_button = tk.Button(self.frame)
        self.icon_button.config(
            image=self.icon,
            command=lambda: self._handle_show_database(),
        )
        self.icon_button.grid(row=0, column=3, sticky="news", padx=5, pady=5)

    def _handle_push_front(self) -> None:
        word = self.entry.get()
        self.event_manager.emit(
            Event(type=EventType.WORD_SUBMIT_FRONT, data={EventDataKey.WORD: word})
        )
        self.entry.delete(0, tk.END)

    def _handle_push_back(self) -> None:
        word = self.entry.get()
        self.event_manager.emit(
            Event(type=EventType.WORD_SUBMIT_BACK, data={EventDataKey.WORD: word})
        )
        self.entry.delete(0, tk.END)

    def _handle_show_database(self) -> None:
        self.event_manager.emit(Event(type=EventType.SHOW_REPOSITORY, data=[]))

    def clear_entry(self) -> None:
        self.entry.delete(0, tk.END)

    def set_word_count(self, count: int) -> None:
        self.word_count.config(text=count)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)
