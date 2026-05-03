import streamlit as st
import requests
import logging
import time
from typing import List, Dict

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

PAGE_STYLES = """
<style>
    :root {
        color-scheme: light;
    }
    .stApp {
        background: linear-gradient(180deg, #eef4ff 0%, #f8fbff 55%, #ffffff 100%);
        color: #0f1733;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
    }
    .hero-container {
        background: radial-gradient(circle at top left, rgba(59, 107, 255, 0.14), transparent 35%),
                    radial-gradient(circle at bottom right, rgba(139, 73, 255, 0.14), transparent 30%),
                    #ffffff;
        border: 1px solid #d7e2fb;
        border-radius: 26px;
        padding: 1.6rem 1.8rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 22px 46px rgba(64, 95, 173, 0.08);
    }
    .hero-title {
        font-size: clamp(2.4rem, 4vw, 3.4rem);
        font-weight: 800;
        letter-spacing: -0.05em;
        margin-bottom: 0.5rem;
        color: #10264f;
    }
    .hero-subtitle {
        font-size: clamp(1rem, 1.2vw, 1.2rem);
        line-height: 1.75;
        color: #2b3a62;
        max-width: 860px;
        margin-bottom: 1.6rem;
    }
    .hero-cards {
        display: grid;
        grid-template-columns: repeat(3, minmax(200px, 1fr));
        gap: 1rem;
    }
    .hero-card {
        background: #f7f9ff;
        border: 1px solid #dbe4f7;
        border-radius: 22px;
        padding: 1.2rem 1.25rem;
        min-height: 120px;
    }
    .hero-card h3 {
        margin: 0;
        font-size: 0.95rem;
        font-weight: 700;
        color: #1f3d72;
    }
    .hero-card p {
        margin: 0.75rem 0 0;
        font-size: 1.5rem;
        font-weight: 700;
        color: #10264f;
    }
    .chat-box,
    .history-card,
    .summary-card {
        background: #ffffff;
        border: 1px solid #d7e2fb;
        border-radius: 24px;
        padding: 26px;
        box-shadow: 0 26px 52px rgba(64, 95, 173, 0.07);
    }
    .chat-entry {
        border-radius: 18px;
        padding: 20px;
        margin-bottom: 18px;
        line-height: 1.7;
        font-size: 1rem;
    }
    .user-msg {
        background: #e8f0ff;
        border-left: 4px solid #3b6bff;
        color: #10264f;
    }
    .ai-msg {
        background: #f4edff;
        border-left: 4px solid #8b49ff;
        color: #2d1b58;
    }
    .chat-entry strong {
        display: block;
        margin-bottom: 0.75rem;
    }
    .status-pill {
        display: inline-flex;
        align-items: center;
        border-radius: 999px;
        padding: 10px 16px;
        margin-bottom: 1rem;
        font-weight: 700;
        font-size: 0.95rem;
    }
    .status-pill.healthy { background: #e6f6ea; color: #116d33; }
    .status-pill.warning { background: #fff4e6; color: #9d5a00; }
    .status-pill.offline { background: #ffe8ea; color: #881d2f; }
    .status-card {
        background: #ffffff;
        border: 1px solid #d7e2fb;
        border-radius: 24px;
        padding: 22px;
        box-shadow: 0 26px 52px rgba(64, 95, 173, 0.08);
        margin-bottom: 1.2rem;
    }
    .status-card h3 {
        margin-top: 0;
        margin-bottom: 0.75rem;
    }
    .status-card p {
        margin-bottom: 1rem;
        color: #40547b;
    }
    .status-card .stButton>button {
        width: 100%;
        margin-top: 0.55rem;
    }
    .stButton>button {
        border-radius: 14px;
        background: linear-gradient(135deg, #3b6bff, #8b49ff);
        color: #ffffff;
        border: none;
        padding: 0.95rem 1.5rem;
        font-weight: 700;
        box-shadow: 0 12px 28px rgba(59, 107, 255, 0.16);
    }
    .stButton>button:hover {
        opacity: 0.95;
    }
    .top-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 1rem;
        background: linear-gradient(135deg, #eef2ff 0%, #f8f4ff 100%);
        border: 1px solid #dbe4f7;
        border-radius: 24px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.2rem;
        box-shadow: 0 20px 48px rgba(59, 78, 160, 0.12);
        backdrop-filter: blur(10px);
        min-height: 140px;
    }
    .top-bar-left {
        flex: 1.8;
    }
    .top-bar-right {
        flex: 1;
        display: flex;
        justify-content: flex-end;
        align-items: center;
    }
    .top-bar-title {
        margin: 0;
        font-size: 1.85rem;
        font-weight: 900;
        letter-spacing: -0.04em;
        color: #111827;
    }
    .top-bar-subtitle {
        margin: 0.4rem 0 0;
        color: #475569;
        line-height: 1.65;
        max-width: 540px;
    }
    .top-bar-label {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        color: #4f46e5;
        font-weight: 700;
        margin-top: 0.75rem;
    }
    .quick-actions-container {
        position: relative;
        text-align: right;
        width: 100%;
    }
    .quick-actions-container .stButton>button {
        width: 100%;
        border-radius: 16px;
        background: linear-gradient(135deg, #1d4ed8, #7c3aed);
        color: #ffffff;
        border: none;
        padding: 0.95rem 1rem;
        font-weight: 700;
        box-shadow: 0 12px 24px rgba(59, 78, 160, 0.16);
    }
    .quick-actions-container .stButton>button:hover {
        opacity: 0.95;
        transform: translateY(-1px);
    }
    .quick-actions-menu {
        display: block;
        position: absolute;
        right: 0;
        top: 100%;
        background: #ffffff;
        border: 1px solid #d7e2fb;
        border-radius: 18px;
        padding: 14px;
        width: 240px;
        margin-top: 0.9rem;
        box-shadow: 0 24px 48px rgba(64, 95, 173, 0.16);
        z-index: 10;
    }
    .quick-actions-menu.hidden {
        display: none;
    }
    .quick-actions-menu .stButton>button {
        width: 100%;
        border-radius: 14px;
        background: #eff6ff;
        color: #1d4ed8;
        border: 1px solid transparent;
        text-align: left;
        padding: 0.85rem 0.95rem;
        margin-bottom: 0.6rem;
        font-weight: 700;
    }
    .quick-actions-menu .stButton>button:hover {
        background: #e0f2fe;
        border-color: #bfdbfe;
    }
    .feature-section {
        display: grid;
        gap: 1rem;
    }
    .feature-card {
        background: linear-gradient(180deg, #ffffff 0%, #f7faff 100%);
        border: 1px solid #c7d2fe;
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 20px 40px rgba(59, 78, 160, 0.08);
    }
    .feature-card h3 {
        margin-top: 0;
        margin-bottom: 0.75rem;
        color: #1e293b;
    }
    .feature-card p {
        margin: 0;
        color: #475569;
        line-height: 1.75;
    }
    .feature-icon {
        font-size: 1.35rem;
        margin-right: 0.75rem;
    }
    .summary-card h3,
    .history-card h3 {
        margin-top: 0;
    }
    .ui-footer {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        justify-content: space-between;
        color: #50638d;
        font-size: 0.95rem;
        padding-top: 12px;
    }
    .ui-footer a {
        color: #3b6bff;
        text-decoration: none;
    }
    .history-item-collapsed {
        background: #f8f9ff;
        border: 1px solid #dbe4f7;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    .history-item-collapsed:hover {
        background: #eef2ff;
        border-color: #c7d2fe;
    }
    .history-item-expanded {
        background: #ffffff;
        border: 1px solid #dbe4f7;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 12px rgba(64, 95, 173, 0.08);
    }
    @media (max-width: 950px) {
        .hero-cards {
            grid-template-columns: repeat(2, minmax(180px, 1fr));
        }
    }
    @media (max-width: 700px) {
        .hero-card,
        .chat-box,
        .history-card,
        .summary-card {
            padding: 20px;
        }
        .hero-cards {
            grid-template-columns: 1fr;
        }
        .stApp {
            padding: 0 12px;
        }
        .stButton>button {
            width: 100%;
        }
        .history-item-collapsed,
        .history-item-expanded {
            padding: 12px;
        }
    }
</style>
"""

st.markdown(PAGE_STYLES, unsafe_allow_html=True)
logger.info('Mini Devin UI started')

if 'chat' not in st.session_state:
    st.session_state.chat = []
    logger.debug('Initialized chat session state')

if 'history' not in st.session_state:
    st.session_state.history = []

if 'expanded_history' not in st.session_state:
    st.session_state.expanded_history = set()

if 'show_quick_actions' not in st.session_state:
    st.session_state.show_quick_actions = False

if 'status_message' not in st.session_state:
    st.session_state.status_message = ''

if 'processing' not in st.session_state:
    st.session_state.processing = False

API_BASE_URL = 'http://127.0.0.1:8001'


def fetch_chat_history(limit: int = 20) -> List[Dict]:
    try:
        start_time = time.time()
        response = requests.get(f'{API_BASE_URL}/history', params={'limit': limit}, timeout=6)
        response.raise_for_status()
        history = response.json()
        
        # Deduplicate by message, keeping the first occurrence (assuming backend returns latest first)
        seen_messages = set()
        unique_history = []
        for entry in history:
            message = entry.get('message', '')
            if message not in seen_messages:
                seen_messages.add(message)
                unique_history.append(entry)
        
        logger.info(f'Loaded history in {time.time() - start_time:.2f}s: {len(history)} records, {len(unique_history)} unique')
        return unique_history
    except requests.RequestException as exc:
        logger.error(f'Failed to load history: {exc}')
        return []


def clear_saved_history() -> bool:
    try:
        response = requests.delete(f'{API_BASE_URL}/history', timeout=6)
        if response.status_code == 200:
            logger.info('Saved chat history cleared successfully')
            return True
        logger.warning(f'Failed to clear history: HTTP {response.status_code}')
        return False
    except requests.RequestException as exc:
        logger.error(f'Error clearing history: {exc}')
        return False


def check_backend_health() -> str:
    try:
        response = requests.get(f'{API_BASE_URL}/health', timeout=5)
        if response.status_code == 200:
            return 'healthy'
        return 'warning'
    except requests.RequestException:
        return 'offline'


def get_ai_response(question: str) -> str:
    try:
        start_time = time.time()
        response = requests.get(f'{API_BASE_URL}/ask', params={'question': question}, timeout=60)
        response.raise_for_status()
        data = response.json()
        logger.info(f'Backend answered in {time.time() - start_time:.2f}s')
        return data.get('response', 'No answer returned from backend.')
    except requests.RequestException as exc:
        logger.error(f'AI response error: {exc}')
        raise


st.markdown('<div class="top-bar">', unsafe_allow_html=True)
bar_left, bar_right = st.columns([3, 1], gap='medium')

with bar_left:
    st.markdown('<div class="top-bar-left">', unsafe_allow_html=True)
    st.markdown('<h1 class="top-bar-title">Mini Devin AI Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<div class="top-bar-label">Production-ready assistant workspace</div>', unsafe_allow_html=True)
    st.markdown('<p class="top-bar-subtitle">A compact workspace for fast chat, smart history review, and clear backend status.</p>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with bar_right:
    st.markdown('<div class="quick-actions-container">', unsafe_allow_html=True)
    if st.button('⚡ Quick Actions', key='quick_actions_toggle', help='Click to show available actions'):
        st.session_state.show_quick_actions = not st.session_state.show_quick_actions

    menu_classes = 'quick-actions-menu' if st.session_state.show_quick_actions else 'quick-actions-menu hidden'
    st.markdown(f'<div class="{menu_classes}">', unsafe_allow_html=True)
    if st.session_state.show_quick_actions:
        if st.button('Refresh history', key='refresh_history'):
            st.session_state.history = fetch_chat_history()
            st.success('Chat history refreshed')
        if st.button('Clear saved history', key='clear_history'):
            if clear_saved_history():
                st.session_state.history = []
                st.success('Saved history cleared')
            else:
                st.error('Could not clear saved history')
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

main_col1, main_col2, main_col3 = st.columns([1.2, 2.4, 1.2], gap='large')

with main_col1:
    st.markdown('<div class="status-card">', unsafe_allow_html=True)
    st.markdown('### System status', unsafe_allow_html=True)
    backend_health = check_backend_health()
    if backend_health == 'healthy':
        st.markdown('<div class="status-pill healthy">✅ Backend Connected</div>', unsafe_allow_html=True)
    elif backend_health == 'warning':
        st.markdown('<div class="status-pill warning">⚠️ Backend responded with issues</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="status-pill offline">❌ Backend Unreachable</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="feature-section">', unsafe_allow_html=True)
    st.markdown('<div class="feature-card"><div><span class="feature-icon">⚡</span><strong>Fast response</strong></div><p>Instant AI answers with intelligent context and quick follow-up readiness.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-card"><div><span class="feature-icon">🧭</span><strong>Clear guidance</strong></div><p>Structured recommendations and practical next steps so outcomes are easy to act on.</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-card"><div><span class="feature-icon">🗂️</span><strong>History + status</strong></div><p>Saved conversations, backend connectivity, and actionable status information in one view.</p></div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="status-card">', unsafe_allow_html=True)
    st.markdown('### About Devin', unsafe_allow_html=True)
    st.markdown('Mini Devin is built for modern teams who need accurate AI guidance, fast SQL and code help, and a clean workspace to manage conversations.', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with main_col2:
    st.markdown('<div class="chat-box">', unsafe_allow_html=True)
    st.markdown('### AI Conversation')
    st.markdown('Ask your question and see the response instantly. The chat box is placed for quick access without scrolling.', unsafe_allow_html=True)

    with st.form(key='question_form_main'):
        question = st.text_area(
            'Send a request to Mini Devin',
            height=160,
            max_chars=820,
            placeholder='Ask for SQL, code explanation, or product guidance...',
            help='Use clear, complete sentences for the best results.',
            label_visibility='visible'
        )
        submit_button = st.form_submit_button('Submit question', disabled=st.session_state.processing)

        if submit_button:
            if question.strip():
                st.session_state.status_message = 'Processing your request...'
                st.session_state.processing = True
                try:
                    with st.spinner('Getting AI response...'):
                        response_text = get_ai_response(question.strip())
                    st.session_state.chat.insert(0, ('AI', response_text))
                    st.session_state.chat.insert(0, ('You', question.strip()))
                    st.session_state.status_message = 'Response received successfully.'
                    st.session_state.processing = False
                except Exception as exc:
                    st.session_state.status_message = f'Unable to fetch response: {exc}'
                    st.session_state.processing = False
            else:
                st.warning('Please enter a question before submitting.')

    if st.session_state.status_message:
        st.info(st.session_state.status_message)

    if st.session_state.chat:
        for role, message in st.session_state.chat:
            style_class = 'user-msg' if role == 'You' else 'ai-msg'
            st.markdown(
                f'<div class="chat-entry {style_class}"><strong>{role}</strong>{message}</div>',
                unsafe_allow_html=True
            )
    else:
        st.info('Your conversation will appear here once you submit a message.')

    st.markdown('</div>', unsafe_allow_html=True)

with main_col3:
    st.markdown('<div class="history-card">', unsafe_allow_html=True)
    st.markdown('### Saved chat history')

    if not st.session_state.history:
        st.session_state.history = fetch_chat_history()

    if st.session_state.history:
        for i, entry in enumerate(st.session_state.history):
            entry_id = f"history_{i}"
            user_question = entry.get('message', '-')
            ai_response = entry.get('response', '-')
            created_at = entry.get('created_at', '')

            if st.button(
                f"💬 {user_question[:60]}{'...' if len(user_question) > 60 else ''}",
                key=f"toggle_{entry_id}",
                help="Click to expand/collapse this conversation"
            ):
                if entry_id in st.session_state.expanded_history:
                    st.session_state.expanded_history.remove(entry_id)
                else:
                    st.session_state.expanded_history.add(entry_id)

            if entry_id in st.session_state.expanded_history:
                st.markdown('<div class="history-item-expanded">', unsafe_allow_html=True)
                st.markdown(f'**You asked:** {user_question}')
                st.markdown(f'**AI responded:** {ai_response}')
                if created_at:
                    st.caption(f"🕒 {created_at}")
                st.markdown('</div>', unsafe_allow_html=True)
            else:
                if created_at:
                    st.caption(f"🕒 {created_at}")
                st.markdown('---')
    else:
        st.write('No saved chat history is available at this time.')


    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('---')
st.markdown('## What you can do with Devin')
st.markdown(
    '- Ask for SQL query generation and execution guidance.  \
' 
    '- Request code explanations and debugging help.  \
' 
    '- Review saved conversations and keep your workflow organized.'
)

st.markdown('<div class="ui-footer">', unsafe_allow_html=True)
st.markdown('Built for clarity, accessibility, and modern AI workflows.', unsafe_allow_html=True)
st.markdown('Powered by Mini Devin and your backend API.', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
