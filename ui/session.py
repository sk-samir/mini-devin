import streamlit as st


def init_session_state():
    defaults = {
        'chat': [],
        'history': [],
        'expanded_history': set(),
        'show_quick_actions': False,
        'status_message': '',
        'processing': False,
        'pending_question': ''
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
