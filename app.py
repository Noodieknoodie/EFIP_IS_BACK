import streamlit as st
from utils.client_manager import ClientManager
from utils.components import delete_confirmation, profile_completion_status
import time
from datetime import datetime
from pathlib import Path
import json

# Change from sections to pages
from sections import (
    client_information,
    assets_liabilities,
    cash_flow,
    balance_sheet,
    projections,
    retirement_scenarios
)

def init_session_state():
    """Initialize session state variables"""
    if 'client_manager' not in st.session_state:
        st.session_state.client_manager = ClientManager()
        
        # Create sample client if no clients exist
        if not list(Path("data/clients").glob("*.json")):
            sample_path = Path("data/sample_client.json")
            if sample_path.exists():
                with open(sample_path, 'r') as f:
                    sample_client = json.load(f)
                st.session_state.client_manager.save_client(sample_client)
    
    if 'selected_client' not in st.session_state:
        st.session_state.selected_client = None
    if 'current_tab' not in st.session_state:
        st.session_state.current_tab = 0
    if 'is_creating_new' not in st.session_state:
        st.session_state.is_creating_new = False
    if 'previous_client_id' not in st.session_state:
        st.session_state.previous_client_id = None

def render_new_client_page():
    """Render the new client creation page"""
    st.title("Create New Client Profile")
    
    # Add a welcome message and instructions
    st.markdown("""
    ### Welcome to Client Profile Creation
    Please fill out the basic information below to create a new client profile.
    You'll be able to add detailed financial information after creating the profile.
    """)
    
    with st.form("new_client_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            client_id = st.text_input(
                "Client ID",
                help="Unique identifier for the client (letters, numbers, hyphens only)"
            )
            first_name = st.text_input("First Name")
            last_name = st.text_input("Last Name")
        
        with col2:
            email = st.text_input("Email")
            phone = st.text_input("Phone")
        
        if st.form_submit_button("Create Client Profile", use_container_width=True):
            if client_id and first_name and last_name:
                with st.spinner("Creating new client profile..."):
                    new_client = {
                        "client_id": client_id,
                        "personal_info": {
                            "client_first_name": first_name,
                            "client_last_name": last_name,
                            "email": email,
                            "phone": phone,
                            "created_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                    }
                    st.session_state.client_manager.save_client(new_client)
                    st.session_state.selected_client = new_client
                    st.session_state.is_creating_new = False
                    st.success("Client profile created successfully!")
                    time.sleep(1)
                    st.rerun()
            else:
                st.error("Client ID, First Name, and Last Name are required!")

def render_client_workspace():
    """Render the main client workspace with navigation"""
    client = st.session_state.selected_client
    client_manager = st.session_state.client_manager
    
    # Show client name and last modified date in header
    client_name = f"{client['personal_info'].get('client_first_name', '')} {client['personal_info'].get('client_last_name', '')}"
    last_modified = datetime.fromtimestamp(Path(f"data/clients/{client['client_id']}.json").stat().st_mtime)
    
    # Main header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title(f"Client: {client_name}")
    with col2:
        st.caption(f"Last Modified: {last_modified.strftime('%Y-%m-%d %H:%M')}")
    
    # Navigation at top
    st.divider()
    nav_col1, nav_col2, nav_col3, nav_col4, nav_col5, nav_col6 = st.columns(6)
    
    pages = {
        nav_col1: ("📋 Client Information", 0),
        nav_col2: ("💰 Assets & Liabilities", 1),
        nav_col3: ("💵 Cash Flow", 2),
        nav_col4: ("📊 Balance Sheet", 3),
        nav_col5: ("📈 Projections", 4),
        nav_col6: ("🎯 Retirement Analysis", 5)
    }
    
    for col, (page_name, page_idx) in pages.items():
        with col:
            if st.button(
                page_name,
                use_container_width=True,
                type="primary" if st.session_state.current_tab == page_idx else "secondary"
            ):
                st.session_state.current_tab = page_idx
                st.rerun()
    
    st.divider()
    
    # Render selected page content
    if st.session_state.current_tab == 0:
        client_information.render_client_information(client, client_manager)
    elif st.session_state.current_tab == 1:
        assets_liabilities.render_assets_liabilities(client, client_manager)
    elif st.session_state.current_tab == 2:
        cash_flow.render_cash_flow(client, client_manager)
    elif st.session_state.current_tab == 3:
        balance_sheet.render_balance_sheet(client, client_manager)
    elif st.session_state.current_tab == 4:
        projections.render_projections(client, client_manager)
    elif st.session_state.current_tab == 5:
        retirement_scenarios.render_retirement_scenarios(client, client_manager)
    
    # Profile completion and quick actions in sidebar
    with st.sidebar:
        st.divider()
        profile_completion_status(client)
        
        st.divider()
        st.subheader("Quick Actions")
        if st.button("📄 Generate Report", key="quick_action_report", use_container_width=True):
            st.info("Report generation coming soon...")
        if st.button("💾 Backup Data", key="quick_action_backup", use_container_width=True):
            with st.spinner("Creating backup..."):
                client_manager.backup_client_data(client['client_id'])
                st.success("Backup created successfully!")

def render_sidebar():
    """Render the client management sidebar"""
    with st.sidebar:
        st.title("Client Management")
        
        # Add a search box for clients
        st.text_input("🔍 Search Clients", key="client_search")
        
        # New Client Button at the top
        if st.button("➕ Create New Client", type="primary", use_container_width=True):
            st.session_state.is_creating_new = True
            st.session_state.selected_client = None
            st.rerun()
        
        st.divider()
        
        # All Clients Section
        st.markdown("### 📋 All Clients")
        clients = st.session_state.client_manager.get_all_clients()
        search_term = st.session_state.get("client_search", "").lower()
        
        # Filter clients based on search
        if search_term:
            clients = [c for c in clients if search_term in c['name'].lower()]
        
        if not clients:
            st.info("No clients found")
        
        for client in clients:
            col1, col2 = st.columns([5, 1])
            with col1:
                if st.button(
                    f"📁 {client['name']}",
                    key=f"client_{client['client_id']}",
                    help=f"Last modified: {client['last_modified']}",
                    use_container_width=True
                ):
                    st.session_state.is_creating_new = False
                    st.session_state.selected_client = st.session_state.client_manager.get_client(client['client_id'])
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"delete_{client['client_id']}"):
                    confirm, cancel = delete_confirmation(f"delete_{client['client_id']}")
                    if confirm:
                        with st.spinner("Deleting client..."):
                            if st.session_state.selected_client and \
                               st.session_state.selected_client['client_id'] == client['client_id']:
                                st.session_state.selected_client = None
                            st.session_state.client_manager.delete_client(client['client_id'])
                            st.success("Client deleted successfully!")
                            time.sleep(1)
                            st.rerun()
        
        # Generate Report Button (only show when client is selected)
        if st.session_state.selected_client and not st.session_state.is_creating_new:
            st.sidebar.divider()
            if st.sidebar.button("📄 Generate Report", 
                               key="sidebar_generate_report", 
                               type="secondary", 
                               use_container_width=True):
                st.sidebar.info("Report generation coming soon...")

def main():
    """Main application entry point"""
    st.set_page_config(
        page_title="Financial Planning Tool",
        page_icon="💰",
        layout="wide"
    )
    
    init_session_state()
    render_sidebar()
    
    # Main content area
    if st.session_state.is_creating_new:
        render_new_client_page()
    elif st.session_state.selected_client:
        render_client_workspace()
    else:
        # Welcome screen
        st.title("Welcome to Financial Planning Tool")
        st.markdown("""
        ### Getting Started
        1. Create a new client profile using the "Create New Client" button in the sidebar
        2. Or select an existing client from the sidebar to view/edit their information
        
        ### Features
        - Comprehensive client information management
        - Asset and liability tracking
        - Cash flow analysis
        - Balance sheet generation
        - Retirement projections
        """)

if __name__ == "__main__":
    main()
