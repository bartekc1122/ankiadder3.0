from tkinter import ttk
import tkinter as tk
import logging
from typing import List, Tuple
from config import Config

log = logging.getLogger(__name__)


class TranslationView:
    def __init__(self, parent: tk.Widget):
        self.parent = parent
        self.config = Config()
        self.frame = ttk.Frame(parent)
        self._setup_ui()
        self._configure_tags()

    def _setup_ui(self) -> None:
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(1, weight=1)

        self.word_label = ttk.Label(self.frame, text="No word selected")
        self.word_label.grid(row=0, column=0, padx=5, pady=5)

        self.frame.configure(style="Custom.TFrame")
        self.word_label.configure(style="Custom.TLabel")

        self.text_widget = tk.Text(
            self.frame,
            bg=self.config.BACKGROUND_COLOR,
            fg=self.config.FOREGROUND_COLOR,
            insertbackground=self.config.TEXT_COLOR,
            wrap="word",
        )
        self.text_widget.grid(row=1, column=0, sticky="news", padx=5, pady=5)
        self.text_widget.insert(tk.END, "No tranlsation")
        self.text_widget.config(state=tk.DISABLED)

    def word_label_change(self, word: str) -> None:
        if not word:
            log.warning("Word is empty!")
            return
        self.word_label.config(text=word)

    def translation_insert(self, parts: List[Tuple[str, str]]) -> None:
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete("1.0", tk.END)

        for tuple in parts:
            self.text_widget.insert(tk.END, f"{tuple[0]}:\n", "bold_large")
            self.text_widget.insert(tk.END, f"{tuple[1]}\n", ("normal", "indent"))
        self.text_widget.config(state=tk.DISABLED)

    def clear(self) -> None:
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.delete("1.0", tk.END)
        self.text_widget.config(state=tk.DISABLED)

    def _configure_tags(self) -> None:
        for tag, config in self.config.TAG_CONFIG.items():
            self.text_widget.tag_configure(tag, **config)

    def grid(self, **kwargs):
        self.frame.grid(**kwargs)
