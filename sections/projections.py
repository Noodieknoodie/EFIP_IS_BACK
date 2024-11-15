import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date

def render_projections(client, client_manager):
    st.header("Retirement Projections")
    
    if not client.get('personal_info', {}).get('client_dob'):
        st.warning("Please complete client information before viewing projections")
        return
    
    render_projection_inputs(client, client_manager)
    st.divider()
    render_projection_results(client)

def render_projection_inputs(client, client_manager):
    with st.form("projection_settings"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Investment Assumptions")
            inflation_rate = st.slider(
                "Inflation Rate (%)",
                min_value=0.0,
                max_value=10.0,
                value=3.0,
                step=0.1
            )
            investment_return = st.slider(
                "Expected Investment Return (%)",
                min_value=0.0,
                max_value=15.0,
                value=7.0,
                step=0.1
            )
        
        with col2:
            st.subheader("Retirement Assumptions")
            retirement_expenses = st.number_input(
                "Expected Monthly Expenses in Retirement",
                min_value=0.0,
                value=5000.0,
                step=100.0
            )
            life_expectancy = st.slider(
                "Life Expectancy",
                min_value=70,
                max_value=100,
                value=90
            )
        
        if st.form_submit_button("Update Projections"):
            # Save projection settings to client data
            if 'projections' not in client:
                client['projections'] = {}
            
            client['projections'].update({
                'inflation_rate': inflation_rate,
                'investment_return': investment_return,
                'retirement_expenses': retirement_expenses,
                'life_expectancy': life_expectancy
            })
            
            client_manager.save_client(client)
            st.success("Projection settings updated!")

def render_projection_results(client):
    st.subheader("Projection Results")
    
    # Placeholder chart for preview
    years = list(range(2024, 2054))
    conservative = [1000000 * (1.05 ** i) for i in range(len(years))]
    moderate = [1000000 * (1.07 ** i) for i in range(len(years))]
    aggressive = [1000000 * (1.09 ** i) for i in range(len(years))]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=years,
        y=conservative,
        name="Conservative",
        line=dict(color="blue")
    ))
    
    fig.add_trace(go.Scatter(
        x=years,
        y=moderate,
        name="Moderate",
        line=dict(color="green")
    ))
    
    fig.add_trace(go.Scatter(
        x=years,
        y=aggressive,
        name="Aggressive",
        line=dict(color="red")
    ))
    
    fig.update_layout(
        title="Portfolio Value Projection",
        xaxis_title="Year",
        yaxis_title="Portfolio Value ($)",
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    st.info("Detailed Monte Carlo simulations and additional analysis coming soon!") 