from __future__ import annotations

from utils.ui_state import State


class StateProxy:
    def __init__(self, prefix: str):
        self._state = State(prefix)

    def __getattr__(self, name: str):
        return self._state.get(name)

    def __setattr__(self, name: str, value):
        if name == "_state":
            object.__setattr__(self, name, value)
        else:
            self._state.set(name, value)

    def __contains__(self, name: str) -> bool:
        return self._state.has(name)

    def get(self, name: str, default=None):
        return self._state.get(name, default)

    def set(self, name: str, value):
        self._state.set(name, value)

    def inc(self, name: str, delta: int = 1) -> int:
        return self._state.inc(name, delta)
