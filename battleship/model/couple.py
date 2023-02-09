from __future__ import annotations

from typing import List, Dict, Generic, TypeVar, Callable, Tuple

T = TypeVar('T')


class Couple(Generic[T]):

    def __init__(self, data: Dict[str, T]):
        self._data = data.copy()
        keys = list(self._data.keys())
        self._current_key = keys[0]
        self._another_key = keys[1]

    def keys(self) -> List[str]:
        return [self._current_key, self._another_key]

    def values(self) -> List[T]:
        return [self.current_value, self.another_value]

    def items(self) -> List[Tuple[str, T]]:
        return [
            (self._current_key, self.current_value),
            (self._another_key, self.another_value),
        ]

    @property
    def current_item(self) -> (str, T):
        return self._current_key, self._data[self._current_key]

    @property
    def current_key(self) -> str:
        return self._current_key

    @property
    def another_key(self) -> str:
        return self._another_key

    @property
    def current_value(self) -> T:
        return self._data[self._current_key]

    @property
    def another_value(self) -> T:
        return self._data[self._another_key]

    def switch_current(self):
        (self._current_key, self._another_key) = (self._another_key, self._current_key)

    def set_current(self, key: str):
        if key not in self._data:
            raise KeyError(f"No value for key {key}")

        self._another_key = self._current_key
        self._current_key = key

    def map_values(self, func: Callable) -> Couple:
        return Couple({
            self._current_key: func(self.current_value),
            self._another_key: func(self.another_value),
        })
