import logging

import streamlit as st
from ui.api import fetch_chat_history, clear_saved_history, check_backend_health, get_ai_response
from ui.layout import render_center_column, render_left_column, render_right_column, render_footer, render_top_bar
from ui.session import init_session_state
from ui.styles import apply_styles

# Initialize logging for UI
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ui')

st.set_page_config(
    page_title='Mini Devin AI Assistant',
    page_icon='🤖',
    layout='wide',
    initial_sidebar_state='expanded'
)

apply_styles()
logger.info('Mini Devin UI started')

init_session_state()

render_top_bar()

main_col1, main_col2, main_col3 = st.columns([1.2, 2.4, 1.2], gap='large')

with main_col1:
    render_left_column()

with main_col2:
    render_center_column()

with main_col3:
    render_right_column()

render_footer()
