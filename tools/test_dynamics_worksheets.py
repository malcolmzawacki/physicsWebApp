"""Conceptual Dynamics export coverage and independent answer checks."""
import io
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from docx import Document
from utils.worksheet_ui import CONCEPTUAL_FORCES, generate_sections, render_document
from utils import recognizing_forces as recognize, force_diagram_match as diagrams
from utils import force_motion_match as motion, force_change as change, force_ranking as ranking
from xtrct_docs.dynamics_activity_adapter import LETTERS


class DynamicsWorksheets(unittest.TestCase):
    def test_all_settings_and_answer_semantics(self):
        for activity, cls in CONCEPTUAL_FORCES.items():
            g = cls()
            for kind in g.get_problem_types():
                with self.subTest(activity=activity,kind=kind):
                    p = g.choose_problem_dict(kind,"Standard")
                    json.dumps(p)
                    spec = p["worksheet_case"]
                    self.assertTrue(p["answers"][0])
                    if g.family == "recognize":
                        case = recognize.SCENARIO_BY_ID[spec["case_id"]]
                        for index,(force,label) in enumerate(recognize.FORCE_LABELS.items()):
                            self.assertEqual(f"{chr(65+index)}: {label}" in p["answers"][0], force in case.forces)
                    elif g.family == "match":
                        case = diagrams.CASE_BY_ID[spec["case_id"]]
                        flags = [diagrams.diagram_matches(case, tuple(diagrams.ForceArrow(**a) for a in panel["data"])) for panel in spec["panels"]]
                        self.assertEqual(sum(flags),1)
                        self.assertTrue(p["answers"][0].startswith(LETTERS[flags.index(True)] + ":"))
                    elif g.family == "motion":
                        case = motion.CASE_BY_ID[spec["case_id"]]
                        options = [next(m for m in motion.MOTIONS if m.id == key) for key in spec["options"]]
                        expected = "; ".join(f"{LETTERS[i]}: {m.description(case.axis)}" for i,m in enumerate(options) if motion.compatible(case,m))
                        self.assertEqual(p["answers"][0],expected)
                    elif g.family == "change":
                        case = change.CASE_BY_ID[spec["case_id"]]
                        expected = "; ".join(LETTERS[i] for i,o in enumerate(spec["options"]) if change.accepted(case,change.ForceState(**o)))
                        self.assertTrue(p["answers"][0].startswith(expected + ":"))
                    elif g.family == "ranking":
                        quantity, comparison, masses, ties = kind.split(" / ")
                        cases = tuple(ranking.RankCase(**p["data"]) for p in spec["panels"])
                        self.assertEqual(p["answers"][0], ranking.ranking_text(ranking.expected_groups(cases,quantity,comparison)))
                        self.assertEqual(len(set(ranking.ranking_value(c,quantity,comparison) for c in cases))<4,ties=="With ties")
                    if spec["panels"]:
                        fig = g.generate_diagram(spec)
                        self.assertEqual(len(fig.axes),len(spec["panels"]))
                        fig.clear()

    def test_builder_controls_and_shortcuts(self):
        from unittest.mock import patch
        from streamlit.testing.v1 import AppTest
        from PIL import Image
        with patch("utils.worksheet_ui.libreoffice_path",return_value="soffice"), patch(
            "utils.worksheet_ui.docx_to_pdf",return_value=b"fixture"), patch(
            "utils.worksheet_ui.page_summary",return_value={"total":1,"questions":1,"answers":0}), patch(
            "utils.worksheet_ui.render_page",return_value=Image.new("RGB",(10,10),"white")):
            app=AppTest.from_string("from utils.worksheet_ui import render_forces_worksheet\nrender_forces_worksheet()",default_timeout=30).run()
            for name in CONCEPTUAL_FORCES:
                app.selectbox(key="forces_worksheet_activity").select(name).run()
                self.assertFalse(app.exception)
                self.assertFalse(any(s.label=="Worksheet difficulty" for s in app.selectbox))
                app.number_input(key="forces_worksheet_count").set_value(1).run()
                app.button(key="forces_worksheet_generate").click().run()
                self.assertFalse(app.exception)
                self.assertTrue(app.session_state["forces_worksheet_result"]["docx"].startswith(b"PK"))
            home=AppTest.from_file("Home.py",default_timeout=30).run()
            home.session_state["router_section"]="Dynamics"
            home.session_state["router_activity"]="Recognizing Forces"
            home.run()
            home.button(key="worksheet_shortcut_Recognizing Forces").click().run()
            self.assertFalse(home.exception)
            self.assertEqual(home.selectbox(key="forces_worksheet_activity").value,"Recognizing Forces")

    def test_export_and_stable_variety(self):
        for activity, cls in CONCEPTUAL_FORCES.items():
            g = cls()
            kind = g.get_problem_types()[0]
            sections = generate_sections([(activity,kind,"Standard","mixed",2)])
            before = repr(sections)
            for enabled in (False,True):
                doc = Document(io.BytesIO(render_document(sections,"Compact",True,
                    section_layouts=[("Compact",enabled,enabled,False)])))
                self.assertEqual(len(doc.inline_shapes),0 if g.family=="recognize" else 2)
                self.assertEqual(repr(sections),before)
            if g.family != "ranking":
                ids = [g.choose_problem_dict(kind,"Standard")["worksheet_case"]["case_id"] for _ in range(5)]
                self.assertEqual(len(set(ids)),5)

if __name__ == "__main__":
    unittest.main()
