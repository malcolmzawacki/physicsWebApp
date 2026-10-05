"""Momentum prompt facts and end-to-end organizing-help checks."""
import sys
from pathlib import Path
from unittest.mock import patch
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from utils.generators.momentum_generators.momentum import MomentumGenerator
from utils.problem_payload import payload_from_dict
from utils.setup_schema import expected_entries
from utils.solve_for import generate_selected
from streamlit.testing.v1 import AppTest


def main():
    generator=MomentumGenerator()
    for target,role in [("momentum","p"),("mass","m"),("velocity","v")]:
        with patch("utils.generators.momentum_generators.momentum.random.randint", side_effect=[3,8]):
            payload=payload_from_dict(generate_selected(generator,"Momentum","Easy","momentum-q."+target))
        facts=expected_entries(payload.extras["setup"])
        assert facts=={key: "?" if key==role else value for key,value in {"p":24,"m":3,"v":8}.items()}
        assert payload.answers==[{"p":24,"m":3,"v":8}[role]]
        for key,phrase in {"p":"24 Ns","m":"3 kg","v":"8 m/s"}.items():
            assert (phrase in payload.question)==(key!=role)
    at=AppTest.from_file(str(ROOT/'Home.py'),default_timeout=25).run()
    at.session_state['router_section']='Momentum'
    at.session_state['router_activity']='Momentum'
    at.run()
    for target in ('momentum','mass','velocity'):
        at.selectbox(key='momentum_solve_for_select').select('momentum-q.'+target).run()
        assert not at.exception
        qid=at.session_state['momentum_question_id']
        forms = [node.proto.form for node in at.get('form')]
        setup_form = next(form for form in forms if form.form_id == f'momentum_setup_form_{qid}')
        assert setup_form.enter_to_submit and not setup_form.clear_on_submit
        assert any(form.form_id == 'momentum_form' for form in forms)
        expected=expected_entries(at.session_state['momentum_payload'].extras['setup'])
        for key,value in expected.items():
            at.text_input(key=f'momentum_setup_input_{qid}_{key}').set_value(str(value))
        at.run()
        assert not at.success
        next(b for b in at.button if b.label=='Check setup').click().run()
        assert not at.exception and len(at.success)==3
        assert not at.session_state['momentum_submitted']
        assert at.session_state['momentum_question_id']==qid
        target_key=next(key for key,value in expected.items() if value=='?')
        given=next(value for value in expected.values() if not isinstance(value,str))
        at.text_input(key=f'momentum_setup_input_{qid}_{target_key}').set_value(str(given)).run()
        assert any('changed' in c.value for c in at.caption)
        next(b for b in at.button if b.label=='Check setup').click().run()
        assert len(at.error)==1
        assert any('matches another given' in m.value for m in at.markdown)
        assert not any('start or the end' in m.value for m in at.markdown)
    next(b for b in at.button if b.label=='New Question').click().run()
    assert at.session_state['momentum_setup_submission'] is None
    assert not any(at.session_state['momentum_setup_draft'].values())
    # Final answer remains independent and advances normally.
    answer=at.session_state['momentum_correct_answers'][0]
    final=next(i for i in at.text_input if 'setup_input' not in i.key)
    final.set_value(str(answer))
    qid=at.session_state['momentum_question_id']
    next(b for b in at.button if b.label=='Submit').click().run()
    assert not at.exception
    assert at.session_state['momentum_question_id']==qid+1
    print('Momentum: prompt facts, all targets, deliberate checks, feedback, reset, and final-answer flow passed.')

if __name__=='__main__':
    main()
