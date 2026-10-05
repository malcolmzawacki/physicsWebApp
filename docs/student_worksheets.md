# Student worksheet pilot



Open Kinematics > Create a worksheet. Each section offers Constant Motion, Accelerated Motion, Distance & Displacement, or Projectiles. Relative Motion is also available at the Advanced course level. Add or remove

sections, each with its own activity and problem type, difficulty, solve-for target and count.

The provisional cap is 20 questions across the whole worksheet, enforced before

any questions are generated. There can be at most 20 nonempty sections.

Choose writing

space, and whether to append answers. Generate explicitly; changing settings

hides old downloads until a new worksheet is generated. Practice state is separate.



Writing space uses physical heights: Compact 0.25 inches, Standard (default)

0.5 inches, and Extra writing space 1 inch per question. Changing spacing or the

answer-key option offers **Update layout**, preserving the current questions.

Changing topic, difficulty, target or count generates new questions instead.



After conversion, the builder reports actual total, question and answer-key page

counts. **Show print preview** offers first/previous/next/last arrow buttons and a

Page X of Y indicator, with boundary buttons disabled. New documents reset to page 1.

It displays the selected page rasterized from the exact

downloadable PDF. Only the current preview image is retained in the session.

Page counts are measured, not estimates of questions per page. The preview uses

`pypdfium2` from `requirements.txt`; install updated requirements before local use.



PDF is the only student download. DOCX remains the internal conversion source;

retrying PDF conversion preserves the questions. Answer keys

start on the next page rather than forcing an odd page in this student workflow.

Existing instructor export defaults are unchanged.



## Deployment



Streamlit Community Cloud installs the LibreOffice Writer and font packages in

the root `packages.txt`. For another Linux host, install those packages in its

image/environment. For Windows development, standard LibreOffice installations

are detected automatically, including after restarting the terminal. For a custom

installation, set `LIBREOFFICE_PATH` to the full path of `soffice.com`, or put its

program directory on PATH. The app never launches Word or a visible office window.



Without the renderer, the UI explains unavailability and disables generation.

For the Chromebook pilot, verify PDF availability on the deployed host before

inviting students. No conversion service or student account is needed.



Each conversion has a temporary directory and isolated LibreOffice profile;

files are removed afterward. One conversion runs per server process, with a

thirty-second queue wait and sixty-second conversion timeout. Downloads persist in

session memory, not a shared cache. Conversion errors allow retry of the same DOCX.



## Verification



Run `python tools/test_student_worksheets.py`. This checks document contents,

answer-key settings, converter cleanup/timeouts, actual routed UI behavior, and

retry stability. Real PDF conversion runs when LibreOffice is installed; CI

installs it explicitly. Before student rollout, visually review Easy/Medium/Hard

PDFs, long prompts and extra spacing, and print one using a school Chromebook.

Check school printer access separately from document generation.



## Progress and measurements



Students see preparation, waiting (only when the converter is occupied), PDF

conversion, and preview preparation messages. A queue timeout offers retry using

the same DOCX. The thirty-second wait is provisional, not a measured capacity limit.

Conversion timeout stops the converter process group on Linux or process tree on

Windows. It does not impose a deadline on Python question/document generation.



Server logs prefixed `worksheet` record document, wait, conversion and preview

seconds. The combined timing excludes idle user time and later page navigation.

AUTHOR_MODE also exposes the timing breakdown in the builder. This measures local

or hosted requests wherever the app is running; no stopwatch is needed. Logs do

not include questions, answers or student identifiers. No classroom capacity claim

is inferred from local timings.



Tests cover multi-section content and UI, total-cap rejection before generation,

queue timeout/recovery, converter failures, actual hanging-process termination,

layout preservation, retry stability and real PDF conversion when available.



This pilot does not add a global catalog, PDF editing, or uploads.



Activity pages offer a Create a worksheet shortcut that starts a fresh recipe with

that activity selected. Ordinary navigation to the builder retains the current

recipe during the session. The shared activity registry includes the five text-solvable Kinematics activities;

motion-graph interpretation is also enabled. Distance/displacement and relative-motion

worksheet adapters omit optional diagrams because all givens are in the prompts.

Practice-page diagrams remain unchanged.





## Motion graph interpretation



Choose Types of Motion Graphs, then Position-Time Graph or Velocity-Time Graph.

All six shapes are always included; no difficulty selector is shown. Hard is the

internal compatibility value, not a student-facing tier.

Students circle direction and motion state choices beside each black-and-white

plot. The twenty-question total includes graph questions. Graph matching is available as a separate activity.



Worksheet graph specifications persist with the questions, so layout updates

redraw the same curves. No live Matplotlib figures or practice-state writes are

retained by the worksheet adapter. Existing instructor and practice paths remain

available. Graphs and choices use the exporter’s existing unsplittable question

blocks. Longer worksheets naturally require more pages; preview the actual PDF.





Graph worksheet selection samples without replacement within each graph family

and difficulty, continuing across matching sections in a document. All requests use six eligible shapes, including legacy Easy/Medium worksheet

requests. After exhausting a pool, a new cycle begins

without repeating the last shape immediately. Counts differ by at most one for

matching pools. Layout updates preserve the original selected graphs.



Multipart answer keys use explicit Word line breaks for each labeled answer and

keep each question's answer block together. This applies to all DOCX/PDF exports.





## Matching motion graphs



Choose Matching Motion Graphs, then Position-Time First or Velocity-Time First.

This uses a single Standard level, matching the practice activity's scope rather

than inventing difficulty tiers. Each question prints a given graph and three

labeled choices in a 2-by-2 arrangement. One answer letter identifies the match.

Primary shapes cycle through all six before repeating; distractors are distinct

and option positions are shuffled. The same choices and answer letter persist

through layout updates. Numerical velocity axes are calibrated to the derivatives

of the existing position curves for these worksheet pairs. All four plots stay in

one question block. These questions use more paper; check the preview.



The practice UI also uses MotionGraphGenerator.FIXED_DIFFICULTY = "Hard". Existing

progress history is retained; new attempts use the existing Hard scoring bucket.

For student exports, WorksheetMotionGraphs normalizes incoming difficulty to Hard.

The base generator keeps explicit legacy subsets for other callers, but defaults

to Hard when omitted. See both class/function docstrings before changing this policy.


## Forces unit

Open **Dynamics > Create a worksheet**, or use a Forces activity shortcut.
High School offers Newton's Second Law. Advanced also offers Center of Mass,
Tension, Atwood Machines, and Inclined Planes, matching practice navigation.
Atwood and Inclines retain their Medium-only setting. Solve-for choices reuse
practice's registry. The existing 20-question total cap applies.

`render_unit_worksheet(unit)` shares generation, download and preview behavior.
`UNIT_ACTIVITIES` restricts visible choices; separate session prefixes preserve
each unit's recipe and PDF. No cross-unit selector is exposed.

Forces worksheets use complete text prompts without practice diagrams. Atwood
diagram labels can disclose unknown masses or coefficients: mask unknowns before
adding those diagrams to worksheets. Prompts explicitly specify g = 10 m/s²,
horizontal reference angles for tension, and meter coordinates for center of
mass. These adaptations do not change practice generators.

## Answer-key precision

The shared exporter displays numeric answers to at most three decimal places,
removing trailing zeros. Nonzero magnitudes below 0.01 use scientific notation
with three decimal places to avoid losing relative accuracy. Text answers are
unchanged, and stored numeric answers retain full precision for grading.

## Optional Tension insets

When a recipe contains Tension, **Include compact Tension diagrams** adds a
black-and-white two-inch sketch beside each prompt. It defaults off for comparison
with text-only worksheets. Wire numbers and given angles are shown, but solved
tensions are never included. Other activities and required motion graphs are
unaffected. Changing this option offers **Update layout** and preserves the
same questions and answers. Stored diagram specifications are rendered only
when requested; a borderless table keeps the prompt and sketch together, with
full-width answer boxes and working space below.

Tension prompts omit the repeated gravity and horizontal-angle reminders.
This applies to newly generated worksheets, with or without insets.

Tension worksheet prompts use `worksheet_question`, authored alongside the
practice prompt from the same sampled scenario. This avoids repeated random
object names and story text without changing the givens, answers, or practice
narrative. Compact inset samples tested with three seeds (12 questions each)
fit two on the title page and three on subsequent full question pages. This is
observed pagination, not a fixed page-count guarantee for other spacing choices
or mixed-section documents.

Tension insets now use a fixed 2 by 1.05 inch print canvas. Actual vertical
extent scales the wire geometry; label font sizes stay fixed. Export must not
use tight image cropping, which would undo these physical size constraints.

**Include answer boxes** defaults on. Turning it off omits multipart answer
tables and their labels while preserving diagrams, chosen writing space, and
the optional answer key. It is a layout-only setting: Update layout reuses the
same generated questions. Graph multiple-choice options are unaffected.
