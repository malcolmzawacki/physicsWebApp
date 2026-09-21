"""End-to-end target requests: generator, browser lifecycle, and DOCX export."""
import ast
import io
import json
import logging
import random
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
logging.disable(logging.CRITICAL)
from docx import Document
from streamlit.testing.v1 import AppTest
from tools.validate_payloads import discover_generators
from utils.solve_for import target_options, generate_selected, _catalog
from utils.problem_payload import payload_from_dict
from utils.solve_for_custom import OhmsLawTargets
from xtrct_docs.payload_adapter import DocumentGenerator
from xtrct_docs.document_creator import create_doc


class SolveForTests(unittest.TestCase):
    def test_all_declared_targets_and_export_requests(self):
        combinations = 0
        generators = [*discover_generators(), OhmsLawTargets()]
        for generator in generators:
            name = type(generator).__name__
            sections = []
            for kind in _catalog().get(name, {}):
                for difficulty in ("Easy", "Medium", "Hard"):
                    options = target_options(generator, kind, difficulty)
                    self.assertEqual(len(options), len({o['id'] for o in options}))
                    for option in options:
                        with self.subTest(generator=name, kind=kind, difficulty=difficulty, target=option):
                            for seed in range(5):
                                random.seed(seed)
                                problem = generate_selected(generator, kind, difficulty, option['id'])
                                payload_from_dict(problem)
                                self.assertEqual(problem['extras']['requested_target_id'], option['id'])
                            # Same seed/request must generate identical text/answers in both consumers.
                            random.seed(81)
                            direct = generate_selected(generator, kind, difficulty, option['id'])
                            random.seed(81)
                            exported = DocumentGenerator(generator).question(kind, difficulty, option['id'])
                            for field in ('question', 'answers', 'units', 'extras'):
                                self.assertEqual(direct[field], exported[field])
                            # Retain figures for dedicated export checks; this sweep verifies text/math.
                            exported.pop('diagram_data', None)
                            sections.append({'heading': option['label'], 'gap': 0, 'problems': [exported]})
                            combinations += 1
            if sections:
                buffer = io.BytesIO()
                create_doc(name, lambda: sections, 1, output_path=buffer, open_document=False, include_graphs=False)
                buffer.seek(0)
                self.assertTrue(Document(buffer).tables)
        self.assertGreater(combinations, 500)
        print(f"Checked {combinations} target combinations with five seeds and DOCX serialization.")

    def test_invalid_and_restricted_targets_fail(self):
        from utils.generators.energy.energy_basics import EnergyBasicsGenerator
        generator = EnergyBasicsGenerator()
        mass = next(o['id'] for o in target_options(generator, 'Kinetic Energy', 'Hard') if o['label'] == 'Mass')
        with self.assertRaises(ValueError):
            generate_selected(generator, 'Kinetic Energy', 'Easy', mass)
        with self.assertRaises(ValueError):
            generate_selected(generator, 'Kinetic Energy', 'Hard', 'invented')
        with self.assertRaises(ValueError):
            DocumentGenerator(generator).question('Kinetic Energy', 'Easy', mass)

    def test_targets_select_the_correct_physical_unknown(self):
        from utils.generators.force_generator import ForceGenerator
        from utils.generators.energy.energy_basics import EnergyBasicsGenerator
        from utils.generators.waves_generator import WaveGenerator
        cases = [
            (ForceGenerator(), "Newton's Second Law", 'Easy', 'numbers', (4, 3, 12, .2, 20),
             {'Object acceleration': [3], 'Net Force on Object': [12], 'Object mass': [4]}),
            (ForceGenerator(), "Newton's Second Law", 'Hard', 'numbers', (4, 3, 12, .2, 20),
             {'Net Force and coefficient of friction': [12, .2], 'Net Force and acceleration': [12, 3], 'Net Force and Applied Force': [12, 20]}),
            (EnergyBasicsGenerator(), 'Kinetic Energy', 'Hard', 'kinetic_energy', (4, 5, 50),
             {'Kinetic Energy': [50], 'Velocity': [5], 'Mass': [4]}),
        ]
        for generator, kind, level, method, values, expected in cases:
            with patch.object(generator, method, return_value=values):
                for option in target_options(generator, kind, level):
                    self.assertEqual(generate_selected(generator, kind, level, option['id'])['answers'], expected[option['label']])
        generator = WaveGenerator()
        for option in target_options(generator, 'Wave Properties', 'Easy'):
            with patch('utils.generators.waves_generator.ri', side_effect=[4, 5]):
                result = generate_selected(generator, 'Wave Properties', 'Easy', option['id'])
            self.assertEqual(result['answers'], [{'Wave Speed':20, 'Wavelength':5, 'Frequency':4}[option['label']]])

    def test_custom_stoichiometry_targets_and_export(self):
        import runpy
        from utils.solve_for_custom import StoichiometryTargets
        factory = runpy.run_path(str(ROOT/'app_pages/1_Chem-_Stoichiometry.py'))['generate_stoichiometry_problem']
        generator = StoichiometryTargets(factory, 'Combustion')
        for option in target_options(generator, 'Product amount', 'Medium'):
            for seed in range(5):
                random.seed(seed)
                result = DocumentGenerator(generator).question('Product amount', 'Medium', option['id'])
                payload_from_dict(result)
                self.assertEqual(result['units'], ['mol' if option['id']=='gram-to-mole' else 'g'])
            buffer = io.BytesIO()
            create_doc('Chemistry', DocumentGenerator(generator).section('Conversions', 'Product amount', 'Medium', option['id']),
                       1, output_path=buffer, open_document=False)
            buffer.seek(0)
            self.assertTrue(Document(buffer).tables)

    def test_relative_unknown_is_withheld_in_prompt_and_diagram(self):
        from utils.generators.kinematics.relative_motion_generator import RelativeMotionGenerator
        generator = RelativeMotionGenerator()
        for kind in generator.TYPES:
            for difficulty in generator.DIFFICULTIES:
                for option in target_options(generator, kind, difficulty):
                    problem = generate_selected(generator, kind, difficulty, option['id'])
                    case, target = problem['extras']['case'], problem['extras']['solve_for']
                    if target == 'result':
                        continue
                    link = case['links'][target]
                    self.assertIn(f"{link['subject']} relative to {link['reference']}: **? m/s**", problem['question'])
                    hidden = [row for row in problem['diagram_data'] if row['value'] is None]
                    self.assertEqual(len(hidden), 1)
                    known = sum(row['velocity'] * row['coefficient'] for i, row in enumerate(case['links']) if i != target)
                    self.assertAlmostEqual((case['relative_velocity'] - known) / link['coefficient'], problem['answers'][0])
                    if kind == 'Combined':
                        self.assertNotEqual(link['subject'], 'water')

    def test_ohm_targets_withhold_requested_given(self):
        from utils.generators.current_electricity.ohms_law_model import build_circuit_case
        for option in target_options(OhmsLawTargets(), 'Single Resistor', 'Easy'):
            random.seed(17)
            problem = generate_selected(OhmsLawTargets(), 'Single Resistor', 'Easy', option['id'])
            case = problem['extras']['case']
            self.assertEqual(case['answer_label'], option['label'])
            self.assertNotIn(option['label'], [label for label, _ in case['givens']])
            labels = [case['diagram']['source_label'], case['diagram']['wire_label'], *case['diagram']['resistor_labels']]
            self.assertEqual(sum('?' in label for label in labels), 1)
        with self.assertRaises(ValueError):
            build_circuit_case('Single Resistor', 'Easy', 'invalid')

    def test_standard_selector_refresh_reset_and_new_question(self):
        app = AppTest.from_string('''
from utils.ui import Interface
from utils.generators.energy.energy_basics import EnergyBasicsGenerator
Interface('target_test','Energy',EnergyBasicsGenerator(),None,['Easy','Medium','Hard']).unified_smart_layout()
''', default_timeout=20).run()
        self.assertFalse(app.exception)
        self.assertFalse(any(w.label == 'Solve for' for w in app.selectbox))
        app.selectbox(key='target_test_difficulty_select_unified').select('Hard').run()
        from utils.generators.energy.energy_basics import EnergyBasicsGenerator
        option = next(o for o in target_options(EnergyBasicsGenerator(), 'Elastic Potential Energy', 'Hard') if o['label'] == 'Spring Strength')
        app.selectbox(key='target_test_solve_for_select').select(option['id']).run()
        self.assertFalse(app.exception)
        self.assertIn('Spring Strength', app.session_state['target_test_units'][0])
        question_id = app.session_state['target_test_question_id']
        app.run()
        self.assertEqual(question_id, app.session_state['target_test_question_id'])
        next(b for b in app.button if b.label == 'New Question').click().run()
        self.assertGreater(app.session_state['target_test_question_id'], question_id)
        self.assertIn('Spring Strength', app.session_state['target_test_units'][0])
        app.selectbox(key='target_test_difficulty_select_unified').select('Easy').run()
        self.assertFalse(app.exception)
        self.assertIn('Elastic Potential Energy', app.session_state['target_test_units'][0])
        self.assertFalse(app.session_state['target_test_submitted'])

    def test_inventory_covers_every_route(self):
        tree = ast.parse((ROOT/'Home.py').read_text(encoding='utf-8'))
        routes = ast.literal_eval(next(n.value for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id=='ACTIVITIES' for t in n.targets)))
        names = []
        def walk(items):
            for name, entry in items.items():
                if 'items' in entry: walk(entry['items'])
                else: names.append(name)
        for items in routes.values():
            walk(items)
        report = (ROOT/'docs/solve_for_evaluation.md').read_text(encoding='utf-8')
        self.assertEqual(len(names), 39)
        for name in names:
            self.assertIn('| '+name+' |', report)

    def test_custom_page_selector_changes_refresh_questions(self):
        app = AppTest.from_file(str(ROOT/'Home.py'), default_timeout=25)
        app.session_state['nav_level'] = 'advanced'
        app.session_state['router_section'] = '⚡Electricity⚡'
        app.session_state['router_group'] = 'Current Electricity'
        app.session_state['router_activity'] = "Circuit Ohm's Law"
        app.run()
        self.assertFalse(app.exception)
        selector = next(w for w in app.selectbox if w.label == 'Solve for')
        for value in ('voltage', 'current', 'resistance'):
            app.selectbox(key=selector.key).select(value).run()
            self.assertFalse(app.exception)
            self.assertTrue(any(value.capitalize() in w.label for w in app.text_input))

        app = AppTest.from_file(str(ROOT/'Home.py'), default_timeout=25)
        app.session_state['nav_level'] = 'advanced'
        app.session_state['router_section'] = 'Chemistry'
        app.session_state['router_group'] = None
        app.session_state['router_activity'] = 'Stoichiometry Practice'
        app.run()
        app.selectbox(key='stoichiometry_reaction_type').select('Combustion').run()
        app.selectbox(key='stoichiometry_difficulty').select('Medium').run()
        for value, unit in [('gram-to-mole','mol'), ('mole-to-gram','g')]:
            app.selectbox(key='stoichiometry_solve_for_select').select(value).run()
            self.assertFalse(app.exception)
            self.assertEqual(app.session_state['stoichiometry_units'], unit)
            self.assertFalse(app.session_state['stoichiometry_submitted'])


if __name__ == '__main__':
    unittest.main()
