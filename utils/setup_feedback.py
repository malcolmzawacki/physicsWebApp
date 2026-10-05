"""Pure setup checks and ordered feedback rules, independent of Streamlit."""

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class SetupFeedback:
    status: str
    code: str
    message: str


def normalize_entry(value):
    return str("" if value is None else value).strip().lower().replace("−", "-")


def check_entry(value, expected):
    value = normalize_entry(value)
    if not value:
        return "empty", "Not entered"
    if isinstance(expected, str):
        return ("correct", "Correct") if value == expected else ("incorrect", "Check this entry")
    try:
        number = float(value)
    except ValueError:
        return "incorrect", "Check this entry"
    if math.isfinite(number) and math.isclose(number, expected, rel_tol=0, abs_tol=1e-9):
        return "correct", "Correct"
    return "incorrect", "Check this entry"


def _other_given(value, key, expected, roles=None):
    # Matching a number is evidence of a possible mix-up, not proof of reasoning.
    try:
        number = float(value)
    except ValueError:
        return None
    if not math.isfinite(number):
        return None
    own = expected[key]
    # A sign-only discrepancy can coincidentally match another given. Do not
    # diagnose that as a quantity mix-up until we have a dedicated sign rule.
    if not isinstance(own, str) and math.isclose(abs(number), abs(own), rel_tol=0, abs_tol=1e-9):
        return None
    matches = [other for other, given in expected.items()
               if other != key and not isinstance(given, str)
               and check_entry(value, given)[0] == "correct"]
    if not matches:
        return None
    return SetupFeedback(
        "incorrect", "matches_other_given",
        "This number matches another given quantity. Check the units and the "
        "words beside it in the problem. Do they describe this column?"
        + (" For velocities, also check whether it describes the start or the end."
           if roles is not None and roles[key].phase in ("initial", "final") else ""),
    )


# First matching rule wins. Add narrowly supported rules ahead of the fallback.
FEEDBACK_RULES = (_other_given,)


def evaluate_entry(value, key, expected, roles=None):
    value = normalize_entry(value)
    status, message = check_entry(value, expected[key])
    if status != "incorrect":
        return SetupFeedback(status, status, message)
    for rule in FEEDBACK_RULES:
        result = rule(value, key, expected, roles)
        if result is not None:
            return result
    return SetupFeedback(
        "incorrect", "unclassified",
        "Recheck the value and wording for this quantity. Use ? if it is asked "
        "for, or x if it is neither provided nor asked for.",
    )
