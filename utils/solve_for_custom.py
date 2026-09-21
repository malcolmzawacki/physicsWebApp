"""Payload adapters for custom pages with clear existing target choices."""
from utils.problem_adapters import circuit_payload
from utils.generators.current_electricity.ohms_law_model import build_circuit_case


class OhmsLawTargets:
    def single_resistor(self, difficulty, solve_for):
        return self._payload(build_circuit_case("Single Resistor", difficulty, solve_for))

    def choose_problem_dict(self, problem_type, difficulty):
        return self._payload(build_circuit_case(problem_type, difficulty))

    @staticmethod
    def _payload(case):
        payload = circuit_payload(case)
        payload["extras"] = {"case": case}
        return payload

    def generate_diagram(self, diagram_data, problem_type, difficulty):
        from utils.circuit_diagrams import circuit_figure
        return circuit_figure(diagram_data)


class StoichiometryTargets:
    """Accept the existing page factory so browser and exporter use identical code."""
    def __init__(self, factory, reaction_type="Random"):
        self.factory, self.reaction_type = factory, reaction_type

    def conversion(self, difficulty, conversion_type=None):
        question, answer, units, details = self.factory(self.reaction_type, difficulty, conversion_type)
        return dict(question=question, answers=[answer], units=[units], extras={"details": details})

    def choose_problem_dict(self, problem_type, difficulty):
        return self.conversion(difficulty)

    def generate_diagram(self, diagram_data, problem_type, difficulty):
        return None
