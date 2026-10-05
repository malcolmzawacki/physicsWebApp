"""Versioned, JSON-safe description of information available to a student."""
import math
from numbers import Real
from utils.quantities import PROFILES


def validate_setup(setup):
    if not isinstance(setup, dict) or setup.get("version") != 1:
        raise ValueError("Organizing help requires schema version 1")
    profile = setup.get("profile")
    if profile not in PROFILES:
        raise ValueError("Unknown organizing-help profile")
    fields = setup.get("fields")
    if not isinstance(fields, dict) or set(fields) != set(PROFILES[profile]):
        raise ValueError("Setup fields must match the profile's roles")
    requested = []
    for key, field in fields.items():
        if not isinstance(field, dict):
            raise ValueError("Setup field must be a dictionary")
        status = field.get("status")
        if status not in ("given", "implied", "requested", "absent"):
            raise ValueError("Unknown setup field status")
        if status in ("given", "implied"):
            value = field.get("value")
            if isinstance(value, bool) or not isinstance(value, Real) or not math.isfinite(value):
                raise ValueError("Given and implied quantities need finite numeric values")
        elif "value" in field:
            raise ValueError("Requested and absent fields must not expose hidden values")
        if status == "implied" and not field.get("source"):
            raise ValueError("Implied quantities need a wording cue")
        if status == "requested":
            requested.append(key)
    if not requested or setup.get("target_roles") != requested:
        raise ValueError("Actual target roles must match requested fields in profile order")


def make_setup(profile, values, given, requested, implied=None):
    implied = implied or {}
    roles = PROFILES[profile]
    given, requested = set(given), set(requested)
    if not (given | requested | set(implied)) <= set(roles) or given & requested or not set(implied) <= given:
        raise ValueError("Inconsistent setup roles")
    fields = {}
    for key in roles:
        if key in requested:
            fields[key] = {"status": "requested"}
        elif key in given:
            fields[key] = {"status": "implied" if key in implied else "given", "value": values[key]}
            if key in implied:
                fields[key]["source"] = implied[key]
        else:
            fields[key] = {"status": "absent"}
    result = {"version": 1, "profile": profile, "fields": fields,
              "target_roles": [key for key in roles if key in requested]}
    validate_setup(result)
    return result


def expected_entries(setup):
    validate_setup(setup)
    return {key: field["value"] if field["status"] in ("given", "implied")
            else "?" if field["status"] == "requested" else "x"
            for key, field in setup["fields"].items()}
