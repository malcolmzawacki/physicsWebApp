"""Shared calculator pop-over; interactions rerun only this fragment."""

import streamlit as st

from utils.calculator import calculate

PREFIX = "physics_calculator_"


def _save_mode():
    st.session_state[PREFIX + "saved_mode"] = st.session_state[PREFIX + "mode"]


def _edit(token):
    key = PREFIX + "expression"
    current = st.session_state.get(key, "")
    if token == "clear":
        st.session_state[key] = ""
        st.session_state.pop(PREFIX + "error", None)
    elif token == "backspace":
        st.session_state[key] = current[:-1]
    else:
        st.session_state[key] = (current + token)[:250]
    st.session_state[PREFIX + "draft"] = st.session_state[key]


def _evaluate():
    st.session_state[PREFIX + "draft"] = st.session_state.get(PREFIX + "expression", "")
    expression = st.session_state.get(PREFIX + "expression", "").strip()
    if not expression:
        return
    try:
        result = calculate(expression, st.session_state.get(PREFIX + "mode", "Degrees") == "Degrees",
                           st.session_state.get(PREFIX + "answer", 0))
    except ValueError as exc:
        st.session_state[PREFIX + "error"] = str(exc)
        return
    st.session_state.pop(PREFIX + "error", None)
    st.session_state[PREFIX + "answer"] = result
    history = st.session_state.setdefault(PREFIX + "history", [])
    history.insert(0, (expression, format(result, ".12g"), st.session_state.get(PREFIX + "mode", "Degrees")))
    del history[10:]


@st.fragment
def render_calculator():
    # Navigation may stop a run before these widgets mount. Keep a separate copy
    # because Streamlit cleans up widget-owned keys when that happens.
    st.session_state.setdefault(PREFIX + "expression", st.session_state.get(PREFIX + "draft", ""))
    st.session_state.setdefault(PREFIX + "mode", st.session_state.get(PREFIX + "saved_mode", "Degrees"))
    st.markdown("""<style>
    .st-key-physics_calculator_anchor {
        position: fixed; bottom: 1.25rem; right: 1.5rem;
        width: auto; z-index: 999;
    }
    .st-key-physics_calculator_anchor button[aria-expanded] {
        box-shadow: 0 3px 14px #0002; border-radius: 2rem;
    }
    .st-key-physics_calculator_anchor [data-testid="stPopover"] {width: 160px;}
    .st-key-physics_calculator_body,
    .st-key-physics_calculator_body [data-testid="stVerticalBlock"] {gap: .25rem;}
    [data-testid="stPopoverBody"]:has(.st-key-physics_calculator_body) {
        width: 350px; max-width: calc(100vw - 2rem);
        max-height: calc(100dvh - 7rem);
    }
    .st-key-physics_calculator_body button {min-height: 1.9rem; padding: .1rem .35rem;}
    .st-key-physics_calculator_body h3 {font-size: 1.15rem; padding: 0 0 .3rem;}
    .st-key-physics_calculator_body [data-testid="stCaptionContainer"] p {font-size: .75rem;}
    .st-key-physics_calculator_result {
        background: color-mix(in srgb, currentColor 6%, transparent);
    }
    .st-key-physics_calculator_result [data-testid="stMetricValue"] {
        font-size: 1.65rem; font-weight: 650; line-height: 1.25;
        font-variant-numeric: tabular-nums; overflow-wrap: anywhere;
    }
    @media (max-width: 600px) {
        .st-key-physics_calculator_anchor {bottom: .75rem; right: .75rem;}
    }
    </style>""", unsafe_allow_html=True)
    with st.container(key="physics_calculator_anchor"):
        with st.popover("Calculator", icon=":material/calculate:", width=350), st.container(key="physics_calculator_body"):
            st.markdown("### Scientific calculator")
            st.radio("Angle mode", ["Degrees", "Radians"], horizontal=True,
                     key=PREFIX + "mode", label_visibility="collapsed", on_change=_save_mode)
            st.text_input("Expression", key=PREFIX + "expression", max_chars=250,
                          placeholder="e.g. 12 * sin(30)", on_change=_evaluate)
            if PREFIX + "error" in st.session_state:
                st.error(st.session_state[PREFIX + "error"])
            elif PREFIX + "answer" in st.session_state:
                result = format(st.session_state[PREFIX + "answer"], ".12g")
                with st.container(border=True, key="physics_calculator_result"):
                    st.metric("Result", result)
            else:
                st.caption("Type an expression or use the keypad.")
            rows = [
                [("sin", "sin("), ("cos", "cos("), ("tan", "tan("), ("√", "sqrt(" )],
                [("7", "7"), ("8", "8"), ("9", "9"), ("÷", "/")],
                [("4", "4"), ("5", "5"), ("6", "6"), ("×", "*")],
                [("1", "1"), ("2", "2"), ("3", "3"), ("−", "-")],
                [("0", "0"), (".", "."), ("^", "^"), ("＋", "+")],
                [("(", "("), (")", ")"), ("π", "pi"), ("Ans", "ans")],
            ]
            for index, row in enumerate(rows):
                for column, (label, token) in zip(st.columns(4), row):
                    column.button(label, key=f"{PREFIX}key_{index}_{label}",
                                  on_click=_edit, args=(token,), width="stretch")
            clear, back, equals = st.columns([1, 1, 2])
            clear.button("Clear", key=PREFIX + "clear", on_click=_edit, args=("clear",), width="stretch")
            back.button("⌫", help="Delete last character", key=PREFIX + "back", on_click=_edit,
                        args=("backspace",), width="stretch")
            equals.button("=", key=PREFIX + "equals", on_click=_evaluate, type="primary", width="stretch")
            st.caption("Enter to calculate · Ans recalls the last result")
            with st.expander("Functions & history"):
                st.caption("Use * to multiply. Scientific notation: 3e8. Functions: sqrt, sin, cos, tan, asin, acos, atan, log (base 10), ln, abs. Constants: pi, e.")
                for expression, result, mode in st.session_state.get(PREFIX + "history", []):
                    st.text(f"{expression} = {result} ({mode})")
                if not st.session_state.get(PREFIX + "history"):
                    st.caption("Your last 10 calculations will appear here.")
