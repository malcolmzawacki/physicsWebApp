"""Restore, merge, reset and serialization checks independent of browser timing."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from utils import progress_storage as storage


def row(record_id="one"):
    return {"_record_id": record_id, "Date": "2026-10-22", "Activity": "Motion",
            "Result": "Correct", "Question": {"prompt": "How far?"}, "Your answer": "5 m",
            "Correct answer": "5 m", "Equations": [], "Diagrams": {},
            "Difficulty": "Easy", "Explanation": "Distance."}


def snapshot():
    return {"version": 1, "generation": "first", "code": "1234-5678-9012-3456",
            "expires_at": 1792771200000, "history": [row()]}


class StorageTests(unittest.TestCase):
    def setUp(self):
        self.state = {}
        self.context = patch.object(storage.st, "session_state", self.state)
        self.context.start()
        self.addCleanup(self.context.stop)

    def test_restore_preserves_all_existing_fields_and_code(self):
        saved = snapshot()
        self.assertTrue(storage.accept_snapshot(saved))
        self.assertEqual(self.state[storage.HISTORY_KEY], saved["history"])
        self.assertEqual(self.state[storage.CODE_KEY], saved["code"])
        self.assertFalse(storage.accept_snapshot(saved))

    def test_optional_problem_type_round_trips_with_legacy_records(self):
        saved = snapshot()
        typed = {**row("typed"), "Problem type": "Type 2"}
        saved["history"].append(typed)
        self.assertTrue(storage.accept_snapshot(saved))
        self.assertEqual(storage.history_for_storage(), saved["history"])
        self.assertNotIn("Problem type", self.state[storage.HISTORY_KEY][0])
        self.assertEqual(self.state[storage.HISTORY_KEY][1]["Problem type"], "Type 2")
        for bad in (None, 123, [], {}):
            invalid = deepcopy(saved)
            invalid["history"][1]["Problem type"] = bad
            self.assertFalse(storage.valid_snapshot(invalid))

    def test_late_restore_merges_work_without_duplicates(self):
        self.state[storage.HISTORY_KEY] = [row("two")]
        storage.accept_snapshot(snapshot())
        self.assertEqual([r["_record_id"] for r in self.state[storage.HISTORY_KEY]], ["one", "two"])
        storage.accept_snapshot(snapshot())
        self.assertEqual(len(self.state[storage.HISTORY_KEY]), 2)

    def test_clear_or_expiry_generation_drops_stale_session_data(self):
        storage.accept_snapshot(snapshot())
        reset = {**snapshot(), "generation": "reset", "history": [], "code": "0000-0000-0000-0001"}
        storage.accept_snapshot(reset)
        self.assertEqual(self.state[storage.HISTORY_KEY], [])
        self.assertEqual(self.state[storage.CODE_KEY], reset["code"])

    def test_expiry_clears_history_without_changing_code(self):
        saved = snapshot()
        storage.accept_snapshot(saved)
        expired = {**saved, "generation": "next-window", "history": []}
        self.assertTrue(storage.accept_snapshot(expired))
        self.assertEqual(self.state[storage.HISTORY_KEY], [])
        self.assertEqual(self.state[storage.CODE_KEY], saved["code"])

    def test_numpy_values_serialize_and_ids_stay_stable(self):
        import numpy as np
        value = row()
        value.pop("_record_id")
        value["Question"] = {"distance": np.float64(5), "values": np.array([1, 2])}
        self.state[storage.HISTORY_KEY] = [value]
        serialized = storage.history_for_storage()
        self.assertEqual(serialized[0]["Question"], {"distance": 5, "values": [1, 2]})
        self.assertEqual(serialized, storage.history_for_storage())

    def test_acknowledged_records_are_not_resent(self):
        self.state[storage.HISTORY_KEY] = [row("saved"), row("new")]
        self.assertEqual(storage.history_for_storage({"saved"}), [row("new")])
        self.assertEqual(storage.history_for_storage({"saved", "new"}), [])

    def test_invalid_saved_data_does_not_replace_live_history(self):
        self.state[storage.HISTORY_KEY] = [row("live")]
        for field, bad in [("version", 2), ("code", "bad"), ("history", [{}])]:
            saved = deepcopy(snapshot())
            saved[field] = bad
            self.assertFalse(storage.accept_snapshot(saved))
        saved = snapshot()
        saved["history"][0]["Diagrams"] = {"image": "data:image/png;base64,not base64"}
        self.assertFalse(storage.accept_snapshot(saved))
        self.assertEqual(self.state[storage.HISTORY_KEY], [row("live")])

    def test_incremental_acknowledges_local_answer_without_echoed_diagram(self):
        saved = snapshot()
        storage.accept_snapshot(saved)
        local = row("new")
        local["Diagrams"] = {"Force": "data:image/png;base64,YWJj"}
        self.state[storage.HISTORY_KEY].append(local)
        event = {"delta": True, "record_ids": ["one", "new"],
                 "snapshot": {**saved, "history": []}, "saved": True}
        self.assertFalse(storage.accept_storage_event(event))
        self.assertEqual(self.state[storage.STATE_KEY]["history"], [row(), local])
        self.assertEqual(storage.history_for_storage({"one", "new"}), [])

    def test_incremental_cross_tab_rows_merge_with_pending_local_work(self):
        saved = snapshot()
        storage.accept_snapshot(saved)
        self.state[storage.HISTORY_KEY].append(row("local"))
        event = {"delta": True, "record_ids": ["one", "other"],
                 "snapshot": {**saved, "history": [row("other")]}}
        self.assertTrue(storage.accept_storage_event(event))
        self.assertEqual([r["_record_id"] for r in self.state[storage.HISTORY_KEY]], ["one", "other", "local"])
        self.assertEqual(storage.history_for_storage({"one", "other"}), [row("local")])
        self.assertFalse(storage.accept_storage_event(event), "duplicate response must not duplicate answers")

    def test_incremental_local_numpy_answer_is_normalized(self):
        import numpy as np
        saved = snapshot()
        storage.accept_snapshot(saved)
        numeric = row("numeric")
        numeric["Question"] = {"values": np.array([1, 2])}
        numeric["Your answer"] = np.array([3, 4])
        self.state[storage.HISTORY_KEY].append(numeric)
        event = {"delta": True, "record_ids": ["one", "numeric"],
                 "snapshot": {**saved, "history": []}}
        self.assertFalse(storage.accept_storage_event(event))
        restored = self.state[storage.HISTORY_KEY][-1]
        self.assertEqual(restored["Question"], {"values": [1, 2]})
        self.assertEqual(restored["Your answer"], [3, 4])

    def test_invalid_delta_does_not_change_progress(self):
        saved = snapshot()
        storage.accept_snapshot(saved)
        for ids, incoming, generation in [(["missing"], [], "first"),
                                          (["one", "one"], [], "first"),
                                          ([True], [], "first"),
                                          (["one"], [], "wrong"),
                                          (["one", "bad"], [{}], "first")]:
            event = {"delta": True, "record_ids": ids,
                     "snapshot": {**saved, "generation": generation, "history": incoming}}
            self.assertFalse(storage.accept_storage_event(event))
            self.assertEqual(self.state[storage.HISTORY_KEY], [row()])

    def test_generation_reset_and_legacy_full_response_still_work(self):
        storage.accept_snapshot(snapshot())
        reset = {**snapshot(), "generation": "reset", "history": []}
        self.assertTrue(storage.accept_storage_event({"snapshot": reset, "delta": False}))
        self.assertEqual(self.state[storage.HISTORY_KEY], [])
        self.assertTrue(storage.accept_storage_event({"snapshot": snapshot()}))
        self.assertEqual(self.state[storage.HISTORY_KEY], [row()])


if __name__ == "__main__":
    unittest.main()
