from abc import ABC
from typing import Optional, Any, Dict


class BaseGenerator(ABC):
    def __init__(self, state_prefix):
        self.state_prefix = state_prefix

    def get_difficulty_range(self, difficulty) -> int:
        """outdated method of creating more complex problems via larger numbers"""
        if difficulty == "Easy":
            return 10
        elif difficulty == "Hard":
            return 50
        else:
            return 20
    


    def choose_problem_dict(self, problem_type: str, difficulty: str) -> Dict[str, Any]:
        """Return a dictionary payload describing a question."""
        raise NotImplementedError("Generator must implement choose_problem_dict")


    def generate_diagram(self, diagram_data: Any, problem_type: str, difficulty: str) -> Optional['matplotlib.figure.Figure']:
        """
        Opt out for diagrams
        """
        return None


    def get_answer_options(self, units: list[str]) -> dict[int, list[str]]:
        """
        Optional method for generators that want to provide button-based answers
        
        :param units: List of unit strings from choose_problem
        :returns: Dict mapping answer index to list of button options
                 Empty dict means use text input for all answers
        """
        return {}  # Default: no button options, use text input
    
    
    # Utility methods for new interface
    def validate_result_dict(self, result: dict) -> bool:
        """Validate that dictionary has required fields"""
        required_fields = ['question', 'answers', 'units']
        for field in required_fields:
            if field not in result:
                raise ValueError(f"Generator missing required field '{field}'")
        return True

    # Optional metadata hook used by the UI to display equations or notes
    def stored_metadata(self) -> Dict[str, Dict[str, Any]]:
        """Return the full metadata map for this generator."""
        return {}

    def get_problem_metadata(self, problem_type: str) -> dict:
        """Return metadata for a given problem type."""
        metadata = self.stored_metadata()
        if not isinstance(metadata, dict):
            return {}
        return metadata.get(problem_type, {})

    def get_problem_types(self) -> list[str]:
        """Return the list of supported problem types for UI consumers."""
        metadata = self.stored_metadata()
        if isinstance(metadata, dict) and metadata:
            return list(metadata.keys())
        return []
