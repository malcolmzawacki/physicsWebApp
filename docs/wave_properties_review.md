# Wave Properties content review and rollout

_Reviewed: 2026-10-11; content and organizer implemented/checked: 2026-10-12._

Organizing help is enabled for all eight Wave Properties forms below. This review
covers `properties_of_waves`, its solve-for catalog entries, and `wave_properties`
page. Harmonics and decibel activities remain outside this reviewed scope.

## Scope and sampling

The page exposes Easy only; difficulty remains compatibility-only in the
generator and catalog. There are four solve-for targets: wave speed, wavelength,
frequency, and period. The first three retain their existing IDs. Mixed practice
samples all eight forms equally. Each explicit target samples its two forms
equally, making frequency/period-based relationships and direct reciprocal
practice reachable without adding another student-facing selector.

The original integer frequency/wavelength seed ranges (2 through 100) are retained.
Given periods are rounded to three decimal places, with trailing zeros removed,
before computing the requested answer. All answers use the values actually
displayed: e.g. a period of 0.143 s requests frequency 1/0.143 Hz, not the hidden
seed frequency of 7 Hz. Requested period answers retain the calculated reciprocal;
students submit them using the existing final-answer tolerance. Organizer entries
check the displayed givens exactly, independently of final-answer grading.

Wavelength uses m consistently in prompts, answer labels, and shared quantity
definitions. Period reuses the duration quantity with a local T role; frequency
has its own Hz definition. Generator equation metadata resolves shared symbols
and covers v=lambda*f, T=1/f, and v=lambda/T with rearrangements. The page's
duplicate equation reference has been removed. There is no inferred algebra.

## Reviewed coverage matrix

All rows are implemented and checked. All givens are explicit; there are no
implied constants. Roles not given or requested are absent (x), even if derivable.

| Variant / difficulty | Given | Requested | Absent | Answer from displayed givens | Disposition |
|---|---|---|---|---|---|
| 0 / Easy | f, lambda | v | T | lambda*f | Implemented; organizer enabled |
| 1 / Easy | v, f | lambda | T | v/f | Implemented; organizer enabled |
| 2 / Easy | v, lambda | f | T | v/lambda | Implemented; organizer enabled |
| 3 / Easy | T, lambda | v | f | lambda/T | Implemented; organizer enabled |
| 4 / Easy | v, T | lambda | f | v*T | Implemented; organizer enabled |
| 5 / Easy | v, lambda | T | f | lambda/v | Implemented; organizer enabled |
| 6 / Easy | f | T | v, lambda | 1/f | Implemented; organizer enabled |
| 7 / Easy | T | f | v, lambda | 1/T | Implemented; organizer enabled |

Frequency and period supply the same independent information and are never
presented as two independent givens. Medium/Hard catalog calls use the same eight
forms for backward compatibility; they are not distinct instructional levels.
Medium/context realism, conversions, signs, and zero-valued waves are deliberately
outside this positive scalar scope. More realistic generation remains roadmap work.

## Feedback, lifecycle, and verification

The four-role organizer uses the shared explicit-check form. Feedback retains the
possible-other-given rule and neutral fallback; no initial/final velocity hint is
applied. Numeric coincidence is not interpreted as proof of a misconception.
Requested/absent metadata contains no hidden answers. Derived-but-unstated values
remain x. No new specialized reciprocal misconception diagnosis is introduced.

`tools/test_wave_setup.py` passed 2,376 displayed-value cases covering all eight
forms, all original frequency seeds, boundary wavelengths, coincident givens,
nonterminating reciprocals, and prompt/answer/unit agreement. It also checks every
explicit-target call and Mixed branch, invalid variants, feedback ambiguity,
DOCX serialization, and the routed page's eight forms. Page checks cover buffered
entries, explicit checks, separate forms with Enter enabled, stale-feedback cues,
selector/new-question resets, independent final-answer scoring, and exclusion of
Harmonics. The existing one-attempt final-answer policy is retained; retries are
separate roadmap work.

Baseline validation passed 4,200/4,200 payloads across 23 generators, plus the
prompt/answer consistency guardrail. The solve-for suite passed all nine tests
including 525 target/level combinations and DOCX serialization. Existing schema,
organizer, Constant Speed, and Momentum checks passed. Organizer regression scripts
and inventory drift checks are now configured in CI; remote CI has not been run
as part of this local rollout.

The teacher confirmed the new period problems and working Tab/Enter behavior on
2026-10-12 and requested the next family. This completes the teacher checkpoint
for the tried scope; narrow-screen, screen-reader, and broader classroom review
are not certified by that confirmation or automated form checks. Single Resistor
is the next family and its status is maintained in the roadmap.

## Original finding retained for context

The 2026-10-11 review found only variants 0–2, period present solely in reference
equations, inconsistent wavelength labels, and no organizer metadata. Those content
and metadata gaps are resolved by this bounded rollout.
