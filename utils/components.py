import streamlit as st
from typing import Callable, Any
from datetime import datetime

def card(title: str, content: Callable, key: str = None, expanded: bool = True):
    """Render a collapsible card with consistent styling"""
    with st.expander(title, expanded=expanded):
        content()

def auto_save_container(save_callback: Callable, interval_seconds: int = 30):
    """Container that auto-saves content periodically"""
    if 'last_save_time' not in st.session_state:
        st.session_state.last_save_time = None

    current_time = datetime.now()
    if (st.session_state.last_save_time is None or 
        (current_time - st.session_state.last_save_time).seconds >= interval_seconds):
        save_callback()
        st.session_state.last_save_time = current_time

def loading_spinner(func: Callable) -> Callable:
    """Decorator to show loading spinner during long operations"""
    def wrapper(*args, **kwargs):
        with st.spinner('Processing...'):
            result = func(*args, **kwargs)
        return result
    return wrapper

def confirm_dialog(message: str, on_confirm: Callable, on_cancel: Callable = None):
    """Show a confirmation dialog"""
    if st.button("Confirm"):
        on_confirm()
    if st.button("Cancel"):
        if on_cancel:
            on_cancel()

def delete_confirmation(key: str):
    """Create a delete confirmation dialog"""
    confirm_col, cancel_col = st.columns([1, 1])
    with confirm_col:
        confirm = st.button("✔️ Confirm", key=f"confirm_{key}")
    with cancel_col:
        cancel = st.button("❌ Cancel", key=f"cancel_{key}")
    return confirm, cancel

def unsaved_changes_warning():
    """Show warning when there are unsaved changes"""
    if st.session_state.get('unsaved_changes', False):
        st.warning("You have unsaved changes. Please save your work before leaving this page.")

def profile_completion_status(client):
    """Show profile completion status"""
    sections = {
        'Basic Info': bool(client.get('personal_info')),
        'Assets': bool(client.get('assets')),
        'Income': bool(client.get('income')),
        'Expenses': bool(client.get('expenses')),
        'Projections': bool(client.get('projections'))
    }
    
    completion = sum(sections.values()) / len(sections)
    
    st.sidebar.progress(completion)
    st.sidebar.caption(f"Profile Completion: {int(completion * 100)}%")
    
    with st.sidebar.expander("Details"):
        for section, completed in sections.items():
            st.write(f"{'✅' if completed else '❌'} {section}")

def error_boundary(func):
    """Decorator to catch and display errors"""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            if st.button("Reset Page"):
                st.rerun()
    return wrapper
  