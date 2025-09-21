from abc import ABC
import streamlit as st
from typing import Optional, Any, Dict
import matplotlib


class BaseGenerator(ABC):
    def __init__(self, state_prefix):
        self.state_prefix = state_prefix

    ######## LEGACY SYSTEMS: KEEP UNTIL UPDATE IS COMPLETE ############

    def get_difficulty_range(self, difficulty) -> int:
        """outdated method of creating more complex problems via larger numbers"""
        if difficulty == "Easy":
            return 10
        elif difficulty == "Hard":
            return 50
        else:
            return 20
    


    def choose_problem_dict(self, problem_type: str, difficulty: str) -> Dict[str, Any]:
        """
        Default dictionary-based chooser.

        Subclasses may override this directly. If they only implement the
        legacy tuple-based `choose_problem`, this fallback converts it to
        the standard dict format.
        """
        if hasattr(self, 'choose_problem'):
            # accept tuple data from current choose problem
            question, answers, units, diagram_data = self.choose_problem(problem_type, difficulty)  # type: ignore[attr-defined]
            result: Dict[str, Any] = {
                'question': question,
                'answers': answers,
                'units': units
            }
            if diagram_data is not None:
                result['diagram_data'] = diagram_data
            button_options = self.get_answer_options(units)
            if button_options:
                result['button_options'] = button_options
            return result
        raise NotImplementedError("Generator must implement choose_problem_dict or choose_problem")


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
    
    
    def initialize_session_state(self) -> None:
        """Initialize basic session state variables with proper prefixing"""
        vars_to_init = [
            'current_question',
            'correct_answer',
            'correct_answer2',
            'unit',
            'unit2',
            'user_answer',
            'user_answer2',
            'submitted',
            'question_id',
            'difficulty',
            'problem_type'
        ]
        
        for var in vars_to_init:
            key = f"{self.state_prefix}{var}"
            if key not in st.session_state:
                st.session_state[key] = None
    
    def clear_answers(self) -> None:
        """Clear user answers when generating new questions"""
        st.session_state[f"{self.state_prefix}user_answer"] = None
        st.session_state[f"{self.state_prefix}user_answer2"] = None
        st.session_state[f"{self.state_prefix}submitted"] = False



    ######### DICTIONARY-BASED FUNCTIONS FOR THE UPDATED SYSTEM ######
    # choose_problem_dict is defined above with a sensible default fallback

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
