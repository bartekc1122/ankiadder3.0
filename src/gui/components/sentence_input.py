from tkinter import ttk
import tkinter as tk
from events import EventType, EventDataKey, EventManager, Event
from typing import Tuple
from config import Config


class SentenceInput:
    def __init__(self, parent: tk.Widget, event_manager: EventManager):
        self.parent = parent
        self.event_manager = event_manager
        self.config = Config()
        self.frame = ttk.Frame(parent)
        self._setup_grid()
        self._setup_ui()

    def _setup_grid(self):
        self.frame.grid_columnconfigure(0, weight=1)

        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_rowconfigure(1, weight=1)
        self.frame.grid_rowconfigure(2, weight=1)
        self.frame.grid_rowconfigure(3, weight=1)
        self.frame.grid_rowconfigure(5, weight=1)
        self.frame.grid_rowconfigure(4, weight=1)

    def _setup_ui(self) -> None:
        self.my_sentence_label = ttk.Label(self.frame)
        self.front_label = ttk.Label(self.frame)
        self.back_label = ttk.Label(self.frame)

        self.my_sentence_entry = ttk.Entry(self.frame)
        self.front_entry = ttk.Entry(self.frame)
        self.back_entry = ttk.Entry(self.frame)

        self.my_sentence_label.config(text="My Sentence:")
        self.front_label.config(text="Front:")
        self.back_label.config(text="Back:")

        self.my_sentence_label.grid(row=0, padx=5, pady=5)
        self.my_sentence_entry.grid(row=1, sticky="news", padx=5, pady=5)

        self.front_label.grid(row=2, padx=5, pady=5)
        self.front_entry.grid(row=3, sticky="news", padx=5, pady=5)

        self.back_label.grid(row=4, padx=5, pady=5)
        self.back_entry.grid(row=5, sticky="news", padx=5, pady=5)

        self.my_sentence_label.configure(style="Custom.TLabel")
        self.front_label.configure(style="Custom.TLabel")
        self.back_label.configure(style="Custom.TLabel")
        self.frame.configure(style="Custom.TFrame")

    def front_insert(self, text: str) -> None:
        self.front_entry.delete(0, tk.END)
        self.front_entry.insert(0, text)

    def back_insert(self, text: str) -> None:
        self.back_entry.delete(0, tk.END)
        self.back_entry.insert(0, text)

    def delete_my_sentence(self) -> None:
        self.my_sentence_entry.delete(0, tk.END)

    def delete_front_back(self) -> None:
        self.front_entry.delete(0, tk.END)
        self.back_entry.delete(0, tk.END)

    def get_front_back(self) -> Tuple[str, str]:
        return (self.front_entry.get(), self.back_entry.get())

    def _handle_sentence_corrctions(self) -> None:
        sentence = self.my_sentence_entry.get()
        self.event_manager.emit(
            Event(
                type=EventType.SENTENCE_CORRECTIONS,
                data={EventDataKey.SENTENCE: sentence},
            )
        )

    def _handle_add_flashcard(self) -> None:
        (front, back) = self.get_front_back()
        self.event_manager.emit(
            Event(
                type=EventType.ADD_FLASHCARD,
                data={EventDataKey.FRONT: front, EventDataKey.BACK: back},
            )
        )
        self.delete_front_back()
        self.delete_my_sentence()

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)
