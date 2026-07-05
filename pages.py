"""Streamlit page renderers."""

from datetime import datetime
from pathlib import Path

import streamlit as st

from backend import ai_engine, auth, charts, database as db, file_handler
from frontend.components import chat_message, feature_card, page_header, stat_card


def render_home():
    """Home landing page."""
    page_header("OmniVerse AI", "Upload, analyze, and chat with your data — powered by AI")

    col1, col2, col3 = st.columns(3)
    with col1:
        feature_card("📁 Smart Upload", "CSV, Excel, PDF, and images — all in one place.")
    with col2:
        feature_card("🤖 AI Analysis", "Instant summaries, charts, and insights from your files.")
    with col3:
        feature_card("💬 File Chatbot", "Ask questions about your uploaded data in plain English.")

    st.markdown("---")
    st.subheader("How It Works")
    steps = st.columns(4)
    labels = [
        ("1️⃣", "Sign Up", "Create your free account"),
        ("2️⃣", "Upload", "Add CSV, Excel, PDF, or image"),
        ("3️⃣", "Analyze", "Get AI summary and charts"),
        ("4️⃣", "Report", "Save and download insights"),
    ]
    for col, (icon, title, desc) in zip(steps, labels):
        with col:
            st.markdown(f"### {icon} {title}")
            st.caption(desc)

    st.markdown("---")
    c1, c2, c3 = st.columns([1, 1, 1])
    with c2:
        if st.button("Get Started →", use_container_width=True, type="primary"):
            st.session_state.page = "Login"


def render_login():
    """Login page."""
    page_header("Welcome Back", "Sign in to your OmniVerse AI account")

    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign In", use_container_width=True)
            if submitted:
                if not username or not password:
                    st.error("Please enter username and password.")
                else:
                    ok, result = auth.login_user(username, password)
                    if ok:
                        st.session_state.user = {
                            "id": result["id"],
                            "username": result["username"],
                            "email": result["email"],
                            "full_name": result["full_name"],
                        }
                        st.session_state.theme = db.get_user_theme(result["id"])
                        st.session_state.theme_loaded = True
                        st.session_state.page = "Dashboard"
                        st.rerun()
                    else:
                        st.error(result)

    with tab2:
        with st.form("register_form"):
            full_name = st.text_input("Full Name")
            username = st.text_input("Username", key="reg_user")
            email = st.text_input("Email")
            password = st.text_input("Password", type="password", key="reg_pass")
            confirm = st.text_input("Confirm Password", type="password")
            submitted = st.form_submit_button("Create Account", use_container_width=True)
            if submitted:
                if password != confirm:
                    st.error("Passwords do not match.")
                else:
                    ok, msg = auth.register_user(username, email, password, full_name)
                    if ok:
                        st.success(msg + " Please log in.")
                    else:
                        st.error(msg)

    if st.button("← Back to Home"):
        st.session_state.page = "Home"
        st.rerun()


def render_dashboard():
    """Main dashboard."""
    user = st.session_state.user
    stats = db.get_dashboard_stats(user["id"])
    uploads = db.get_user_uploads(user["id"])

    page_header(
        f"Hello, {user.get('full_name') or user['username']}! 👋",
        "Your data analysis command center",
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        stat_card("Total Uploads", stats["uploads"])
    with c2:
        stat_card("Reports Generated", stats["reports"])
    with c3:
        stat_card("Account", user["username"])

    st.markdown("---")
    st.subheader("Quick Actions")
    a1, a2, a3 = st.columns(3)
    with a1:
        if st.button("📤 Upload File", use_container_width=True):
            st.session_state.page = "Upload"
            st.rerun()
    with a2:
        if st.button("🔬 AI Analysis", use_container_width=True):
            st.session_state.page = "AI Analysis"
            st.rerun()
    with a3:
        if st.button("📊 View Reports", use_container_width=True):
            st.session_state.page = "Reports"
            st.rerun()

    st.markdown("---")
    st.subheader("Recent Uploads")
    if uploads:
        for u in uploads[:5]:
            cols = st.columns([3, 1, 1])
            with cols[0]:
                st.write(f"**{u['filename']}**")
            with cols[1]:
                st.caption(u["file_type"].upper())
            with cols[2]:
                st.caption(u["uploaded_at"][:10])
    else:
        st.info("No uploads yet. Upload a file to get started!")


def render_upload():
    """File upload page."""
    page_header("Upload File", "Supported: CSV, Excel, PDF, PNG, JPG, GIF, WebP")

    uploaded = st.file_uploader(
        "Choose a file",
        type=["csv", "xlsx", "xls", "pdf", "png", "jpg", "jpeg", "gif", "webp"],
    )

    if uploaded:
        st.success(f"Selected: **{uploaded.name}** ({uploaded.size / 1024:.1f} KB)")

        if st.button("Upload & Preview", type="primary"):
            user_id = st.session_state.user["id"]
            path, file_type = file_handler.save_uploaded_file(uploaded, user_id)
            if path is None:
                st.error(file_type)
            else:
                upload_id = db.save_upload(user_id, uploaded.name, path, file_type)
                preview = file_handler.get_preview_data(path, file_type)
                st.session_state.current_upload = {
                    "id": upload_id,
                    "filename": uploaded.name,
                    "path": path,
                    "type": file_type,
                    "preview": preview,
                }
                st.session_state.chat_history = []
                st.success("File uploaded successfully!")
                _render_preview(preview, uploaded.name)

        if st.session_state.get("current_upload"):
            st.markdown("---")
            cu = st.session_state.current_upload
            _render_preview(cu["preview"], cu["filename"])

    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Dashboard"):
            st.session_state.page = "Dashboard"
            st.rerun()
    with col2:
        if st.session_state.get("current_upload"):
            if st.button("Continue to AI Analysis →", type="primary"):
                st.session_state.page = "AI Analysis"
                st.rerun()


def _render_preview(preview, filename):
    """Show file preview based on type."""
    st.subheader(f"Preview: {filename}")
    kind = preview["kind"]

    if kind == "dataframe":
        st.dataframe(preview["data"].head(20), use_container_width=True)
        st.caption(f"Showing first 20 of {len(preview['data'])} rows")
    elif kind == "text":
        st.text_area("Document Text", preview["data"][:3000], height=300)
    elif kind == "image":
        st.image(preview["data"], caption=filename, use_container_width=True)
    else:
        st.warning("Preview not available for this file type.")


def render_ai_analysis():
    """AI summary, charts, and chatbot."""
    cu = st.session_state.get("current_upload")
    if not cu:
        st.warning("No file selected. Upload a file first.")
        if st.button("Go to Upload"):
            st.session_state.page = "Upload"
            st.rerun()
        return

    page_header("AI Analysis", f"Analyzing: {cu['filename']}")

    tab1, tab2, tab3 = st.tabs(["📝 AI Summary", "📊 Charts", "💬 Chatbot"])

    with tab1:
        if st.button("Generate Summary", type="primary"):
            summary = ai_engine.generate_summary(cu["preview"], cu["filename"])
            st.session_state.last_summary = summary
            st.markdown(summary)

        if st.session_state.get("last_summary"):
            st.markdown("---")
            st.markdown(st.session_state.last_summary)

        if st.button("Save as Report"):
            summary = st.session_state.get("last_summary") or ai_engine.generate_summary(
                cu["preview"], cu["filename"]
            )
            report_name = f"report_{cu['filename']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            report_path = file_handler.REPORTS_DIR / report_name
            file_handler.ensure_dirs()
            report_path.write_text(summary, encoding="utf-8")
            db.save_report(
                st.session_state.user["id"],
                cu["id"],
                f"Analysis: {cu['filename']}",
                summary,
                str(report_path),
            )
            st.success(f"Report saved: {report_name}")

    with tab2:
        if cu["preview"]["kind"] == "dataframe":
            df = cu["preview"]["data"]
            numeric = charts.get_numeric_columns(df)
            categorical = charts.get_categorical_columns(df)

            st.subheader("Auto Chart")
            auto_fig = charts.auto_chart(df)
            if auto_fig:
                st.plotly_chart(auto_fig, use_container_width=True)

            st.subheader("Custom Chart")
            chart_type = st.selectbox(
                "Chart Type",
                ["Bar", "Line", "Scatter", "Histogram", "Pie"],
            )
            all_cols = df.columns.tolist()

            if chart_type == "Bar":
                x = st.selectbox("X Axis", all_cols)
                y = st.selectbox("Y Axis (optional)", ["—"] + numeric)
                y_col = None if y == "—" else y
                st.plotly_chart(charts.build_bar_chart(df, x, y_col), use_container_width=True)
            elif chart_type == "Line" and len(numeric) >= 1:
                x = st.selectbox("X Axis", all_cols, key="line_x")
                y = st.selectbox("Y Axis", numeric, key="line_y")
                st.plotly_chart(charts.build_line_chart(df, x, y), use_container_width=True)
            elif chart_type == "Scatter" and len(numeric) >= 2:
                x = st.selectbox("X Axis", numeric, key="sc_x")
                y = st.selectbox("Y Axis", numeric, key="sc_y")
                color = st.selectbox("Color (optional)", ["—"] + categorical)
                color_col = None if color == "—" else color
                st.plotly_chart(
                    charts.build_scatter_chart(df, x, y, color_col),
                    use_container_width=True,
                )
            elif chart_type == "Histogram" and numeric:
                col = st.selectbox("Column", numeric, key="hist_col")
                st.plotly_chart(charts.build_histogram(df, col), use_container_width=True)
            elif chart_type == "Pie" and categorical:
                col = st.selectbox("Column", categorical, key="pie_col")
                st.plotly_chart(charts.build_pie_chart(df, col), use_container_width=True)
            else:
                st.info("Not enough suitable columns for this chart type.")
        else:
            st.info("Charts are available for CSV and Excel files with tabular data.")

    with tab3:
        st.caption("Ask questions about your uploaded file.")
        if "chat_history" not in st.session_state:
            st.session_state.chat_history = []

        for msg in st.session_state.chat_history:
            chat_message(msg["role"], msg["content"])

        question = st.chat_input("Ask about your file...")
        if question:
            st.session_state.chat_history.append({"role": "user", "content": question})
            answer = ai_engine.chat_with_file(question, cu["preview"], cu["filename"])
            st.session_state.chat_history.append({"role": "bot", "content": answer})
            st.rerun()

    if st.button("← Back to Upload"):
        st.session_state.page = "Upload"
        st.rerun()


def render_reports():
    """Reports listing page."""
    page_header("Reports", "Your saved AI analysis reports")

    reports = db.get_user_reports(st.session_state.user["id"])
    if not reports:
        st.info("No reports yet. Generate one from the AI Analysis page.")
    else:
        for r in reports:
            with st.expander(f"📄 {r['title']} — {r['created_at'][:10]}"):
                st.markdown(r["summary"][:2000])
                if Path(r["file_path"]).exists():
                    with open(r["file_path"], "r", encoding="utf-8") as f:
                        st.download_button(
                            "Download Report",
                            f.read(),
                            file_name=Path(r["file_path"]).name,
                            key=f"dl_{r['id']}",
                        )


def render_profile():
    """User profile page."""
    user = st.session_state.user
    db_user = db.get_user_by_id(user["id"])
    page_header("Profile", "Manage your account information")

    with st.form("profile_form"):
        full_name = st.text_input("Full Name", value=db_user.get("full_name", ""))
        email = st.text_input("Email", value=db_user["email"])
        username = st.text_input("Username", value=db_user["username"], disabled=True)
        st.caption(f"Member since {db_user['created_at'][:10]}")
        if st.form_submit_button("Save Changes", use_container_width=True):
            ok = db.update_user_profile(user["id"], full_name, email)
            if ok:
                st.session_state.user["full_name"] = full_name
                st.session_state.user["email"] = email
                st.success("Profile updated!")
            else:
                st.error("Email already in use.")


def render_settings():
    """App settings page."""
    page_header("Settings", "Customize your experience")

    theme = st.radio(
        "Theme",
        ["light", "dark"],
        index=0 if st.session_state.get("theme", "light") == "light" else 1,
        horizontal=True,
    )

    if theme != st.session_state.get("theme"):
        st.session_state.theme = theme
        db.set_user_theme(st.session_state.user["id"], theme)
        st.rerun()

    st.markdown("---")
    st.subheader("About")
    st.markdown(
        """
        **OmniVerse AI** v1.0  
        Upload and analyze CSV, Excel, PDF, and image files with AI-powered insights.
        """
    )
