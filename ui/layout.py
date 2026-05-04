import streamlit as st

from ui.api import check_backend_health, clear_saved_history, fetch_chat_history, get_ai_response


def render_top_bar():
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


def render_left_column():
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


def render_center_column():
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
        button_label = 'Processing...' if st.session_state.processing else 'Submit question'
        submit_button = st.form_submit_button(button_label, disabled=st.session_state.processing)

        if submit_button:
            if question.strip():
                st.session_state.pending_question = question.strip()
                st.session_state.status_message = 'Processing your request...'
                st.session_state.processing = True
                st.experimental_rerun()
            else:
                st.warning('Please enter a question before submitting.')

    if st.session_state.processing and st.session_state.pending_question:
        with st.spinner('Getting AI response...'):
            try:
                response_text = get_ai_response(st.session_state.pending_question)
                st.session_state.chat.insert(0, ('AI', response_text))
                st.session_state.chat.insert(0, ('You', st.session_state.pending_question))
                st.session_state.status_message = 'Response received successfully.'
            except Exception as exc:
                st.session_state.status_message = f'Unable to fetch response: {exc}'
            finally:
                st.session_state.processing = False
                st.session_state.pending_question = ''
                st.experimental_rerun()

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


def render_right_column():
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


def render_footer():
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
