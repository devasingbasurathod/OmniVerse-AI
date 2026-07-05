"""Reusable UI components."""

import streamlit as st


def page_header(title, subtitle=""):
    """Render a styled page header."""
    sub = f"<p>{subtitle}</p>" if subtitle else ""
    st.markdown(
        f'<div class="main-header"><h1>{title}</h1>{sub}</div>',
        unsafe_allow_html=True,
    )


def stat_card(label, value):
    """Render a dashboard stat card."""
    st.markdown(
        f"""
        <div class="stat-card">
            <h3>{label}</h3>
            <p class="value">{value}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def feature_card(title, description):
    """Render a feature highlight card."""
    st.markdown(
        f"""
        <div class="feature-card">
            <h4>{title}</h4>
            <p>{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def chat_message(role, content):
    """Render a chat bubble."""
    css_class = "chat-user" if role == "user" else "chat-bot"
    st.markdown(
        f'<div class="{css_class}">{content}</div>',
        unsafe_allow_html=True,
    )
