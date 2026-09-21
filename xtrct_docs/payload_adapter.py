"""Attach explicit generator context to the legacy worksheet factories."""
from utils.problem_adapters import with_diagram_renderer
from utils.solve_for import generate_selected, target_options, MIXED


class DocumentGenerator:
    def __init__(self, generator, method_types=None):
        self.generator = generator
        self.method_types = method_types or {}

    def targets(self, problem_type, difficulty="Medium"):
        return target_options(self.generator, problem_type, difficulty)

    def question(self, problem_type, difficulty="Medium", solve_for=MIXED):
        result = generate_selected(self.generator, problem_type, difficulty, solve_for)
        return with_diagram_renderer(result, self.generator, problem_type, difficulty)

    def section(self, heading, problem_type, difficulty="Medium", solve_for=MIXED, count=5, gap=1):
        """Return a fresh section factory, reusable for each worksheet version."""
        def build():
            return [{"heading": heading, "gap": gap, "problems": [
                self.question(problem_type, difficulty, solve_for) for _ in range(count)]}]
        return build

    def __getattr__(self, name):
        method = getattr(self.generator, name)
        if not callable(method):
            return method

        def generate(*args, **kwargs):
            result = method(*args, **kwargs)
            if isinstance(result, dict) and "answers" in result:
                types = self.generator.get_problem_types()
                problem_type = self.method_types.get(name, types[0] if len(types) == 1 else "")
                difficulty = kwargs.get("difficulty", args[0] if args and args[0] in ("Easy", "Medium", "Hard") else "Medium")
                result = with_diagram_renderer(result, self.generator, problem_type, difficulty)
            return result
        return generate
