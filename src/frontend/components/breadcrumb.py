"""
Breadcrumb Navigation Component
Provides navigation breadcrumbs for better UX.
"""

import streamlit as st


def render_breadcrumb(items):
    """
    Render breadcrumb navigation.
    
    Args:
        items: List of tuples (label, page_id) or list of strings
               If tuple, first element is label, second is page identifier
               If string, just the label
    """
    if not items:
        return
    
    breadcrumb_html = '<div class="nav-breadcrumb">'
    
    for i, item in enumerate(items):
        if isinstance(item, tuple):
            label, page_id = item
            # For now, just render as text (can be enhanced with links later)
            breadcrumb_html += f'<span>{label}</span>'
        else:
            breadcrumb_html += f'<span>{item}</span>'
        
        if i < len(items) - 1:
            breadcrumb_html += '<span class="nav-breadcrumb-separator"> / </span>'
    
    breadcrumb_html += '</div>'
    
    st.markdown(breadcrumb_html, unsafe_allow_html=True)

