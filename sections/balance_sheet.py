import streamlit as st
import pandas as pd

def render_balance_sheet(client, client_manager):
    st.header("Balance Sheet")
    
    col1, col2 = st.columns(2)
    
    with col1:
        render_assets_summary(client)
    
    with col2:
        render_liabilities_summary(client)
    
    st.divider()
    render_net_worth_analysis(client)

def render_assets_summary(client):
    st.subheader("Assets")
    
    assets_data = []
    total_assets = 0
    
    if 'assets' in client:
        for category, assets in client['assets'].items():
            category_total = sum(float(asset.get('value', 0)) for asset in assets)
            total_assets += category_total
            assets_data.append({
                'Category': category.replace('_', ' ').title(),
                'Value': f"${category_total:,.2f}"
            })
    
    if assets_data:
        df = pd.DataFrame(assets_data)
        st.dataframe(df, hide_index=True)
    
    st.metric("Total Assets", f"${total_assets:,.2f}")

def render_liabilities_summary(client):
    st.subheader("Liabilities")
    
    # Placeholder for liabilities - to be implemented
    st.info("Liabilities section coming soon...")

def render_net_worth_analysis(client):
    st.subheader("Net Worth Analysis")
    
    total_assets = 0
    if 'assets' in client:
        for category in client['assets'].values():
            for asset in category:
                total_assets += float(asset.get('value', 0))
    
    # Placeholder for liabilities calculation
    total_liabilities = 0
    
    net_worth = total_assets - total_liabilities
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Assets", f"${total_assets:,.2f}")
    col2.metric("Total Liabilities", f"${total_liabilities:,.2f}")
    col3.metric("Net Worth", f"${net_worth:,.2f}") 