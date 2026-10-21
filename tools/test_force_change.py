"""C3 independent valid-change matrix, exact-set checking, artwork, and UI flow."""
import itertools
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from utils.force_change import (
    CASES, CASE_BY_ID, PRACTICE_SETS, ForceState, accepted, available_cases,
    change_description, check_changes, make_options, new_attempt,
    render_change_diagram, submit_attempt,
)

EXPECTED = {
    "start_right": {(2,1),(3,1),(1,0)},
    "start_left": {(0,1),(1,2),(1,3)},
    "add_push": {(1,0),(2,0),(3,0)},
    "add_rope": {(0,1),(0,2),(0,3)},
    "coast_right": {(1,1),(2,2)},
    "coast_left": {(2,2),(1,1)},
    "slow_right": {(0,1),(2,3)},
    "slow_left": {(3,2),(1,0)},
    "faster_right": {(3,1),(2,0)},
    "faster_left": {(0,2),(1,3)},
}


def model_checks():
    assert set(EXPECTED) == set(CASE_BY_ID)
    operations = set()
    count = 0
    for case in CASES:
        for p,t in itertools.product(range(4), repeat=2):
            assert accepted(case, ForceState(p,t)) == ((p,t) in EXPECTED[case.id]), (case.id,p,t)
        for seed in range(30):
            options = make_options(case, random.Random(seed))
            assert len(set(options)) == 4
            assert {o for o in options if accepted(case,o)} == {ForceState(*pair) for pair in EXPECTED[case.id]}
            for o in options:
                assert (o.push != case.initial.push) + (o.pull != case.initial.pull) == 1
                operations.add(change_description(case.initial,o).split()[0])
            for flags in itertools.product((False,True), repeat=4):
                selected=tuple(i for i,flag in enumerate(flags) if flag)
                expected={i for i,o in enumerate(options) if (o.push,o.pull) in EXPECTED[case.id]}
                result=check_changes(case,options,selected)
                assert result["correct"] == (set(selected) == expected)
                assert set(result["missing"]) == expected-set(selected)
                assert set(result["extra"]) == set(selected)-expected
                count += 1
    assert operations == {"Add","Remove","Increase","Reduce"}
    for p,t in itertools.product(range(4), repeat=2):
        state=ForceState(p,t)
        assert state.net == 10*p-10*t
        assert render_change_diagram(state).startswith(b"\x89PNG")
    for bad in ((-1,0),(4,1),(True,1),(1.5,0)):
        try:
            ForceState(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("Invalid force state accepted")
    for context in PRACTICE_SETS:
        assert len(available_cases(context)) >= 2
    attempt=new_attempt("coast_right")
    assert submit_attempt(attempt) and not submit_attempt(attempt)
    attempt["selection"]=tuple(i for i,o in enumerate(attempt["options"]) if (o.push,o.pull) in EXPECTED["coast_right"])
    assert submit_attempt(attempt) and attempt["completed"]
    assert attempt["outcome"] == "Corrected after feedback"
    assert not submit_attempt(attempt)
    print(f"C3 model passed: 10 cases, all 160 case/state combinations, {count} answer sets, four change operations, and all 16 force diagrams.")


def ui_checks():
    from streamlit.testing.v1 import AppTest
    at=AppTest.from_file(str(ROOT/"Home.py"),default_timeout=30)
    at.session_state["practice_auto_load"]=False
    at.run()

    def click(label):
        next(b for b in at.button if b.label==label).click().run()
        assert not at.exception

    def expected():
        attempt=at.session_state["force_change_attempt"]
        return tuple(i for i,o in enumerate(attempt["options"]) if (o.push,o.pull) in EXPECTED[attempt["case_id"]])

    def select(indices,qid=None):
        current=at.session_state["force_change_question_id"]
        at.session_state[f"force_change_cards_{current}"]={"question_id":current if qid is None else qid,"indices":list(indices)}
        at.run()
        assert not at.exception

    click("Dynamics")
    click("Change of State")
    assert next(b for b in at.button if b.label=="Check changes").proto.type == "primary"
    click("Check changes")
    assert at.warning and not at.session_state["force_change_attempt"]["checks"]
    good=expected()
    select([good[0]])
    assert not at.session_state["force_change_attempt"]["checks"]
    click("Check changes")
    assert at.warning and not at.session_state["force_change_attempt"]["completed"]
    click("Check changes")
    assert len(at.session_state["practice_answer_history"])==1
    select([])
    assert at.session_state["force_change_attempt"]["selection"]==()
    select([0],qid=-1)
    assert at.session_state["force_change_attempt"]["selection"]==()
    select(good)
    click("Show interaction hint")
    click("Force and Motion Matching")
    click("Change of State")
    assert at.session_state["force_change_attempt"]["selection"]==good
    click("Check changes")
    assert at.success and any(t.value=="⭐ x 1" for t in at.title)
    assert at.session_state["force_change_attempt"]["outcome"]=="Completed with help"
    select([])
    assert at.session_state["force_change_attempt"]["selection"]==good
    assert len(at.session_state["practice_answer_history"])==2
    assert "Before" in at.session_state["practice_answer_history"][-1]["Diagrams"]
    for context in PRACTICE_SETS:
        at.selectbox(key="force_change_context").set_value(context).run()
        assert not at.exception
        assert CASE_BY_ID[at.session_state["force_change_attempt"]["case_id"]] in available_cases(context)
    click("Try a related case")
    click("Skip question")
    click("Reset practice")
    assert at.session_state["force_change_records"]==[]
    for case in CASES:
        at.session_state["force_change_attempt"]=new_attempt(case.id)
        at.session_state["force_change_question_id"]+=1
        at.run()
        select(expected())
        click("Check changes")
        assert at.success
        at.run()
        assert len(at.session_state["force_change_attempt"]["checks"])==1
    click("Next question")
    qid=at.session_state["force_change_question_id"]
    at.session_state["practice_auto_load"]=True
    at.session_state[f"force_change_cancel_next_{qid}"]=True
    select(expected())
    click("Check changes")
    assert at.session_state["force_change_question_id"]==qid
    at.checkbox(key=f"force_change_cancel_next_{qid}").uncheck().run()
    assert at.session_state["force_change_question_id"]==qid+1
    count=len(at.session_state["force_change_records"])
    at.run()
    assert len(at.session_state["force_change_records"])==count
    print("C3 UI passed: exact-set selection, revisions, hints, stale events, navigation, every case, stars/history, contexts/reset, and shared countdown.")


if __name__=="__main__":
    model_checks()
    ui_checks()
