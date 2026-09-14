# Current Electricity Starter Scope

_Created: 2026-03-30_

This note defines the first-pass scope for a current electricity starter page built around Ohm's law and simple series circuits.

## Instructional Goal

Students should be able to:

- read a simple schematic with a battery and one or two resistors
- identify the givens shown on the diagram and in the side panel
- use `V = IR` to solve for voltage, current, or resistance
- use `R_total = R1 + R2` for a series circuit
- calculate a voltage drop across one resistor in a series circuit

## Initial Scope

Included:

- single-resistor Ohm's law problems
- two-resistor series circuits
- always-visible side-by-side diagram and prompt layout
- schematic-symbol diagrams rendered with `schemdraw` when available

Deferred:

- parallel circuits
- Kirchhoff rule formalism
- power calculations
- realistic breadboard or pictorial wiring diagrams
- multi-loop analysis

## Modeling Assumptions

- Batteries are ideal voltage sources.
- Wires are ideal with negligible resistance.
- Resistors obey Ohm's law exactly.
- Current is the same through each element in one simple series loop.
- Values are chosen for classroom-friendly arithmetic in the starter activity.
- The current generator currently uses curated sets of resistance and current values so answers stay simple and avoid awkward decimals. This is an intentional starter limitation and should be revisited if you want broader randomization later.

## Diagram Approach

- Prefer schematic symbols over pictorial components for the first activity.
- Keep the circuit visible beside the prompt at all times so students can reference labels without scrolling.
- If `schemdraw` is unavailable in the environment, the page should degrade to a textual circuit summary rather than fail during import.
