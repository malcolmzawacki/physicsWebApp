# Progress identities and expanded Word formatting

This completes the two code follow-ups from the September 14 audit. Visual Word
and browser review remains for the user; automated checks do not verify pagination.

## Progress identities

All 70 problem types across 23 generators now declare permanent `id` values and
legacy display-label `aliases` in metadata. Twelve custom activity types use
`utils/progress_ids.py`. Session history merges label-keyed attempts and correct
counts into ID-keyed records, including when both already exist. Migration is
idempotent; performance tables still show readable labels. Reset initializes ID
keys. This does not add persistence across browser sessions or server restarts.

When renaming a type, retain its ID and append the old label to `aliases`. New
types need unique IDs. Custom activities must also update the registry's current
label. Do not derive permanent IDs from display labels at runtime.

## Word formatting

Question text and section instructions support Markdown headings, nested ordered
and unordered lists, list starting numbers, tables with aligned cells and repeating
headers, block quotes, links, hard breaks, rules, nested emphasis, strikethrough,
and literal inline/fenced code. Answer text supports inline formatting.

LaTeX delimited by `$...$`, `$$...$$`, `\(...\)`, or `\[...\]` becomes editable
Word equations. Supported structures include fractions, subscripts/superscripts,
roots, vectors/accents, delimiters, aligned/gathered equations, and matrices.
This is not a full TeX engine: unsupported commands/structures raise contextual
errors. Markdown images must use the existing diagram payload/renderer path;
the exporter does not fetch image URLs. Raw HTML is not interpreted.

Install the updated requirements, including `markdown-it-py` and `latex2mathml`.
The new integration suite is `python tools/test_progress_and_formatting.py` and
runs in CI alongside the five existing guardrails. It checks identity uniqueness,
history migration across every generator, custom aliases, and saved/reopened Word
structure (equations, numbering, links, tables, literal code, and emphasis).

## Afternoon review

Generate a repeatable formatting fixture:

```powershell
python tools/test_progress_and_formatting.py --sample review_samples/worksheet_formatting.docx
```

- In Word, check page breaks, question spacing, nested lists, table widths and
  headers; click an equation to confirm it is editable. Check print preview too.
- Export a normal worksheet preset and check diagram size, placement, answer key,
  multiple versions, and exports with diagrams disabled.
- In the browser, check narrow and wide layouts, choice reset, feedback after
  reruns, countdown cancellation/resume, and one scored attempt per question.
- Check progress tables after practice and reset: readable labels, correct counts,
  and no duplicate rows. Legacy-history merging is covered by automated fixtures.

LibreOffice is unavailable in this environment. The sample is for human review,
not a claim of visually verified Word layout.
