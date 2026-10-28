# Force activity performance audit — 2026-10-23

## Implemented follow-up

After the baseline investigation below, the teacher authorized speed-ups while
preserving the student experience. Routine save responses now carry an ordered
record-ID acknowledgement plus only records the server does not already hold.
Initial hydration and generation resets still send full snapshots. A 30-answer
test using synthetic image data measured 10,500 bytes of acknowledgements versus
18,718,440 bytes under the old protocol with the same records. This excludes
initial hydration and outbound new-answer data; it is not total network traffic.
Full browser history and review diagrams remain intact. Tests cover restoration,
cross-tab deltas, resets/expiry, invalid responses, quota and blocked storage.

The three card-matching pages now reconcile component state before rendering,
with tests confirming one execution per selection, current board state,
deselection and rejection of stale events. Existing interaction checks still
cover scoring, feedback, hints, completion and representation switching. The
countdown animation/deadline/cancel behavior was deliberately left unchanged.
The new persistence and one-execution tests run in Correctness Guardrails.

## Baseline investigation (before the changes above)

The current implementation has avoidable overhead that could make an unreliable
connection or a busy shared server more noticeable. This audit does not establish
the cause of the classroom interruptions: the deployed revision, hosting metrics,
school connection and student devices were not measured. No activity behavior or
progress-storage protocol was changed during this investigation.

## Strongest finding: growing progress uploads

`utils/progress_storage.py` sends only unacknowledged answer records **to the
browser**, but `utils/progress_storage_frontend/storage.js:62` publishes the
**entire** saved snapshot back to the server whenever an answer changes it.
That includes all saved base64 diagrams, including earlier answers. Hydration
after a refresh also uploads the complete saved history, as intended for review.

A synthetic session with five checks in each of six force activities, using
mixed motion graphs for Force and Motion Matching, produced:

| Application data | Measured/modelled size |
| --- | ---: |
| Final 30-check history JSON | 1,518,345 bytes |
| Same text represented as UTF-16, before browser accounting overhead | 3,036,690 bytes |
| Sum of full-history response payloads over those 30 saves | 18,707,295 bytes |

These are illustrative synthetic payloads, not captured network bytes. The
calculation excludes initial hydration, protocol overhead and any transport
compression. Forty students with that same history would produce approximately
748 MB of these upload payloads over the session, not at once. Retries add records.
Different randomly generated diagrams and text-only motion mode change the sizes.

The browser also reads, validates and serializes the whole history synchronously
on saving/polling. The saved history grows toward browser storage limits. Existing
quota-failure handling warns and preserves live-session work; no quota failure was
observed in this audit. Exact limits and runtime costs on Chromebooks are unmeasured.

The browser-saving feature appears in commit `bda6cf8` dated 2026-10-23. It is a
candidate for today's issue only if that revision was deployed during class.

First optimization: acknowledge IDs/metadata for records already held by the
server, and send only missing records back. Retain full initial hydration,
cross-tab merging, fixed expiry, reset generations, code retention and offline/
quota recovery. Reusing image assets across history rows and reducing synchronous
serialization are separate follow-ups; don't silently drop answer-review diagrams.

## Countdown traffic

`utils/activity_flow.py:44` requests a progress update approximately every 50 ms.
A deterministic fake-clock run of the real helper counted **102 progress calls**
for a five-second countdown. Streamlit may batch/coalesce these; this is not a
count of physical network packets. The five-second wait is intentional, but this
many updates is unnecessary for a student-facing countdown. The loop occupies the
session's script thread while waiting; it does not freeze every other session.

Second optimization: reduce to a few visible steps per second while preserving
the five-second deadline, cancellation and exactly-once advancement. A browser
timer could reduce traffic further but needs its own flow/cancellation review.

## Two activity executions for one card selection

Instrumented Streamlit AppTests found **two activity executions per selection**
in Force and Motion Matching, Match the Free-Body Diagram and Change of State.
Each handles the component event, updates state, and explicitly reruns the page.
Local warm selections took about 0.019–0.020 seconds, excluding browser and network
work. The cost is small on this desktop but redundant across many concurrent users.
This does not mean two separate browser/server round trips are required.

Third optimization: reconcile the component's selection before rendering the
board, keeping fresh question IDs, deselection, locked answers and stale-event
handling. Verify rapid clicks and switching representations before removing the
extra rerun; the current frontend/server synchronization must not regress.

## Image size and server rendering

Representative uncompressed application payloads (JSON arrays of base64 PNGs):

| Example set | PNG count | Encoded payload | Uncached render time here |
| --- | ---: | ---: | ---: |
| Match FBD | 4 | 65,144 bytes | 1.139 s, includes first Matplotlib startup |
| Builder | 1 | 7,746 bytes | 0.022 s |
| Motion, text (reference only) | 1 | 15,178 bytes | 0.013 s |
| Motion, dots including reference | 5 | 62,094 bytes | 0.080 s |
| Motion, mixed graphs including reference | 5 | 104,566 bytes | 0.095 s |
| Change of State including reference | 5 | 68,726 bytes | 0.063 s |
| Ranking review images | 4 | 55,724 bytes | 0.055 s |
| Ranking's additional live versions | 4 | 21,832 bytes | 0.049 s |

The motion reference and builder images use native Streamlit media URLs; the
clickable choice images are inline base64. The table counts complete example
image sets, not exact per-click wire transfers. Native media can be cached by the
browser; inline images remain part of each component argument payload. The card
frontend already avoids rebuilding/redecoding unchanged images on selection.

Matplotlib runs on the **server**. Chromebooks display static images and a small
local card interface, with no physics simulation, chart animation or remote chart
library. A motion graph set is not individually huge, but cold rendering and unique
ranking/builder variants can compete for shared hosting CPU and cache memory.
Existing `st.cache_data` decorators help repeated diagrams. Ranking currently
renders both review and live variants before an answer is checked; the review
variants could be deferred until submission. Cache entry limits deserve review
under realistic traffic, especially for varied builder drafts/ranking boards.

The local Streamlit 1.49 configuration reported websocket compression disabled.
Production settings may differ. Enabling compression is not a substitute for
removing redundant payloads and must be measured against server CPU costs.

## What to measure next

Use the actual deployed build with a class-sized concurrent run and shaped
bandwidth/latency. Compare early versus late-session latency and text versus graph
mode. Record disconnects/reconnects, server CPU/memory, payload sizes and browser
long tasks. A warm single-desktop preview cannot establish school readiness.

During diagnosis, switching automatic loading off reduces countdown traffic;
text motion mode reduces diagram transfers. Refresh restores saved answers on the
current implementation, but resets the in-progress question and transfers saved
history again, so it is not a performance fix.

The baseline measurements above used local synthetic inputs only. No student
progress was inspected or exported. Temporary measurement files are not required
to run the regression checks in `tools/test_progress_storage.py`,
`tools/test_progress_storage_frontend.js`, and `tools/test_force_card_updates.py`.
