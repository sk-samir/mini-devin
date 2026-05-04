import streamlit as st

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
        transition: transform 0.15s ease, opacity 0.15s ease;
    }
    .stButton>button:hover {
        opacity: 0.95;
        transform: translateY(-1px);
    }
    .stButton>button:disabled {
        background: #a9b6ff;
        color: #eef0ff;
        box-shadow: none;
        cursor: not-allowed;
        opacity: 0.75;
        pointer-events: none;
        transform: none;
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


def apply_styles():
    st.markdown(PAGE_STYLES, unsafe_allow_html=True)
