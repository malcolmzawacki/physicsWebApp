from __future__ import annotations

import importlib.util
import random
import sys
import types
from typing import Dict, List, Tuple
from pathlib import Path

# Ensure project-root imports work when running the script directly.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def _install_streamlit_stub_if_missing() -> None:
    if importlib.util.find_spec("streamlit") is not None:
        return

    stub = types.ModuleType("streamlit")

    def _noop(*args, **kwargs):
        return None

    stub.session_state = {}
    stub.pyplot = _noop
    stub.write = _noop
    stub.markdown = _noop
    stub.warning = _noop
    stub.error = _noop
    stub.info = _noop
    stub.success = _noop
    stub.caption = _noop
    stub.subheader = _noop
    stub.header = _noop
    stub.title = _noop
    stub.expander = _noop
    stub.button = _noop
    stub.columns = lambda *args, **kwargs: []
    stub.container = _noop
    stub.empty = _noop
    stub.stop = _noop
    stub.rerun = _noop
    stub.experimental_rerun = _noop
    stub.__getattr__ = lambda _name: _noop
    sys.modules["streamlit"] = stub


_install_streamlit_stub_if_missing()

import importlib
import inspect
from utils.generators.base_generator import BaseGenerator


def discover_generators():
    generators = []
    for path in sorted((PROJECT_ROOT / "utils/generators").rglob("*.py")):
        module_name = ".".join(path.relative_to(PROJECT_ROOT).with_suffix("").parts)
        module = importlib.import_module(module_name)
        for _, cls in inspect.getmembers(module, inspect.isclass):
            if cls.__module__ == module_name and cls is not BaseGenerator and issubclass(cls, BaseGenerator):
                generators.append(cls())
    return generators


from utils.problem_payload import payload_from_dict


def validate_generator(
    gen, generator_name: str, problem_types: List[str], difficulties: List[str], seeds: List[int]
) -> Tuple[int, int, List[str]]:
    """Return (total_runs, failures, messages)."""
    total = 0
    failures = 0
    messages: List[str] = []

    if not isinstance(problem_types, list) or not problem_types:
        return 0, 1, [f"{generator_name}: stored_metadata() returned no problem types"]

    for p in problem_types:
        if not isinstance(p, str) or not p.strip():
            failures += 1
            messages.append(f"{generator_name}: invalid metadata key {p!r}")
            continue
        for d in difficulties:
            for seed in seeds:
                total += 1
                try:
                    random.seed(seed)
                    result = gen.choose_problem_dict(p, d)
                    if result is None:
                        raise ValueError("choose_problem_dict returned None")
                    payload_from_dict(result)  # raises on error
                    if result.get("diagram_data") is not None:
                        import matplotlib.pyplot as plt
                        plt.close("all")
                except Exception as e:
                    failures += 1
                    messages.append(
                        f"{generator_name} [type={p} | difficulty={d} | seed={seed}]: {e}"
                    )
    return total, failures, messages


def main() -> int:
    difficulties = ["Easy", "Medium", "Hard"]
    seeds = list(range(20))

    generators = discover_generators()
    checks: Dict[str, Tuple[object, List[str]]] = {
        gen.__class__.__name__: (gen, list(gen.stored_metadata().keys()))
        for gen in generators
    }

    total = failures = 0
    all_messages: List[str] = []
    for name, (gen, ptypes) in checks.items():
        t, f, msgs = validate_generator(gen, name, ptypes, difficulties, seeds)
        total += t
        failures += f
        all_messages.extend(msgs)

    print(
        "Validated payloads (metadata-driven): "
        f"{total - failures}/{total} passed "
        f"across {len(generators)} generators, "
        f"{len(difficulties)} difficulties, {len(seeds)} seed(s)."
    )
    if failures:
        print("Failures:")
        for m in all_messages:
            print(" -", m)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
