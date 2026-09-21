"""Permanent identities for custom activities that bypass generator metadata.

Keep keys fixed when editing labels; append old labels to aliases on a rename.
Generator-based activities declare the same id/aliases fields in stored_metadata.
"""
CUSTOM_PROGRESS = {
    "electricity.ohm.single-resistor": {"label": "Single Resistor", "aliases": ["Single Resistor"]},
    "electricity.ohm.series-current": {"label": "Series Current", "aliases": ["Series Current"]},
    "electricity.ohm.voltage-drop": {"label": "Voltage Drop", "aliases": ["Voltage Drop"]},
    "electricity.series.resistance": {"label": "Series Equivalent Resistance", "aliases": ["Series Equivalent Resistance"]},
    "electricity.series.current": {"label": "Series Total Current", "aliases": ["Series Total Current"]},
    "electricity.parallel.resistance": {"label": "Parallel Equivalent Resistance", "aliases": ["Parallel Equivalent Resistance"]},
    "electricity.parallel.current": {"label": "Parallel Branch Current", "aliases": ["Parallel Branch Current"]},
    "static.conduction": {"label": "Charging by Conduction", "aliases": ["Charging by Conduction"]},
    "static.induction": {"label": "Charging by Induction", "aliases": ["Charging by Induction"]},
    "static.friction.comparison": {"label": "Comparison Practice", "aliases": ["Comparison Practice"]},
    "static.friction.ranking": {"label": "Ranking Logic Puzzle", "aliases": ["Ranking Logic Puzzle"]},
    "motion.graph-matching": {"label": "Matching Motion Graphs", "aliases": ["Matching Motion Graphs"]},
}


def custom_progress_id(label):
    for identity, entry in CUSTOM_PROGRESS.items():
        if label == entry["label"] or label in entry["aliases"]:
            return identity
    return label


def migrate_custom_progress(performance):
    for old in list(performance):
        identity = custom_progress_id(old)
        if identity == old:
            continue
        previous = performance.pop(old)
        target = performance.setdefault(identity, {})
        for difficulty, stats in previous.items():
            bucket = target.setdefault(difficulty, {"attempts": 0, "correct": 0})
            for metric in ("attempts", "correct"):
                bucket[metric] += stats.get(metric, 0)
    return performance


def progress_label(identity):
    return CUSTOM_PROGRESS.get(identity, {}).get("label", identity)
