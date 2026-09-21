# September audit corrections

**September 15 update:** [Progress IDs and expanded native Word formatting](implementation_fixes_2026-09-15.md)
supersede the incremental ID rollout and limited formatting described below.

The implementation audit is retained as a historical record. Its defects have been addressed in this change; this file describes the resulting behavior and verification limits.

## Physics and activities

- Parallel schematics use common upper/lower rails without a source short. Site and export adapters share the corrected geometry.
- Tension uses force balance with positive tensions and feasible wire angles. Opposing wires have at least five degrees of angular separation.
- Thermal loss samples cannot consume more than the available energy. The payload boundary rejects non-real and non-finite numeric answers.
- Static incline prompts explicitly ask for a maximum angle or minimum coefficient. Induction states its classroom charge-chunk assumption rather than implying a physical magnitude can be inferred from rod charge alone.
- Graph difficulty progresses from constant motion (Easy), through speeding up (Medium), to the full mix including slowing down (Hard). Explicit graph-type requests and complete worksheet graph sets remain available.

## Shared input and question flow

- Standard, Relative Motion, matching, and circuit activities record one attempt per question. Use New Question/New Circuit for another attempt. Feedback persists on reruns, and correct questions use the shared per-question cancellable countdown. Matching selectors immediately regenerate the set.
- Choice selections reset for each new question. Choice/text fallback combinations collect all parts and share numeric parsing. Duplicate dropdown values are valid unless the payload sets `unique_choices=True`; torque rankings declare this constraint.
- `utils/grading.py` centralizes finite-number parsing and comparison. Standard/Relative Motion numeric answers use 10% relative tolerance with a 1e-9 zero floor. Circuit answers retain their existing 5% / 0.05-unit policy. String answers are trimmed and case-insensitive. Circuit tolerance is intentionally distinct, not an implicit layout side effect.
- Difficulty stars are explicitly Easy=1, Medium=2, Hard=3 regardless of selector ordering. Optional type weighting uses metadata `star_weight`, default 1. Existing session star totals are retained.
- Metadata can declare a stable `id` plus `aliases` for older display labels. Interface merges legacy history into the ID without losing counts; unconverted generators retain their existing label keys for compatibility. When renaming a type, keep its ID and declare old labels as aliases.
- Interface retains the normalized payload, including extras. Explanations and solution equations render after submission; hints, tags and diagrams remain available. Canonical fields such as `diagram_data`, `button_options`, and `hints` stay at the top level; extension fields can be top-level or in `extras`. Payload `time_limit` (legacy alias `timer`) controls advancement, with an explicit layout `timer` taking precedence. These values describe the next-question delay, not a timed exam.
- Equation rendering accepts both short/long metadata names and joins equation lists into a LaTeX gathered environment. Optional `show_equations` and `side_by_side` payload settings are respected unless the caller overrides them.

## Word export

Install all declared dependencies with `pip install -r requirements.txt`, including `python-docx`.
Both `python -m xtrct_docs.doc_face` and `python xtrct_docs/doc_face.py` launch the existing worksheet entry point.

Every organizer worksheet preset returns a callable that creates fresh sections for each version. The duplicated incline coefficient block is removed. `create_doc` validates payloads before using their answers/units, returns the saved path, and accepts `output_path` and `open_document=False` for automation/tests.

Diagrams are included by default. Explicit `include_graphs=False` omits all figures consistently, including side-by-side figures, and labels omitted diagrams. Choice options and numeric fallback blanks are printed in either layout. Raw diagram data must have a renderer:

```python
from utils.problem_adapters import with_diagram_renderer, circuit_payload, matching_payload

# For a generator's ordinary raw diagram data:
problem = with_diagram_renderer(problem, generator, problem_type, difficulty)

# For custom circuit or matching cases:
problem = circuit_payload(circuit_case)
problem = matching_payload(matching_case)
```

The organizer attaches context automatically for its tension, Atwood and displacement presets. These adapters also produce payloads the standard Interface can consume; custom case dictionaries are not implicitly guessed to be standard payloads.

Prompt rendering preserves paragraphs and lists, supports bold/italic/code spans, and renders `$...$`, `$$...$$`, and `\(...\)` math supported by Matplotlib mathtext as inline images. This is an explicit worksheet markup subset, not a complete Markdown/LaTeX document processor; unsupported math produces a clear error. Ordinary source-wrapped prose lines are joined within their paragraph. Graph embedding uses memory buffers rather than temporary PNG files.

## Verification

CI now runs all five commands:

```text
python tools/validate_payloads.py
python tools/check_prompt_answer_consistency.py
python tools/test_activity_flow.py
python tools/test_relative_motion_page.py
python tools/test_audit_regressions.py
```

Payload validation discovers all BaseGenerator subclasses automatically (currently 23; 4,200 seeded checks). The added audit suite checks force balance, thermal answer domains, electrical connectivity, export serialization and diagrams, prompt formatting, payload ownership, mixed inputs, progress migration, selector resets, one-attempt scoring, and countdown resume behavior. All organizer presets are serialized and reopened as Word documents in regression tests.

The installed environment lacks LibreOffice. An attempted `render_docx.py` verification stopped with `LibreOffice soffice.exe was not found on PATH`; Word/PDF pagination and visual layout remain unverified. No DOCX is being delivered as a visually certified artifact. The code and serialization checks do not substitute for that final visual check.
