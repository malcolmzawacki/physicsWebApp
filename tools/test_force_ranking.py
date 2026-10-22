"""C10 exact ranking physics, generator promises, ties/gaps, and routed lifecycle."""
from fractions import Fraction
import itertools
from pathlib import Path
import random
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from utils.force_ranking import (
    COMPARISONS,MASS_PATTERNS,QUANTITIES,RankCase,check_ranking,
    expected_groups,make_board,ranking_text,ranking_value,render_rank_diagram,
)


def model_checks():
    board=(RankCase(40,10,1),RankCase(60,0,4),RankCase(10,40,2),RankCase(20,20,3))
    truth={
        ("Net force",COMPARISONS[0]):"B > A = C > D",
        ("Acceleration",COMPARISONS[0]):"A > B = C > D",
        ("Net force",COMPARISONS[1]):"B > A > D > C",
        ("Acceleration",COMPARISONS[1]):"A > B > D > C",
    }
    for mode,text in truth.items():
        assert ranking_text(expected_groups(board,*mode))==text
    assert check_ranking(board,(1,3,3,4),"Acceleration",COMPARISONS[0])["correct"]
    assert not check_ranking(board,(2,1,2,4),"Acceleration",COMPARISONS[0])["correct"]
    assert ranking_value(RankCase(10,0,3),"Acceleration",COMPARISONS[0])==Fraction(10,3)
    triple=(RankCase(20,0,1),RankCase(30,10,2),RankCase(40,20,3),RankCase(10,0,4))
    assert check_ranking(triple,(1,1,1,4),"Net force",COMPARISONS[0])["correct"]
    zeros=tuple(RankCase(10*m,10*m,m) for m in range(1,5))
    assert check_ranking(zeros,(1,1,1,1),"Acceleration",COMPARISONS[1])["correct"]
    boards=0; rankings=0
    for quantity,comparison,masses,ties in itertools.product(QUANTITIES,COMPARISONS,MASS_PATTERNS,(False,True)):
        for seed in range(100):
            cases=make_board(quantity,comparison,masses,ties,random.Random(seed))
            assert len(set(cases))==4
            assert (len({c.mass for c in cases})==1)==(masses==MASS_PATTERNS[0])
            # Independent values calculated from displayed integer givens.
            values=[]
            for c in cases:
                v=Fraction(c.push-c.pull,1 if quantity=="Net force" else c.mass)
                values.append(abs(v) if comparison==COMPARISONS[0] else v)
                assert v==ranking_value(c,quantity,COMPARISONS[1])
            assert len(set(values))==(3 if ties else 4)
            desired=tuple(tuple(i for i,v in enumerate(values) if v==value) for value in sorted(set(values),reverse=True))
            if seed<5:
                for ranks in itertools.product(range(1,5),repeat=4):
                    entered=tuple(tuple(i for i,r in enumerate(ranks) if r==rank) for rank in sorted(set(ranks)))
                    assert check_ranking(cases,ranks,quantity,comparison)["correct"]==(min(ranks)==1 and entered==desired)
                    rankings+=1
            boards+=1
    for mass,push,pull in itertools.product(range(1,5),(0,10,60),(0,10,60)):
        c=RankCase(push,pull,mass)
        assert render_rank_diagram(c,60).startswith(b"\x89PNG")
    for ranks in ((None,1,2,3),(True,1,2,3),(0,1,2,3),(5,1,2,3),(1,2,3)):
        try:
            check_ranking(board,ranks,"Net force",COMPARISONS[0])
        except ValueError:
            pass
        else:
            raise AssertionError("Malformed ranking accepted")
    print(f"Ranking model passed: {boards} controlled boards, {rankings} rank assignments, independent force/acceleration and signed/magnitude counterexamples, and 36 diagrams.")


def ui_checks():
    from streamlit.testing.v1 import AppTest
    at=AppTest.from_file(str(ROOT/"Home.py"),default_timeout=30)
    at.session_state["practice_auto_load"]=False
    at.run()

    def click(label):
        next(b for b in at.button if b.label==label).click().run()
        assert not at.exception

    def set_ranks(correct=True):
        attempt=at.session_state["force_ranking_attempt"]
        qid=at.session_state["force_ranking_question_id"]
        groups=expected_groups(attempt["cases"],*attempt["settings"][:2])
        ranks={i:r for r,group in enumerate(groups,1) for i in group}
        for i in range(4):
            at.selectbox(key=f"force_ranking_rank_{qid}_{i}").set_value(ranks[i] if correct else 1)

    click("Dynamics")
    click("Net Force and Acceleration Ranking")
    # Numerical givens remain readable page text, independent of image scaling.
    visible_text = "\n".join(item.value for item in at.markdown)
    for case in at.session_state["force_ranking_attempt"]["cases"]:
        assert f"P = {case.push} N" in visible_text
        assert f"T = {case.pull} N" in visible_text
    assert next(b for b in at.button if b.label=="Check ranking").proto.type=="primary"
    click("Check ranking")
    assert at.warning and not at.session_state["force_ranking_attempt"]["checks"]
    set_ranks(False)
    click("Check ranking")
    assert at.warning and len(at.session_state["practice_answer_history"])==1
    click("Check ranking")
    assert len(at.session_state["practice_answer_history"])==1
    click("Show ranking hint")
    click("Change of State")
    click("Net Force and Acceleration Ranking")
    qid=at.session_state["force_ranking_question_id"]
    assert all(at.selectbox(key=f"force_ranking_rank_{qid}_{i}").value==1 for i in range(4))
    set_ranks()
    click("Check ranking")
    assert at.success and any(t.value=="⭐ x 1" for t in at.title)
    assert at.session_state["force_ranking_attempt"]["outcome"]=="Completed with help"
    before=at.session_state["force_ranking_attempt"]["cases"]
    click("Rank the same cases by the other quantity")
    assert at.session_state["force_ranking_attempt"]["cases"]==before
    assert at.session_state["force_ranking_attempt"]["settings"][0]=="Acceleration"
    assert at.session_state["force_ranking_attempt"]["draft"]==(None,)*4
    assert at.session_state["force_ranking_transferred"]
    click("Skip question")
    assert "force_ranking_transferred" not in at.session_state
    for quantity,comparison,masses,ties in itertools.product(QUANTITIES,COMPARISONS,MASS_PATTERNS,(False,True)):
        at.selectbox(key="force_ranking_quantity").set_value(quantity).run()
        at.selectbox(key="force_ranking_comparison").set_value(comparison).run()
        at.selectbox(key="force_ranking_masses").set_value(masses).run()
        at.checkbox(key="force_ranking_ties").set_value(ties).run()
        assert not at.exception
        set_ranks()
        click("Check ranking")
        assert at.success
        assert next(b for b in at.button if b.label=="Check ranking").disabled
        count=len(at.session_state["practice_answer_history"])
        at.run()
        assert len(at.session_state["practice_answer_history"])==count
        click("Next question")
    click("Reset practice")
    assert at.session_state["force_ranking_records"]==[]
    assert not at.session_state["force_ranking_attempt"]["checks"]
    qid=at.session_state["force_ranking_question_id"]
    at.session_state["practice_auto_load"]=True
    at.session_state[f"force_ranking_cancel_next_{qid}"]=True
    set_ranks()
    click("Check ranking")
    assert at.session_state["force_ranking_question_id"]==qid
    at.checkbox(key=f"force_ranking_cancel_next_{qid}").uncheck().run()
    assert at.session_state["force_ranking_question_id"]==qid+1
    count=len(at.session_state["force_ranking_records"])
    at.run()
    assert len(at.session_state["force_ranking_records"])==count
    print("Ranking UI passed: incomplete/duplicate checks, tied ranks, hints/drafts, all 16 settings, stars/history, same-case quantity comparison, reset, and countdown.")


if __name__=="__main__":
    model_checks()
    ui_checks()
