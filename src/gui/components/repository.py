from tkinter import simpledialog
import tkinter as tk
import logging
from events import EventManager, Event, EventDataKey, EventType
from typing import List
from config import Config

log = logging.getLogger(__name__)


class Repository:
    def __init__(self, parent: tk.Widget, event_manager: EventManager):
        log.info("Repository init.")
        self.event_manager = event_manager
        self.parent = parent
        self.repository_window: tk.Toplevel = None
        self.word_list = []
        self.config = Config()

    def open_window(self, word_list: List[str]) -> None:
        if self.repository_window is not None and self.repository_window.winfo_exists():
            self.repository_window.lift()
            return

        self.word_list = word_list
        self.repository_window = tk.Toplevel(self.parent)
        self.repository_window.title("Repository")
        self.repository_window.geometry("230x400")
        self.repository_window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.create_widgets()

    def create_widgets(self) -> None:
        self.list_frame = tk.Frame(self.repository_window)
        self.list_frame.pack(fill=tk.BOTH, expand=True)

        self.word_listbox = tk.Listbox(self.list_frame)
        self.word_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.reload_list(self.word_list)

        self.button_frame = tk.Frame(self.repository_window)
        self.button_frame.pack(fil=tk.X, padx=10, pady=10)

        self.delete_button = tk.Button(
            self.button_frame, text="Delete", command=self._handle_delete_word
        )
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.edit_button = tk.Button(
            self.button_frame, text="Edit", command=self._handle_edit_word
        )
        self.edit_button.pack(side=tk.LEFT, padx=5)

    def _handle_delete_word(self) -> None:
        selected_index = self.word_listbox.curselection()
        if selected_index:
            selected_word = self.word_listbox.get(selected_index)
        self.event_manager.emit(
            Event(type=EventType.DELETE_WORD, data={EventDataKey.WORD: selected_word})
        )

    def _handle_edit_word(self) -> None:
        selected_index = self.word_listbox.curselection()
        if selected_index:
            selected_word = self.word_listbox.get(selected_index)
            new_word = simpledialog.askstring(
                "Edit Word", "Enter new word:", initialvalue=selected_word
            )
            if new_word:
                self.event_manager.emit(
                    Event(
                        type=EventType.EDIT_WORD,
                        data={
                            EventDataKey.EDIT_OLD_WORD: selected_word,
                            EventDataKey.EDIT_NEW_WORD: new_word,
                        },
                    )
                )

    def reload_list(self, word_list: List[str]) -> None:
        if self.repository_window is None or not self.repository_window.winfo_exists():
            log.debug("Repository winodw is not opne, Skipping reload.")
            return
        self.word_listbox.delete(0, tk.END)
        for word in self.word_list:
            self.word_listbox.insert(tk.END, word)
        log.info("List reloaded in the repository window.")

    def on_close(self) -> None:
        self.repository_window.destroy()
        self.repository_window = None
        log.info("Repository window colsed.")
