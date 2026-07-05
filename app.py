"""OmniVerse AI — Main Streamlit Application."""

import streamlit as st

from backend import database as db
from backend.file_handler import ensure_dirs
from frontend.pages import (
    render_ai_analysis,
    render_dashboard,
    render_home,
    render_login,
    render_profile,
    render_reports,
    render_settings,
    render_upload,
)
from frontend.styles import apply_theme

# ── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="OmniVerse AI",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Initialize ───────────────────────────────────────────────────────────────
ensure_dirs()
db.init_db()

# ── Session State Defaults ───────────────────────────────────────────────────
defaults = {
    "user": None,
    "page": "Home",
    "theme": "light",
    "current_upload": None,
    "chat_history": [],
    "last_summary": None,
}
for key, val in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = val

# Restore theme preference for logged-in users on first load
if st.session_state.user and "theme_loaded" not in st.session_state:
    st.session_state.theme = db.get_user_theme(st.session_state.user["id"])
    st.session_state.theme_loaded = True

apply_theme(st.session_state.theme)

# ── Navigation ───────────────────────────────────────────────────────────────
PUBLIC_PAGES = {"Home", "Login"}
AUTH_PAGES = {
    "Dashboard",
    "Upload",
    "AI Analysis",
    "Reports",
    "Profile",
    "Settings",
}

if st.session_state.user is None and st.session_state.page in AUTH_PAGES:
    st.session_state.page = "Login"

# ── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<p class="nav-brand">🌐 OmniVerse AI</p>', unsafe_allow_html=True)
    st.markdown("---")

    if st.session_state.user:
        st.caption(f"Signed in as **{st.session_state.user['username']}**")
        nav_items = [
            ("Dashboard", "🏠"),
            ("Upload", "📤"),
            ("AI Analysis", "🔬"),
            ("Reports", "📊"),
            ("Profile", "👤"),
            ("Settings", "⚙️"),
        ]
        for page_name, icon in nav_items:
            if st.button(f"{icon} {page_name}", use_container_width=True, key=f"nav_{page_name}"):
                st.session_state.page = page_name
                st.rerun()

        st.markdown("---")
        if st.button("🚪 Logout", use_container_width=True):
            for key in ["user", "current_upload", "chat_history", "last_summary", "theme_loaded"]:
                st.session_state[key] = defaults.get(key)
            st.session_state.page = "Home"
            st.rerun()
    else:
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.page = "Home"
            st.rerun()
        if st.button("🔑 Login", use_container_width=True):
            st.session_state.page = "Login"
            st.rerun()

# ── Route to Page ────────────────────────────────────────────────────────────
page = st.session_state.page

if page == "Home":
    render_home()
elif page == "Login":
    render_login()
elif page == "Dashboard":
    render_dashboard()
elif page == "Upload":
    render_upload()
elif page == "AI Analysis":
    render_ai_analysis()
elif page == "Reports":
    render_reports()
elif page == "Profile":
    render_profile()
elif page == "Settings":
    render_settings()
else:
    st.session_state.page = "Home"
    st.rerun()
