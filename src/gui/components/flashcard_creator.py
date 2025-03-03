from tkinter import ttk
import tkinter as tk
from typing import List, Tuple
from config import Config


class FlashcardCreator:
    def __init__(self, parent: tk.Widget):
        self.parent = parent
        self.config = Config()
        self.frame = ttk.Frame(parent)
        self.frame.configure(style="Custom.TFrame")
        self._setup_ui()
        self._configure_tags()

    def _setup_ui(self) -> None:
        self.frame.grid_columnconfigure(0, weight=1)
        self.frame.grid_rowconfigure(0, weight=1)

        self.text_widget = tk.Text(
            self.frame,
            bg=self.config.BACKGROUND_COLOR,
            fg=self.config.FOREGROUND_COLOR,
            insertbackground=self.config.TEXT_COLOR,
            wrap="word",
        )
        self.text_widget.grid(row=0, column=0, sticky="news", padx=5, pady=5)
        self.text_widget.insert(tk.END, "No instractions")
        self.text_widget.config(state=tk.DISABLED)

    def corrections_insert(self, parts: List[Tuple[str, str]]) -> None:
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
