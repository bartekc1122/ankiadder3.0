from enum import Enum, auto
from dataclasses import dataclass
from typing import Any, Dict, Callable, List
import logging

log = logging.getLogger(__name__)


class EventType(Enum):
    WORD_SUBMIT_FRONT = auto()
    WORD_SUBMIT_BACK = auto()
    SENTENCE_CORRECTIONS = auto()
    ADD_FLASHCARD = auto()
    SHOW_REPOSITORY = auto()
    DELETE_WORD = auto()
    EDIT_WORD = auto()


class EventDataKey(Enum):
    WORD = auto()
    BEGINNING_WORD_CHANGED = auto()
    SENTENCE = auto()
    FRONT = auto()
    BACK = auto()
    EDIT_NEW_WORD = auto()
    EDIT_OLD_WORD = auto()


@dataclass
class Event:
    type: EventType
    data: Dict[EventDataKey, Any]


class EventManager:
    def __init__(self):
        log.info("EventManager init.")
        self._subscribers: Dict[EventType, List[Callable[[Event], None]]] = {}

    def subscribe(
        self, event_type: EventType, callback: Callable[[Event], None]
    ) -> None:
        if event_type not in self._subscribers:
            log.info(f"Adding new event type: {event_type}.")
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)
        log.info(f"{callback.__name__} subscribes {event_type}.")

    def emit(self, event: Event) -> None:
        if event.type in self._subscribers:
            for callback in self._subscribers[event.type]:
                log.info(f"Emiting {event.type} event to {callback.__name__}.")
                callback(event)
        else:
            log.error(f"Cannot emit event {event.type}, do not exists in dictionary.")
