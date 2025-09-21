from __future__ import annotations

import streamlit as st
from typing import Any


class State:
    """
    Small helper around Streamlit session_state to reduce stringly-typed key bugs.
    Keys are always namespaced with the provided prefix.
    """

    def __init__(self, prefix: str) -> None:
        self.prefix = prefix

    def key(self, name: str) -> str:
        return f"{self.prefix}_{name}"

    def has(self, name: str) -> bool:
        return self.key(name) in st.session_state

    def get(self, name: str, default: Any = None) -> Any:
        return st.session_state.get(self.key(name), default)

    def set(self, name: str, value: Any) -> None:
        st.session_state[self.key(name)] = value

    def ensure(self, name: str, default: Any) -> None:
        if not self.has(name):
            self.set(name, default)

    def inc(self, name: str, delta: int = 1) -> int:
        value = int(self.get(name, 0)) + delta
        self.set(name, value)
        return value

    def pop(self, name: str) -> None:
        """Remove a namespaced key from session_state if present."""
        key = self.key(name)
        if key in st.session_state:
            del st.session_state[key]

    def ensure_lazy(self, name: str, factory: callable) -> None:
        """
        Ensure a namespaced key exists, computing its default lazily via factory().

        Unlike ensure(name, default), this only calls factory if the key is absent,
        avoiding unintended side effects from eager evaluation.
        """
        if not self.has(name):
            self.set(name, factory())
