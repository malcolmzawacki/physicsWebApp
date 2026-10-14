# Systematic content and organizing-help rollout

_Established process: 2026-10-12, first applied to the Wave Properties rollout.
This specifies how to use the existing inventory tools consistently._

## One work package, one instructional family

Use a named problem type (or an explicitly bounded difficulty/scenario subset) as
the unit of work. A page may contain multiple families with different readiness.
Keep one implementation package active at a time, consistent with the teacher's
preference to try each incremental rollout. Maintain a small ordered queue in
[project_roadmap.md](project_roadmap.md); don't create disconnected TODO lists.

Content completion, architecture migration, feedback expansion, and UI enablement
are distinct outputs. A discovery such as missing period questions produces a
visible content task and an updated review; it is not silently omitted. Existing
session authorization applies to routine work; these checks are quality criteria,
not new permission prompts.

## Sources of truth

| Question | Authoritative location |
|---|---|
| What exists and what has been reviewed? | Generated organizing_help_inventory.md plus organizing_help_reviews.json |
| What is shipped right now? | current_state.md, backed by source and targeted tests |
| What educational direction guides changes, and what comes next? | Product direction and ordered queue in project_roadmap.md |
| What does this family intend to teach/cover? | Linked family review and coverage matrix |
| What identifies quantities, roles, units, symbols? | utils/quantities.py for migrated profiles |
| What information does this generated prompt supply? | Generator-produced extras.setup, validated by setup_schema |
| What targets can be requested? | solve_for_catalog.json where applicable; actual target is in each generated setup |
| What feedback is supported? | setup_feedback.py rules and tests |

The inventory is generated; edit decisions in the review ledger, then rebuild.
Keep new family notes linked from its ledger notes. Do not rewrite every historical
record when status changes; update current_state, the queue, and the authoritative
review. Status counts refer to rows, not pages or completed branch audits.

Use the [README document guide](../README.md#where-to-look) to locate an existing
home before adding a file. Routine updates belong in these owners, not new dated
reports or parallel plans. Keep strategy in the roadmap, reusable contracts in
feature guides, and branch evidence in the linked family review.

## Repeatable stages and exit evidence

| Stage | Deliverable | Exit evidence |
|---|---|---|
| Discover | Complete activity/type rows and source entry points | Route/type discovery includes custom layouts and unsupported modes |
| Review content | Intended combination matrix and explicit exclusions | Compare actual prompts, reference equations, targets, and all reachable branches |
| Resolve content gaps | Missing combinations, wording, unit/precision fixes where agreed | Students have sufficient independent information; expected answers match displayed givens |
| Connect metadata | Shared quantities/roles, actual targets, equation/label mappings | Valid schema; hidden answers excluded from givens; constants/implied facts explicit |
| Verify feedback | Existing rule fit and necessary specialized rules | Positive examples and ambiguous/coincident-number counterexamples; fallback retained |
| Integrate and test | Bounded page opt-in, state flow, appropriate tests | Enter/Tab, independent final answers, question resets, unsupported branches, visual review |
| Record and observe | Updated ledger, generated inventory, concise findings | Teacher can try the exact shipped scope; new discoveries become queued work |

Review doesn't require exposing every mathematically imaginable inverse. Define
instructionally intended combinations and classify others as excluded with a
reason. Existing solve-for deferrals are not automatic blockers; fixed-output
problems can emit actual requested roles. Content gaps within the intended scope
should be completed before enabling that family, as agreed during the Waves review.

## Coverage matrix: required for each family

Use one row per distinct given/requested scenario, with difficulty and sampling
scope explicit. Include both selector-driven and randomly chosen branches. The
site inventory stays readable at type level; this matrix supplies the detail it
intentionally lacks.

| Branch / difficulty | Given and implied roles | Requested roles | Absent roles | Displayed units / precision | Prompt + answer evidence | Organizer evidence | Disposition |
|---|---|---|---|---|---|---|---|
| Fill before rollout |  |  |  |  |  |  | Not reviewed |

Dispositions: intended/implemented, intended/missing, deliberately excluded, or
needs a decision. Distinguish the two frequency/period forms of a wave-speed
question even when they share the same requested quantity. Never label a whole
page ready based on one exercised branch.

## Family work-package template

Copy this into a family review document:

```text
Family / inventory IDs:
Scope: problem types, difficulties, scenarios, target combinations
Source entry points: page, generator/custom model, equations, solve-for
Current behavior and evidence:
Intended coverage matrix:
Explicit exclusions and reasons:
Content gaps and dependencies:
Quantity/role profile: units, symbols, object/axis/stage context
Given/implied information and assumptions:
Displayed precision and answer/checking policy:
Feedback rules: supported cases, ambiguity, fallback
UI integration: layout, Enter/Tab, last-check results, final-answer separation
Verification: automated commands/results; manual checks; remaining limits
Rollout status and date:
Discoveries reusable by the next family:
```

## Verification scaled to the change

For generator/physics changes, run the two established baseline checks:

```text
python tools/validate_payloads.py
python tools/check_prompt_answer_consistency.py
```

Also run schema, applicable family and interaction scripts, solve-for checks when
targets change, and export checks when shared generation/formatting changes. Add
meaningful branch tests for new content; don't merely assert that copied metadata
matches itself. Verify prompt values, displayed rounding, and physically supported
relationships. Record failures and limits without claiming unrelated coverage.

For organizer changes, existing scripts are test_setup_schema.py,
test_setup_workspace.py, test_constant_setup.py, test_momentum_setup.py,
test_wave_setup.py, test_single_resistor_setup.py, test_force_setup.py, and
test_energy_setup.py under
tools/. Browser/manual review is needed for actual keyboard behavior, alignment,
small screens, and assistive technology; AppTest checks alone are not equivalent.

After a status/type/route change:

```text
python tools/build_organizing_inventory.py
python tools/build_organizing_inventory.py --check
```

Custom selector changes require updating the inventory's explicit adapter. A new
route without an adapter is surfaced as unresolved; it must not vanish. Worksheet
assistance has a separate scope and must not automatically inherit practice status.

## Reporting progress without overstating it

Use the existing review ledger status field with an informative stage and bounded
notes; a database/schema migration is not necessary just to start using this
process. Suggested language: Reviewed/content gap, Metadata migrated/UI pending,
Enabled/bounded scope, or Alternate scaffold required. Blank still means unreviewed.
Do not bulk-fill classifications from estimates in the architecture guide.

At the end of each package report: exact enabled scope, verification, outstanding
gaps, and one next candidate. If content needs a pedagogical decision, present the
concrete matrix/options; continue independent review work while that decision is
pending. Teacher observations inform a follow-up package rather than silently
expanding the active one to adjacent units.

## First application of this process

Wave Properties' existing review now records all eight implemented forms, period
precision, sampling, shared units/equations, and branch-level evidence. Its
four-role organizer is enabled, automated checks passed, and the teacher confirmed
the period problems and Tab/Enter behavior. Single Resistor has now followed the
same process using its existing circuit guide, with automated checks passed and
teacher review pending. The next scalar candidates
are queued by estimated complexity, not presumed ready. Grouped and nonnumeric
scaffolds follow as separate designs.
