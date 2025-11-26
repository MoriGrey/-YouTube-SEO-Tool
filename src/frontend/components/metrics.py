"""
Metrics Display Component
Enhanced metric cards for dashboard.
"""

import streamlit as st


def render_metric_card(value, label, color="default", icon="", change=None, change_label=""):
    """
    Render an enhanced metric card.
    
    Args:
        value: The metric value to display
        label: Label for the metric
        color: Color theme (default, success, warning, error, info)
        icon: Optional icon emoji or symbol
        change: Optional change value (e.g., +5.2%)
        change_label: Optional label for change
    """
    color_class = f"metric-{color}"
    
    metric_html = f"""
    <div class="metric-card fade-in">
        {f'<div style="font-size: 1.5rem; margin-bottom: 0.5rem;">{icon}</div>' if icon else ''}
        <div class="metric-value {color_class}">{value}</div>
        <div class="metric-label">{label}</div>
        {f'<div style="margin-top: 0.5rem; font-size: 0.875rem; color: var(--text-secondary);">{change} {change_label}</div>' if change else ''}
    </div>
    """
    
    st.markdown(metric_html, unsafe_allow_html=True)

