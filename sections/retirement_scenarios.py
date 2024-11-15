import streamlit as st
import plotly.graph_objects as go
from typing import Dict

def calculate_max_spending(scenario: Dict) -> float:
    """Binary search to find maximum sustainable spending that results in $0 at final age"""
    min_spend = 0
    max_spend = scenario['starting_balance']
    tolerance = 100
    
    while (max_spend - min_spend) > tolerance:
        current_spend = (max_spend + min_spend) / 2
        final_balance = project_scenario(scenario, current_spend)['final_balance']
        
        if final_balance > 0:
            min_spend = current_spend
        else:
            max_spend = current_spend
            
    return min_spend

def project_scenario(scenario: Dict, retirement_spending: float) -> Dict:
    """Project retirement scenario year by year"""
    years = list(range(scenario['current_age'], scenario['final_age'] + 1))
    balances = [scenario['starting_balance']]
    
    for year in range(len(years) - 1):
        current_balance = balances[-1]
        balance_after_growth = current_balance * (1 + scenario['growth_rate'] / 100)
        
        if year < scenario['retirement_age'] - scenario['current_age']:
            balance_after_cash_flow = balance_after_growth + scenario['annual_contribution']
        else:
            inflation_adjusted_spending = retirement_spending * (1 + scenario['inflation_rate'] / 100) ** year
            balance_after_cash_flow = balance_after_growth - inflation_adjusted_spending
            
        balances.append(balance_after_cash_flow)
    
    return {
        'years': years,
        'balances': balances,
        'final_balance': balances[-1]
    }

def render_retirement_scenarios(client: Dict, client_manager):
    st.title("Retirement Scenario Analysis")
    
    # Initialize state if needed
    if 'retirement_scenarios' not in st.session_state:
        st.session_state.retirement_scenarios = {
            'mode': 'traditional',
            'field_states': {},  # Initialize empty field states
            'scenarios': {
                'conservative': {
                    'name': 'Conservative',
                    'color': '#FF6B6B',
                    'current_age': client.get('personal_info', {}).get('age', 40),
                    'final_age': 95,
                    'retirement_age': 65,
                    'annual_contribution': 0,
                    'growth_rate': 6.0,
                    'inflation_rate': 3.0,
                    'retirement_spending': 50000,
                    'starting_balance': client.get('assets', {}).get('retirement_accounts', 0)
                },
                'moderate': {
                    'name': 'Moderate',
                    'color': '#4DABF7',
                    'current_age': client.get('personal_info', {}).get('age', 40),
                    'final_age': 95,
                    'retirement_age': 65,
                    'annual_contribution': 0,
                    'growth_rate': 7.0,
                    'inflation_rate': 3.0,
                    'retirement_spending': 50000,
                    'starting_balance': client.get('assets', {}).get('retirement_accounts', 0)
                },
                'aggressive': {
                    'name': 'Aggressive',
                    'color': '#51CF66',
                    'current_age': client.get('personal_info', {}).get('age', 40),
                    'final_age': 95,
                    'retirement_age': 65,
                    'annual_contribution': 0,
                    'growth_rate': 8.0,
                    'inflation_rate': 3.0,
                    'retirement_spending': 50000,
                    'starting_balance': client.get('assets', {}).get('retirement_accounts', 0)
                }
            }
        }
    elif 'field_states' not in st.session_state.retirement_scenarios:
        st.session_state.retirement_scenarios['field_states'] = {}
    
    mode = st.radio("Analysis Mode", ["Traditional", "Maximum Spending"], horizontal=True)
    
    # Three columns for scenarios
    cols = st.columns(3)
    for idx, (scenario_key, scenario) in enumerate(st.session_state.retirement_scenarios['scenarios'].items()):
        with cols[idx]:
            st.markdown(f"### {scenario['name']}")
            
            # Growth rate (always independent)
            st.write("Growth Rate (%)")
            scenario['growth_rate'] = st.number_input(
                "Growth Rate",
                value=float(scenario['growth_rate']),
                min_value=0.0,
                max_value=15.0,
                step=0.1,
                key=f"{scenario_key}_growth",
                label_visibility="collapsed"
            )
            
            # All other inputs (with linking)
            fields = ['current_age', 'final_age', 'retirement_age', 'annual_contribution', 
                     'inflation_rate', 'retirement_spending']
            
            for field in fields:
                if field == 'retirement_spending' and mode == 'maximum_spending':
                    continue
                
                # Initialize field state if needed
                field_key = f"{scenario_key}_{field}_linked"
                if field_key not in st.session_state.retirement_scenarios['field_states']:
                    st.session_state.retirement_scenarios['field_states'][field_key] = True
                
                # Create a row for the field label and link toggle
                label_col, toggle_col = st.columns([5, 1])
                with label_col:
                    st.write(field.replace('_', ' ').title())
                with toggle_col:
                    # Use session state to track link state
                    is_linked = st.session_state.retirement_scenarios['field_states'][field_key]
                    
                    # Update link state and icon based on checkbox
                    new_state = st.checkbox(
                        "🔗" if is_linked else "🔓",
                        value=is_linked,
                        key=f"link_{scenario_key}_{field}",
                        help="Link/unlink this value across scenarios"
                    )
                    
                    # If state changed, update it and sync values if needed
                    if new_state != is_linked:
                        st.session_state.retirement_scenarios['field_states'][field_key] = new_state
                        if new_state:  # If newly linked, sync values
                            value = scenario[field]
                            for other_key, other_scenario in st.session_state.retirement_scenarios['scenarios'].items():
                                if other_key != scenario_key:
                                    other_scenario[field] = value
                
                # Input field
                value = st.number_input(
                    field,
                    value=scenario[field],
                    key=f"input_{scenario_key}_{field}",
                    label_visibility="collapsed"
                )
                
                # Update current scenario
                scenario[field] = value
                
                # Update other scenarios if linked
                if st.session_state.retirement_scenarios['field_states'][field_key]:
                    for other_key, other_scenario in st.session_state.retirement_scenarios['scenarios'].items():
                        if other_key != scenario_key:
                            other_key_field = f"{other_key}_{field}_linked"
                            if st.session_state.retirement_scenarios['field_states'].get(other_key_field, True):
                                other_scenario[field] = value

            # Max spending calculation
            if mode == "Maximum Spending":
                if st.button("Calculate Maximum Spending", key=f"calc_{scenario_key}"):
                    max_spend = calculate_max_spending(scenario)
                    scenario['retirement_spending'] = max_spend
                    st.success(f"Maximum sustainable spending: ${max_spend:,.2f}/year")
                    
                    # Update other scenarios if retirement_spending is linked
                    for other_key, other_scenario in st.session_state.retirement_scenarios['scenarios'].items():
                        if other_key != scenario_key and 'retirement_spending' not in st.session_state.retirement_scenarios['field_states'][f"{other_key}_retirement_spending_linked"]:
                            other_scenario['retirement_spending'] = max_spend

    # Display projection chart
    st.markdown("### Projection Results")
    fig = go.Figure()
    
    for scenario_key, scenario in st.session_state.retirement_scenarios['scenarios'].items():
        projection = project_scenario(scenario, scenario['retirement_spending'])
        
        fig.add_trace(go.Scatter(
            x=projection['years'],
            y=projection['balances'],
            name=f"{scenario['name']} ({scenario['growth_rate']}%)",
            line=dict(color=scenario['color']),
            hovertemplate="Age: %{x}<br>Balance: $%{y:,.0f}"
        ))
    
    fig.add_vline(
        x=scenario['retirement_age'],
        line_dash="dash",
        line_color="red",
        annotation_text="Retirement Age"
    )
    
    fig.update_layout(
        height=600,
        xaxis_title="Age",
        yaxis_title="Portfolio Balance ($)",
        yaxis_tickformat="$,.0f",
        hovermode="x unified",
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)