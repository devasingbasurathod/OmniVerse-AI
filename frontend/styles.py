"""Theme and CSS styling for dark/light mode."""

import streamlit as st


def get_theme_css(theme="light"):
    """Return custom CSS for the selected theme."""
    is_dark = theme == "dark"

    bg = "#0f172a" if is_dark else "#f8fafc"
    card = "#1e293b" if is_dark else "#ffffff"
    text = "#f1f5f9" if is_dark else "#0f172a"
    muted = "#94a3b8" if is_dark else "#64748b"
    accent = "#6366f1"
    accent_hover = "#4f46e5"
    border = "#334155" if is_dark else "#e2e8f0"

    return f"""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

        html, body, [class*="css"] {{
            font-family: 'Inter', sans-serif;
        }}

        .stApp {{
            background-color: {bg};
        }}

        .main-header {{
            background: linear-gradient(135deg, {accent} 0%, #8b5cf6 100%);
            padding: 2rem;
            border-radius: 16px;
            color: white;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
        }}

        .main-header h1 {{
            margin: 0;
            font-size: 2rem;
            font-weight: 700;
        }}

        .main-header p {{
            margin: 0.5rem 0 0 0;
            opacity: 0.9;
            font-size: 1rem;
        }}

        .stat-card {{
            background: {card};
            border: 1px solid {border};
            border-radius: 12px;
            padding: 1.25rem;
            text-align: center;
            box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        }}

        .stat-card h3 {{
            color: {muted};
            font-size: 0.85rem;
            font-weight: 500;
            margin: 0 0 0.5rem 0;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}

        .stat-card .value {{
            color: {accent};
            font-size: 2rem;
            font-weight: 700;
            margin: 0;
        }}

        .feature-card {{
            background: {card};
            border: 1px solid {border};
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            transition: transform 0.2s, box-shadow 0.2s;
        }}

        .feature-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(99, 102, 241, 0.15);
        }}

        .feature-card h4 {{
            color: {text};
            margin: 0 0 0.5rem 0;
            font-size: 1.1rem;
        }}

        .feature-card p {{
            color: {muted};
            margin: 0;
            font-size: 0.9rem;
            line-height: 1.5;
        }}

        .nav-brand {{
            font-size: 1.3rem;
            font-weight: 700;
            color: {accent};
            padding: 0.5rem 0;
        }}

        .chat-user {{
            background: {accent};
            color: white;
            padding: 0.75rem 1rem;
            border-radius: 12px 12px 4px 12px;
            margin: 0.5rem 0;
            max-width: 80%;
            margin-left: auto;
        }}

        .chat-bot {{
            background: {card};
            border: 1px solid {border};
            color: {text};
            padding: 0.75rem 1rem;
            border-radius: 12px 12px 12px 4px;
            margin: 0.5rem 0;
            max-width: 80%;
        }}

        div[data-testid="stSidebar"] {{
            background-color: {card};
            border-right: 1px solid {border};
        }}

        .stButton > button {{
            background: {accent};
            color: white;
            border: none;
            border-radius: 8px;
            font-weight: 500;
            transition: background 0.2s;
        }}

        .stButton > button:hover {{
            background: {accent_hover};
            color: white;
        }}
    </style>
    """


def apply_theme(theme="light"):
    """Inject theme CSS into the page."""
    st.markdown(get_theme_css(theme), unsafe_allow_html=True)
