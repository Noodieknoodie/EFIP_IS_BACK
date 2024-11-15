import streamlit as st
from datetime import datetime
from utils.age_calculator import calculate_age
from utils.validators import validate_name, validate_date

def render_client_information(client, client_manager):
    st.header("Client Information")
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_primary_client(client, client_manager)
    
    with col2:
        render_spouse_information(client, client_manager)

def render_primary_client(client, client_manager):
    st.subheader("Client Information")
    with st.form("client_info_form"):
        client_info = client.get('personal_info', {})
        
        first_name = st.text_input("First Name", value=client_info.get('client_first_name', ''))
        last_name = st.text_input("Last Name", value=client_info.get('client_last_name', ''))
        
        # Validate names
        valid_first_name, first_name_msg = validate_name(first_name)
        valid_last_name, last_name_msg = validate_name(last_name)
        
        if not valid_first_name:
            st.error(first_name_msg)
        if not valid_last_name:
            st.error(last_name_msg)
        
        dob = st.date_input("Date of Birth", 
            value=datetime.strptime(client_info.get('client_dob', '1960-01-01'), '%Y-%m-%d'))
        
        is_retired = st.checkbox("Already Retired?", value=client_info.get('is_retired', False))
        retirement_age = None
        if not is_retired:
            retirement_age = st.number_input("Retirement Age", 
                value=client_info.get('retirement_age', 65),
                min_value=0, max_value=100)
        
        current_age = calculate_age(dob.strftime('%Y-%m-%d'))
        st.info(f"Current Age: {current_age}")
        
        if st.form_submit_button("Update Client Information"):
            updated_info = {
                'client_first_name': first_name,
                'client_last_name': last_name,
                'client_dob': dob.strftime('%Y-%m-%d'),
                'is_retired': is_retired,
                'retirement_age': retirement_age if not is_retired else None
            }
            client['personal_info'].update(updated_info)
            client_manager.save_client(client)
            st.success("Client information updated!")

def render_spouse_information(client, client_manager):
    st.subheader("Spouse Information")
    with st.form("spouse_info_form"):
        client_info = client.get('personal_info', {})
        
        spouse_first_name = st.text_input(
            "First Name", 
            value=client_info.get('spouse_first_name', ''),
            key="spouse_first_name"
        )
        spouse_last_name = st.text_input(
            "Last Name", 
            value=client_info.get('spouse_last_name', ''),
            key="spouse_last_name"
        )
        spouse_dob = st.date_input(
            "Date of Birth", 
            value=datetime.strptime(client_info.get('spouse_dob', '1960-01-01'), '%Y-%m-%d'),
            key="spouse_dob"
        )
        
        spouse_is_retired = st.checkbox(
            "Already Retired?", 
            value=client_info.get('spouse_is_retired', False),
            key="spouse_is_retired"
        )
        
        spouse_retirement_age = None
        if not spouse_is_retired:
            spouse_retirement_age = st.number_input(
                "Retirement Age", 
                value=client_info.get('spouse_retirement_age', 65),
                min_value=0,
                max_value=100,
                key="spouse_retirement_age"
            )
        
        spouse_current_age = calculate_age(spouse_dob.strftime('%Y-%m-%d'))
        st.info(f"Current Age: {spouse_current_age}")
        
        if st.form_submit_button("Update Spouse Information"):
            updated_info = {
                'spouse_first_name': spouse_first_name,
                'spouse_last_name': spouse_last_name,
                'spouse_dob': spouse_dob.strftime('%Y-%m-%d'),
                'spouse_is_retired': spouse_is_retired,
                'spouse_retirement_age': spouse_retirement_age if not spouse_is_retired else None
            }
            client['personal_info'].update(updated_info)
            client_manager.save_client(client)
            st.success("Spouse information updated!")