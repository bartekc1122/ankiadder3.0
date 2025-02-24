from tkinter import messagebox
import logging
import traceback
from typing import Callable, Optional, TypeVar, NoReturn
import sys

log = logging.getLogger(__name__)

T = TypeVar("T")


class ErrorHandler:
    @staticmethod
    def show_error(title: str, message: str) -> None:
        log.error(f"{title}: {message}")
        messagebox.showerror(title, message)

    @staticmethod
    def show_warning(title: str, message: str) -> None:
        log.warning(f"{title}: {message}")
        messagebox.showwarning(title, message)

    @staticmethod
    def ask_retry(title: str, message: str) -> bool:
        log.info(f"Asking for retry: {title}: {message}")
        return messagebox.askyesno(title, message)

    @staticmethod
    def show_fatal_error(title: str, message: str) -> NoReturn:
        log.critical(f"FATAL ERROR - {title}: {message}")
        messagebox.showerror(
            title, f"{message}\n\nThe program will be closed after clicking OK."
        )
        sys.exit(1)

    @staticmethod
    def safe_execute(
        operation: Callable[[], T],
        error_title: str = "Operation Failed",
        allow_retry: bool = False,
        default_return: Optional[T] = None,
    ) -> Optional[T]:
        while True:
            try:
                return operation()
            except Exception as e:
                tb = traceback.format_exc()
                log.error(f"Operation failed: {str(e)}\n{tb}")

                if allow_retry:
                    retry = ErrorHandler.ask_retry(
                        error_title,
                        f"An error occured: {str(e)}\n\nWould you like to retry?",
                    )
                    if retry:
                        continue
                else:
                    ErrorHandler.show_error(error_title, f"An error occurred: {str(e)}")

                ErrorHandler.show_fatal_error("Fatal Error", "Can not preceeed!")
