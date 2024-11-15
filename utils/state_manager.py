import streamlit as st
from typing import Any, Optional
from datetime import datetime

class StateManager:
    @staticmethod
    def init_session_state():
        """Initialize all session state variables"""
        if 'client_manager' not in st.session_state:
            from utils.client_manager import ClientManager
            st.session_state.client_manager = ClientManager()
        
        defaults = {
            'selected_client': None,
            'current_client_data': {},
            'last_save_time': None,
            'unsaved_changes': False,
            'active_tab': 0,
            'show_save_indicator': False,
            'calculation_in_progress': False,
            'error_message': None,
            'success_message': None,
            'calculation_settings': {},
            'report_templates': [],
            'custom_categories': {},
            'analysis_results': {}
        }
        
        for key, default_value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value

    @staticmethod
    def set_state(key: str, value: Any):
        """Set a session state value and mark changes as unsaved"""
        st.session_state[key] = value
        if key != 'unsaved_changes':
            st.session_state.unsaved_changes = True

    @staticmethod
    def get_state(key: str, default: Any = None) -> Any:
        """Get a session state value"""
        return st.session_state.get(key, default)

    @staticmethod
    def mark_saved():
        """Mark current state as saved"""
        st.session_state.unsaved_changes = False
        st.session_state.last_save_time = datetime.now()
        st.session_state.show_save_indicator = True

    @staticmethod
    def show_message(message: str, type: str = "info"):
        """Show a message to the user"""
        if type == "error":
            st.error(message)
        elif type == "success":
            st.success(message)
        else:
            st.info(message)

    @staticmethod
    def auto_save(client, client_manager):
        """Auto-save client data periodically"""
        if st.session_state.get('unsaved_changes', False):
            current_time = datetime.now()
            last_save = st.session_state.get('last_save_time')
            
            if not last_save or (current_time - last_save).seconds >= 30:
                with st.spinner("Auto-saving..."):
                    client_manager.save_client(client)
                    st.session_state.last_save_time = current_time
                    st.session_state.unsaved_changes = False 