# Optional projectile diagrams

Projectiles uses the shared, initially collapsed **Diagram** expander. Students
can open it independently of Organizing help. Horizontal launches, same-height
landings, elevated launches (including launches behind the edge), and landings
on a cliff are supported.

`projectile_payload` creates `diagram_data` from the explicit printed `givens`
and the wording's scene cues. It does not pass answers, supporting calculations,
or the organizer's solved `values` to the renderer. Unknown quantities have no
numeric labels; computed components, flight times, and peak heights are omitted
unless explicitly given. Printed distances are drawn between their stated
endpoints: a distance from the cliff base is distinct from total flight range.
The first time at cliff height is marked on the ascending part of the path.

`utils/projectile_diagrams.py` reconstructs a physical trajectory using only the
printed givens and g=10. Calculated values control geometry but never become
numeric labels. There are no coordinate ticks or numbered axes. Approximate
unknown proportions are visible; this is the intended visual scaffolding.
The existing worksheet diagram option renders the same figure.

Absolute distances do not determine image size. The renderer normalizes the
total range to a fixed drawing width. If the flight's vertical extent divided
by range is between 0.08 and 1.0, it uses equal horizontal and vertical scales,
preserving proportions and angles. Matplotlib's equal aspect setting ensures
that this is also true in screen pixels, rather than just data coordinates.

Outside that band, only the vertical direction is adjusted, by the smallest
factor needed to reach the nearest bound. The full parabola remains visible,
with the same relative horizontal event positions and vertical heights. A bold
note states that vertical distances are enlarged or compressed and by how much;
a second line states that the axes use different scales and angles are not to
scale. Velocity arrows follow the displayed trajectory. Numeric angle labels
still report the given physical angle. Labels use a separate area to prevent
extreme proportions from pushing them off the page.

For example, a 100 m horizontal-launch cliff and 1,000,000 m range would receive
800× vertical enlargement. A 100 m cliff and 400 m range preserve equal scales.
Changing either case's absolute size by a common factor does not change its
layout. The thresholds are named constants and can be tuned after student review.

Validation: `tools/test_projectile_diagrams.py` checks scene/target coverage,
physical/pixel scale, extreme ratios, hidden-data isolation and worksheet rendering.
`tools/test_projectile_setup.py` checks given/target separation for sampled
problems and the collapsed expander alongside the organizer's form lifecycle.
