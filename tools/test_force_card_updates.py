"""Card selections reach the rendered board in one activity execution."""
from pathlib import Path
import sys
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from streamlit.testing.v1 import AppTest
from utils import force_motion_match_ui, force_diagram_match_ui, force_change_ui


def main():
    cases = (
        (force_motion_match_ui, "render_force_motion_match", "Force and Motion Matching", "force_motion_match", True),
        (force_diagram_match_ui, "render_force_diagram_match", "Match the Free-Body Diagram", "force_diagram_match", False),
        (force_change_ui, "render_force_change", "Change of State", "force_change", True),
    )
    for module, handler, route, prefix, multi in cases:
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / "Home.py"), default_timeout=30)
        app.session_state["practice_auto_load"] = False
        app.run()
        next(b for b in app.button if b.label == "Dynamics").click().run()
        with patch.object(module, handler, wraps=getattr(module, handler)) as executions, \
             patch.object(module, "graph_cards", wraps=module.graph_cards) as boards:
            next(b for b in app.button if b.label == route).click().run()
            qid = app.session_state[f"{prefix}_question_id"]
            selections = ([0], [0, 2], [], [3]) if multi else (0, 2, 3, 1)
            for selection in selections:
                executions.reset_mock()
                boards.reset_mock()
                app.session_state[f"{prefix}_cards_{qid}"] = {
                    "question_id": qid, "indices" if multi else "index": selection}
                app.run()
                assert not app.exception
                assert executions.call_count == boards.call_count == 1, route
                expected = tuple(selection) if multi else selection
                assert app.session_state[f"{prefix}_attempt"]["selection"] == expected
                assert boards.call_args.args[3] == selection, "board must receive current selection immediately"
                assert "practice_answer_history" not in app.session_state or not app.session_state["practice_answer_history"]
            app.session_state[f"{prefix}_cards_{qid}"] = {
                "question_id": qid - 1, "indices" if multi else "index": [] if multi else 0}
            app.run()
            assert app.session_state[f"{prefix}_attempt"]["selection"] == expected, "stale event changed a new question"
    print("Force cards passed: one execution per selection, immediate board state, deselection, stale events, and no scoring on edits.")


if __name__ == "__main__":
    main()
