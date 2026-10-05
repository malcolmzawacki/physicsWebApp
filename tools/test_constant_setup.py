"""Constant Speed rollout: explicit checks, target changes, unsupported branches."""
import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from streamlit.testing.v1 import AppTest
from utils.setup_schema import expected_entries
from utils.solve_for import target_options
from utils.generators.kinematics.const_motion_generator import ConstantMotionGenerator


def main():
    at=AppTest.from_file(str(ROOT/'Home.py'),default_timeout=25).run()
    next(b for b in at.sidebar.button if b.label=='Kinematics').click().run()
    next(b for b in at.sidebar.button if b.label=='Constant Motion').click().run()
    for target in target_options(ConstantMotionGenerator(),'Constant Speed','Easy'):
        at.selectbox(key='const_motion__solve_for_select').select(target['id']).run()
        assert not at.exception
        qid=at.session_state['const_motion__question_id']
        expected=expected_entries(at.session_state['const_motion__payload'].extras['setup'])
        for key,value in expected.items():
            at.text_input(key=f'const_motion__setup_input_{qid}_{key}').set_value(str(value))
        at.run()
        assert not at.success  # No correctness feedback until deliberate submission.
        next(b for b in at.button if b.label=='Check setup').click().run()
        assert not at.exception and len(at.success)==3
        assert at.session_state['const_motion__question_id']==qid
        assert not at.session_state['const_motion__submitted']
        numeric=[key for key,value in expected.items() if not isinstance(value,str)]
        target_key=next(key for key,value in expected.items() if value=='?')
        at.text_input(key=f'const_motion__setup_input_{qid}_{target_key}').set_value(str(expected[numeric[0]])).run()
        assert any('changed' in c.value for c in at.caption)
        next(b for b in at.button if b.label=='Check setup').click().run()
        assert len(at.error)==1
        assert any('matches another given' in m.value for m in at.markdown)
    for kind in ('Average Speed','Average Velocity','Combined Constant Motion'):
        at.selectbox(key='const_motion__problem_type_select_unified').select(kind).run()
        assert not at.exception
        assert not any(e.label=='Organizing help' for e in at.expander)
        assert not any(b.label=='Check setup' for b in at.button)
    at.selectbox(key='const_motion__problem_type_select_unified').select('Constant Speed').run()
    assert not at.exception
    assert any(e.label=='Organizing help' for e in at.expander)
    assert at.session_state['const_motion__setup_submission'] is None
    assert not any(at.session_state['const_motion__setup_draft'].values())
    print('Constant Speed rollout passed: targets, deliberate checking, feedback, and type transitions.')

if __name__=='__main__':
    main()
