"""
Loading States Component
Provides loading indicators and overlays.
"""

import streamlit as st
import time


def show_loading(message="Loading...", key=None):
    """
    Show loading overlay.
    
    Args:
        message: Loading message to display
        key: Optional unique key for the loading state
    """
    loading_key = key or f"loading_{int(time.time())}"
    
    # Store loading state
    if "loading_states" not in st.session_state:
        st.session_state.loading_states = {}
    
    st.session_state.loading_states[loading_key] = {
        "message": message,
        "active": True
    }
    
    # Render loading overlay
    loading_html = f"""
    <div class="loading-overlay" id="loading-overlay-{loading_key}">
        <div class="loading-content">
            <div class="loading-spinner" style="margin: 0 auto 1rem;"></div>
            <p style="color: var(--text-primary); margin: 0;">{message}</p>
        </div>
    </div>
    <script>
        // Show loading overlay
        document.getElementById('loading-overlay-{loading_key}').style.display = 'flex';
    </script>
    """
    
    st.markdown(loading_html, unsafe_allow_html=True)


def hide_loading(key=None):
    """
    Hide loading overlay.
    
    Args:
        key: Optional unique key for the loading state
    """
    if "loading_states" not in st.session_state:
        return
    
    if key:
        if key in st.session_state.loading_states:
            st.session_state.loading_states[key]["active"] = False
    else:
        # Hide all loading states
        for k in st.session_state.loading_states:
            st.session_state.loading_states[k]["active"] = False


def loading_spinner(message="Loading..."):
    """
    Render inline loading spinner.
    
    Args:
        message: Optional message to display next to spinner
    """
    spinner_html = f"""
    <div style="display: flex; align-items: center; gap: 0.5rem;">
        <div class="loading-spinner"></div>
        <span>{message}</span>
    </div>
    """
    st.markdown(spinner_html, unsafe_allow_html=True)

