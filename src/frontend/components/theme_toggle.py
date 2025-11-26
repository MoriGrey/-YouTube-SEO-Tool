"""
Theme Toggle Component
Provides dark/light theme switching functionality.
"""

import streamlit as st


def render_theme_toggle():
    """Render theme toggle button in sidebar."""
    # Initialize theme in session state
    if "theme" not in st.session_state:
        st.session_state.theme = "dark"
    
    # Theme toggle button
    current_theme = st.session_state.theme
    new_theme = "light" if current_theme == "dark" else "dark"
    icon = "☀️" if current_theme == "dark" else "🌙"
    label = f"{icon} Switch to {new_theme.title()} Theme"
    
    if st.button(label, key="theme_toggle"):
        st.session_state.theme = new_theme
        # Update HTML attribute
        st.markdown(
            f'<script>document.documentElement.setAttribute("data-theme", "{new_theme}");</script>',
            unsafe_allow_html=True
        )
        st.rerun()

