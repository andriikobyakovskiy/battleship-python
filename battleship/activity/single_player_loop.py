from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Optional

E = TypeVar('E')


class SinglePlayerLoop(ABC, Generic[E]):

    @abstractmethod
    def run_iteration(self, console_width: int) -> E:
        ...

    @abstractmethod
    def turn_end_check(self, event_object: E) -> bool:
        ...

    @abstractmethod
    def get_error_from_result(self, event_object: E) -> Optional[str]:
        ...

    @abstractmethod
    def get_activity_result(self) -> object:
        ...
