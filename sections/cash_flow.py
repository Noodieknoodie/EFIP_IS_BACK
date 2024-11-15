import streamlit as st
from utils.components import card

def render_cash_flow(client, client_manager):
    st.header("Cash Flow Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_income_section(client, client_manager)
    
    with col2:
        render_expenses_section(client, client_manager)

def render_income_section(client, client_manager):
    with card("Monthly Income", lambda: None):
        with st.form("income_form"):
            income_data = client.get('income', {})
            updated_income = {}
            
            st.subheader("Employment Income")
            updated_income['salary'] = st.number_input(
                "Salary/Wages",
                value=float(income_data.get('salary', 0)),
                step=100.0,
                format="%0.2f"
            )
            
            st.subheader("Retirement Income")
            updated_income['pension'] = st.number_input(
                "Pension",
                value=float(income_data.get('pension', 0)),
                step=100.0,
                format="%0.2f"
            )
            updated_income['social_security'] = st.number_input(
                "Social Security",
                value=float(income_data.get('social_security', 0)),
                step=100.0,
                format="%0.2f"
            )
            
            st.subheader("Investment Income")
            updated_income['investment'] = st.number_input(
                "Investment Income",
                value=float(income_data.get('investment', 0)),
                step=100.0,
                format="%0.2f"
            )
            updated_income['rental'] = st.number_input(
                "Rental Income",
                value=float(income_data.get('rental', 0)),
                step=100.0,
                format="%0.2f"
            )
            
            st.subheader("Other Income")
            updated_income['other'] = st.number_input(
                "Other Income",
                value=float(income_data.get('other', 0)),
                step=100.0,
                format="%0.2f"
            )
            
            if st.form_submit_button("Update Income"):
                client['income'] = updated_income
                client_manager.save_client(client)
                st.success("Income updated successfully!")

def render_expenses_section(client, client_manager):
    with card("Monthly Expenses", lambda: None):
        with st.form("expenses_form"):
            expenses_data = client.get('expenses', {})
            updated_expenses = {}
            
            st.subheader("Essential Expenses")
            updated_expenses['housing'] = st.number_input(
                "Housing (Mortgage/Rent)",
                value=float(expenses_data.get('housing', 0)),
                step=100.0,
                format="%0.2f"
            )
            updated_expenses['utilities'] = st.number_input(
                "Utilities",
                value=float(expenses_data.get('utilities', 0)),
                step=50.0,
                format="%0.2f"
            )
            updated_expenses['groceries'] = st.number_input(
                "Groceries",
                value=float(expenses_data.get('groceries', 0)),
                step=50.0,
                format="%0.2f"
            )
            
            st.subheader("Healthcare")
            updated_expenses['healthcare'] = st.number_input(
                "Healthcare",
                value=float(expenses_data.get('healthcare', 0)),
                step=50.0,
                format="%0.2f"
            )
            updated_expenses['insurance'] = st.number_input(
                "Insurance Premiums",
                value=float(expenses_data.get('insurance', 0)),
                step=50.0,
                format="%0.2f"
            )
            
            st.subheader("Discretionary Expenses")
            updated_expenses['entertainment'] = st.number_input(
                "Entertainment",
                value=float(expenses_data.get('entertainment', 0)),
                step=50.0,
                format="%0.2f"
            )
            updated_expenses['travel'] = st.number_input(
                "Travel",
                value=float(expenses_data.get('travel', 0)),
                step=50.0,
                format="%0.2f"
            )
            
            if st.form_submit_button("Update Expenses"):
                client['expenses'] = updated_expenses
                client_manager.save_client(client)
                st.success("Expenses updated successfully!") 