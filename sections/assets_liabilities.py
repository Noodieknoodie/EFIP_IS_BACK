import streamlit as st
from config.settings import DEFAULT_ASSET_CATEGORIES

def render_assets_liabilities(client, client_manager):
    st.header("Assets")
    
    render_summary_metrics(client)
    st.divider()
    render_asset_categories(client, client_manager)

def render_summary_metrics(client):
    total_assets, total_nest_egg, total_managed, total_unmanaged = calculate_totals(client)
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Assets", f"${total_assets:,.2f}")
        col1a, col1b = st.columns(2)
        col1a.metric("Managed Assets", f"${total_managed:,.2f}")
        col1b.metric("Unmanaged Assets", f"${total_unmanaged:,.2f}")
    
    with col2:
        st.metric("Total Nest Egg", f"${total_nest_egg:,.2f}")
        col2a, col2b = st.columns(2)
        col2a.metric("Managed Nest Egg", f"${total_managed:,.2f}")
        col2b.metric("Unmanaged Nest Egg", f"${total_unmanaged:,.2f}")

def calculate_totals(client):
    total_assets = 0
    total_nest_egg = 0
    total_managed = 0
    total_unmanaged = 0
    
    if 'assets' in client:
        for category in client['assets'].values():
            for asset in category:
                value = float(asset.get('value', 0))
                total_assets += value
                
                if asset.get('include_in_nest_egg', True):
                    total_nest_egg += value
                    
                if asset.get('is_managed', False):
                    total_managed += value
                else:
                    total_unmanaged += value
    
    return total_assets, total_nest_egg, total_managed, total_unmanaged

def render_asset_categories(client, client_manager):
    if 'asset_categories' not in client:
        client['asset_categories'] = list(DEFAULT_ASSET_CATEGORIES.keys())
        client['assets'] = {cat: [] for cat in client['asset_categories']}
        client_manager.save_client(client)

    # Add new category button
    col1, col2 = st.columns([3, 1])
    with col2:
        if st.button("➕ Add New Category"):
            new_category = f"category_{len(client['asset_categories'])}"
            client['asset_categories'].append(new_category)
            client['assets'][new_category] = []
            client_manager.save_client(client)
            st.rerun()

    # Render each category as a card
    for category in client['asset_categories']:
        with st.expander(DEFAULT_ASSET_CATEGORIES.get(category, category.replace('_', ' ').title()), expanded=True):
            render_asset_category(category, client, client_manager)

def render_asset_category(category, client, client_manager):
    assets = client['assets'].get(category, [])
    
    # Category settings
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        new_name = st.text_input(
            "Category Name", 
            value=DEFAULT_ASSET_CATEGORIES.get(category, category),
            key=f"cat_name_{category}"
        )
    
    # Add new asset button
    with col3:
        if st.button("Add Asset", key=f"add_asset_{category}"):
            assets.append({
                "name": "",
                "value": 0.0,
                "is_managed": False,
                "include_in_nest_egg": True
            })
            client['assets'][category] = assets
            client_manager.save_client(client)
            st.rerun()

    # Render each asset in the category
    for idx, asset in enumerate(assets):
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 2, 1, 1, 1])
            
            with col1:
                asset['name'] = st.text_input(
                    "Asset Name",
                    value=asset.get('name', ''),
                    key=f"asset_name_{category}_{idx}"
                )
            
            with col2:
                asset['value'] = st.number_input(
                    "Value",
                    value=float(asset.get('value', 0)),
                    step=1000.0,
                    format="%0.2f",
                    key=f"asset_value_{category}_{idx}"
                )
            
            with col3:
                asset['is_managed'] = st.checkbox(
                    "Managed",
                    value=asset.get('is_managed', False),
                    key=f"asset_managed_{category}_{idx}"
                )
            
            with col4:
                asset['include_in_nest_egg'] = st.checkbox(
                    "In Nest Egg",
                    value=asset.get('include_in_nest_egg', True),
                    key=f"asset_nest_egg_{category}_{idx}"
                )
            
            with col5:
                if st.button("🗑️", key=f"delete_asset_{category}_{idx}"):
                    assets.pop(idx)
                    client['assets'][category] = assets
                    client_manager.save_client(client)
                    st.rerun()

        st.divider()

    # Save changes to category
    if st.button("Save Changes", key=f"save_{category}"):
        client['assets'][category] = assets
        client_manager.save_client(client)
        st.success("Changes saved successfully!")