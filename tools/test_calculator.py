"""Arithmetic, input restriction, and shared calculator navigation regressions."""

from pathlib import Path
import math
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from utils.calculator import calculate


class CalculatorTests(unittest.TestCase):
    def test_physics_expressions(self):
        self.assertEqual(calculate("0.5 * 2 * 3^2"), 9)
        self.assertEqual(calculate("3e8 / 6e14"), 5e-7)
        self.assertAlmostEqual(calculate("12 * sin(30)"), 6)
        self.assertAlmostEqual(calculate("sin(pi/2)", degrees=False), 1)
        self.assertEqual(calculate("sqrt(144) + log(100)"), 14)
        self.assertEqual(calculate("ans * 2", answer=7), 14)
        self.assertEqual(calculate("−2^2"), -4)
        self.assertAlmostEqual(calculate("asin(1)"), 90)
        self.assertAlmostEqual(calculate("ln(e)"), 1)

    def test_rejects_invalid_or_unbounded_input(self):
        for expression in ["1/0", "sqrt(-1)", "(-1)^0.5", "1e309", "9^999999",
                           "__import__('os')", "pi.real", "[1,2]", "True", "sin(1, 2)",
                           "sqrt(x=4)", "2(3)", "1+", "9" * 251]:
            with self.subTest(expression=expression), self.assertRaises(ValueError):
                calculate(expression)

    def test_saved_calculation_and_navigation(self):
        from streamlit.testing.v1 import AppTest
        app = AppTest.from_file(str(ROOT / "Home.py"), default_timeout=30).run()
        self.assertFalse(app.exception)
        app.text_input(key="physics_calculator_expression").set_value("12 * sin(30)").run()
        self.assertFalse(app.exception)
        self.assertAlmostEqual(app.session_state["physics_calculator_answer"], 6)
        app.radio(key="physics_calculator_mode").set_value("Radians").run()
        next(b for b in app.button if b.label == "Kinematics").click().run()
        next(b for b in app.button if b.label == "Constant Motion").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.text_input(key="physics_calculator_expression").value, "12 * sin(30)")
        self.assertEqual(app.radio(key="physics_calculator_mode").value, "Radians")
        self.assertEqual(len(app.session_state["physics_calculator_history"]), 1)
        app.button(key="physics_calculator_clear").click().run()
        self.assertEqual(app.text_input(key="physics_calculator_expression").value, "")
        app.button(key="physics_calculator_key_1_7").click().run()
        app.button(key="physics_calculator_equals").click().run()
        self.assertEqual(app.session_state["physics_calculator_answer"], 7)


if __name__ == "__main__":
    unittest.main()
