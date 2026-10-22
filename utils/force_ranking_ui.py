"""C10 rank selectors with ties, explicit signed/magnitude modes, and revision."""
import streamlit as st

from utils.activity_flow import next_question_countdown
from utils.force_motion_match_ui import data_url
from utils.force_ranking import (
    COMPARISONS, MASS_PATTERNS, QUANTITIES, new_attempt, ranking_text,
    ranking_value, render_rank_diagram, submit_attempt,
)
from utils.session_progress import record_answer
from utils.ui_components import render_header
from utils.ui_state import State


@st.cache_data(show_spinner=False)
def ranking_image(case,scale,include_values=True):
    """Keep printable givens in saved images and use page text for live cards."""
    return render_rank_diagram(case,scale,include_values=include_values)


def render_force_ranking():
    state=State("force_ranking")
    state.ensure("records",[])
    state.ensure("question_id",0)

    def start(settings):
        if state.has("attempt"):
            state.set("records",[*state.get("records"),state.get("attempt")])
        state.inc("question_id")
        state.set("attempt",new_attempt(*settings))
        state.pop("transferred")

    render_header("Net Force and Acceleration Ranking",sum(bool(r.get("completed")) for r in [*state.get("records"),state.get("attempt",{})]))
    st.html("""<style>
    [class*="st-key-force_ranking_"] [data-baseweb="select"] > div {
        min-height:3rem; border:2px solid #7c8798;
    }
    [class*="st-key-force_ranking_"] [data-baseweb="select"] * {
        font-size:1.15rem; font-weight:600;
    }
    [class*="st-key-force_ranking_rank_"] [data-testid="stWidgetLabel"] p {
        font-size:1.05rem; font-weight:600;
    }
    body:has(.st-key-force_ranking_quantity) [role="option"] {
        font-size:1.15rem;
    }
    .st-key-force_ranking_equations .katex { font-size:1.4em; }
    </style>""")
    a,b=st.columns(2)
    with a:
        quantity=st.selectbox("Rank by",QUANTITIES,key=state.key("quantity"))
    with b:
        comparison=st.selectbox("Compare",COMPARISONS,key=state.key("comparison"))
    with st.expander("Practice settings"):
        masses=st.selectbox("Masses",MASS_PATTERNS,key=state.key("masses"))
        ties=st.checkbox("Include tied values in new questions",value=True,key=state.key("ties"))
    settings=(quantity,comparison,masses,ties)
    if not state.has("attempt") or state.get("attempt")["settings"] != settings:
        start(settings)
    attempt=state.get("attempt")
    qid=state.get("question_id")
    cases=attempt["cases"]
    st.write("Rank the four cases from **greatest to least**. **1 means greatest**; equal values receive the same rank. Gaps between ranks are fine.")
    if comparison == COMPARISONS[0]:
        st.info(f"Compare {quantity.lower()} magnitudes: ignore left/right signs. Equal strengths in opposite directions tie.")
    else:
        st.info(f"Compare signed {quantity.lower()}: right is positive and left is negative. For example, −2 is greater than −6.")
    st.caption("Each cart stays on a level, frictionless track. Air resistance is neglected. P is the rightward push; T is the leftward rope pull. N and W balance vertically. Use g = 10 m/s². All diagrams use one arrow scale.")
    if attempt["hint_used"]:
        st.info("Subtract the leftward pull from the rightward push. For acceleration, divide each case's net force by its own mass. If ranking magnitudes, take absolute values before comparing. A larger net force does not always mean a larger acceleration when masses differ.")
    scale=max(max(c.push,c.pull,10*c.mass) for c in cases)
    images=[data_url(ranking_image(c,scale)) for c in cases]
    for col,letter,case,image in zip(st.columns(4),"ABCD",cases,images):
        with col:
            with st.container(border=True):
                st.markdown(f"**Case {letter} · {case.mass} kg**")
                st.image(ranking_image(case,scale,include_values=False),width="stretch")
                st.markdown(f"**P = {case.push} N →**  \n**T = {case.pull} N ←**")
    with st.expander("Text descriptions of diagrams"):
        for letter,case in zip("ABCD",cases):
            st.write(f"**{letter}:** {case.description}")
    with st.form(state.key(f"form_{qid}")):
        ranks=[]
        for i,(col,letter) in enumerate(zip(st.columns(4),"ABCD")):
            with col:
                state.ensure(f"rank_{qid}_{i}",attempt["draft"][i])
                ranks.append(st.selectbox(f"Rank for {letter}",[None,1,2,3,4],
                             format_func=lambda r: "Choose rank" if r is None else str(r),
                             placeholder="Rank…",key=state.key(f"rank_{qid}_{i}"),disabled=attempt["completed"]))
        a,b=st.columns(2)
        with a:
            checked=st.form_submit_button("Check ranking",type="primary",disabled=attempt["completed"],width="stretch")
        with b:
            hinted=st.form_submit_button("Show ranking hint",disabled=attempt["completed"],width="stretch")
    if hinted:
        attempt["hint_used"]=True
        attempt["draft"]=tuple(ranks)
        state.set("attempt",attempt)
        st.rerun()
    if checked:
        if any(r is None for r in ranks):
            st.warning("Choose a rank for every case before checking. This has not counted as an attempt.")
        elif submit_attempt(attempt,ranks):
            last=attempt["checks"][-1]
            record_answer("Net Force and Acceleration Ranking",f"Rank {quantity.lower()} by {comparison.lower()}, greatest to least.",
                          {letter:r for letter,r in zip("ABCD",ranks)},ranking_text(last["groups"]),last["correct"],
                          explanation="Compare net force first; divide by mass when ranking acceleration. Equal values must tie.",
                          diagrams=dict(zip("ABCD",images)))
            state.set("attempt",attempt)
            st.rerun()
    if attempt["checks"]:
        last=attempt["checks"][-1]
        st.caption("Feedback describes the last checked ranks. Submit again after changing ranks.")
        if last["correct"]:
            st.success("Correct — the ordering and ties match. ⭐")
            st.write(ranking_text(last["groups"]))
        else:
            st.warning("Revise your ranking and check again.")
            for message in last["feedback"]:
                st.write(message)
        with st.expander("Values used for this check"):
            unit="N" if quantity == "Net force" else "m/s²"
            for letter,case in zip("ABCD",cases):
                st.write(f"{letter}: Fₓ = {case.push} − {case.pull} = {case.net} N; m = {case.mass} kg; ranked value = {ranking_value(case,quantity,comparison)} {unit}.")
    with st.container(key=state.key("equations")):
        with st.expander("Equation reference"):
            more=st.checkbox("More Equations",key=state.key("more_equations"))
            st.latex(r"F_{\mathrm{net},x}=m a_x")
            if more:
                st.latex(r"F_{\mathrm{net},x}=P-T,\qquad a_x=\frac{P-T}{m}")

    def next_question():
        if state.get("question_id")==qid:
            start(settings)

    def related():
        if state.get("question_id")==qid:
            # Same physical cases: isolate the effect of switching F_net ↔ a.
            state.set("quantity",QUANTITIES[1] if quantity==QUANTITIES[0] else QUANTITIES[0])
            state.set("records",[*state.get("records"),attempt])
            state.inc("question_id")
            next_settings=(state.get("quantity"),comparison,masses,ties)
            next_attempt=new_attempt(*next_settings)
            next_attempt["cases"]=cases
            # Ties are guaranteed only for newly generated boards. Preserve the
            # physical comparison even when a target switch changes which cases tie.
            state.set("attempt",next_attempt)
            state.set("transferred",True)

    if state.get("transferred"):
        st.caption("Related comparison: the same four carts, now ranked by the other quantity. Their ties may change.")
    a,b=st.columns(2)
    with a:
        st.button("Next question" if attempt["completed"] else "Skip question",key=state.key(f"next_{qid}"),on_click=next_question,width="stretch")
    with b:
        st.button("Rank the same cases by the other quantity",key=state.key(f"related_{qid}"),on_click=related,width="stretch")
    with st.expander("Your Performance"):
        st.caption("This session only. One star per completed board; duplicate checks do not add attempts. Ties and rank gaps are accepted when the ordering is correct.")
        st.dataframe([{"Quantity":r["settings"][0],"Comparison":r["settings"][1],"Checks":len(r["checks"]),
                       "Hint used":r["hint_used"],"Result":r["outcome"] or ("In progress" if r is attempt else "Skipped")}
                      for r in [*state.get("records"),attempt]],hide_index=True,width="stretch")

        def reset():
            state.set("records",[])
            state.pop("attempt")
            state.pop("transferred")
        st.button("Reset practice",key=state.key("reset"),on_click=reset)
    if attempt["completed"]:
        def advance():
            next_question()
            st.rerun()
        next_question_countdown(state,qid,advance,seconds=5)
