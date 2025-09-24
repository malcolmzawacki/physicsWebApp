from __future__ import annotations

from typing import Callable, Iterable, Tuple, Union
import importlib

import streamlit as st

TabLoader = Union[Callable[[], None], str]
TabSpec = Tuple[str, TabLoader]


def lazy_tabs(
    tab_specs: Iterable[TabSpec],
    *,
    state_key: str = "loaded_tabs",
    auto_load_first: bool = False,
) -> None:
    state = st.session_state.setdefault(state_key, set())

    if auto_load_first and not state:
        state.add(_tab_state_key(state_key, 1))

    labels = [label for label, _ in tab_specs]
    containers = st.tabs(labels)

    for idx, ((label, loader), container) in enumerate(zip(tab_specs, containers), start=1):
        tab_state_key = _tab_state_key(state_key, idx)
        with container:
            if tab_state_key in state:
                _resolve_loader(loader)()
            elif st.button(f"Load {label}", key=f"{tab_state_key}_button"):
                state.add(tab_state_key)
                st.rerun()


def _tab_state_key(state_key: str, index: int) -> str:
    return f"{state_key}_{index}"


def _resolve_loader(loader: TabLoader) -> Callable[[], None]:
    if callable(loader):
        return loader

    module_path, attr_name = loader.rsplit(":", 1)
    module = importlib.import_module(module_path)
    return getattr(module, attr_name)
