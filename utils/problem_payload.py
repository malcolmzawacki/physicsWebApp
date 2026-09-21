from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import math
from numbers import Number, Real


class ProblemPayloadError(ValueError):
    pass


@dataclass
class ProblemPayload:
    """
    Canonical payload for generator outputs.

    Required fields: question, answers, units
    Optional fields are free-form and may be ignored by some UIs.
    """

    question: str
    answers: List[Any]
    units: List[str]

    # Optional metadata populated by UI or generator
    problem_type: Optional[str] = None
    difficulty: Optional[str] = None

    # Optional features
    diagram_data: Any = None
    button_options: Dict[int, List[str]] = field(default_factory=dict)
    hints: List[str] = field(default_factory=list)
    extras: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not isinstance(self.question, str) or not self.question.strip():
            raise ProblemPayloadError("'question' must be a non-empty string")
        if not isinstance(self.answers, list) or len(self.answers) == 0:
            raise ProblemPayloadError("'answers' must be a non-empty list")
        if not isinstance(self.units, list) or len(self.units) != len(self.answers):
            raise ProblemPayloadError("'units' must be a list of same length as 'answers'")
        for answer in self.answers:
            if isinstance(answer, Number) and (not isinstance(answer, Real) or not math.isfinite(answer)):
                raise ProblemPayloadError("Numeric answers must be real and finite")
        if not all(isinstance(unit, str) for unit in self.units):
            raise ProblemPayloadError("Unit labels must be strings")
        if not isinstance(self.extras, dict):
            raise ProblemPayloadError("'extras' must be a dictionary")
        if not isinstance(self.button_options, dict):
            raise ProblemPayloadError("'button_options' must be a dictionary")
        for index, options in self.button_options.items():
            if not isinstance(index, int) or not 0 <= index < len(self.answers) or not isinstance(options, list):
                raise ProblemPayloadError("Choice options must map answer indices to lists")


def payload_from_dict(data: Dict[str, Any]) -> ProblemPayload:
    """
    Normalize a raw dict into a ProblemPayload, raising on missing fields.
    Unknown keys are routed to `extras`.
    """
    if not isinstance(data, dict):
        raise ProblemPayloadError("Generator result must be a dict")

    # Known top-level keys
    known = {
        'question', 'answers', 'units',
        'problem_type', 'difficulty',
        'diagram_data', 'button_options', 'hints', 'extras'
    }

    core = {k: data.get(k) for k in ['question', 'answers', 'units']}

    # Optional fields (if present)
    optional: Dict[str, Any] = {}
    for key in ['problem_type', 'difficulty', 'diagram_data', 'button_options', 'hints', 'extras']:
        if key in data:
            optional[key] = data[key]

    # Anything else goes to extras
    raw_extras = optional.get('extras', {})
    if not isinstance(raw_extras, dict):
        raise ProblemPayloadError("'extras' must be a dictionary")
    extras: Dict[str, Any] = dict(raw_extras)
    for k, v in data.items():
        if k not in known:
            extras[k] = v
    optional['extras'] = extras

    return ProblemPayload(**{**core, **optional})
