from tkinter import simpledialog, ttk
import tkinter as tk
import logging
from events import EventManager, Event, EventDataKey, EventType
from typing import List, Optional
from config import Config

log = logging.getLogger(__name__)


class LanguageSelector:
    def __init__(
        self,
        parent: tk.Widget,
        event_manager: EventManager,
        language_list: List[str],
        current_language,
    ):
        log.info("LanguageSelector init.")
        self.event_manager = event_manager
        self.parent = parent
        self.language_list = language_list
        self.current_language = current_language
        self.language_selector_window: Optional[tk.Toplevel] = None
        self.config = Config()

    def open_window(self) -> None:
        if (
            self.language_selector_window is not None
            and self.language_selector_window.winfo_exists()
        ):
            self.language_selector_window.lift()
            return
        self.language_selector_window = tk.Toplevel(self.parent)
        self.language_selector_window.title("Wybór języka")
        self.language_selector_window.geometry("300x250")
        self.language_selector_window.register(False, False)

        self.language_selector_window.transient(self.parent)
        self.language_selector_window.grab_set()

        x = self.parent.winfo_x() + (self.parent.winfo_width() - 250) // 2
        y = self.parent.winfo_y() + (self.parent.winfo_height() - 150) // 2
        self.language_selector_window.geometry(f"+{x}+{y}")

        self.language_selector_window.protocol("WM_DELETE_WINDOW", self.on_close)

        self.create_widgets()

    def create_widgets(self) -> None:
        label = tk.Label(self.language_selector_window, text="Wybierz język:")
        label.pack(pady=(15, 5))

        self.language_combo = ttk.Combobox(
            self.language_selector_window, values=self.language_list, state="readonly"
        )
        self.language_combo.pack(padx=20, pady=10, fill=tk.X)

        if self.current_language in self.language_list:
            self.language_combo.set(self.current_language)
        else:
            self.language_combo.current(0)

        button_frame = tk.Frame(self.language_selector_window)
        button_frame.pack(fill=tk.X, padx=20, pady=15)

        ok_button = tk.Button(
            button_frame, text="OK", command=self._handle_language_change
        )
        ok_button.pack(side=tk.LEFT, padx=5)

        cancel_button = tk.Button(button_frame, text="Anuluj", command=self.on_close)
        cancel_button.pack(side=tk.RIGHT, padx=5)

    def _handle_language_change(self) -> None:
        selected_language = self.language_combo.get()

        if selected_language and selected_language != self.current_language:
            self.current_language = selected_language

            self.event_manager.emit(
                Event(
                    type=EventType.LANGUAGE_CHANGED,
                    data={EventDataKey.SELECTED_LANGUAGE: selected_language},
                )
            )

            log.info(f"Language changed to: {selected_language}")

        self.on_close()

    def on_close(self) -> None:
        if self.language_selector_window is not None:
            self.language_selector_window.destroy()
            self.language_selector_window = None
            log.info("Language selection window closed.")
