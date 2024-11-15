import json
import os
from pathlib import Path
from datetime import datetime
import streamlit as st
from utils.components import loading_spinner

class ClientManager:
    def __init__(self):
        self.clients_dir = Path("data/clients")
        self.clients_dir.mkdir(parents=True, exist_ok=True)

    def get_all_clients(self):
        """Return a list of all clients with their basic info"""
        clients = []
        for file_path in self.clients_dir.glob("*.json"):
            try:
                with open(file_path, 'r') as f:
                    client_data = json.load(f)
                    name = (f"{client_data.get('personal_info', {}).get('client_first_name', '')} "
                           f"{client_data.get('personal_info', {}).get('client_last_name', '')}")
                    clients.append({
                        'client_id': file_path.stem,
                        'name': name.strip() or 'Unknown',
                        'last_modified': datetime.fromtimestamp(file_path.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                    })
            except (json.JSONDecodeError, FileNotFoundError):
                continue
        return sorted(clients, key=lambda x: x['name'].lower())

    def get_client(self, client_id):
        """Load client data from JSON file"""
        file_path = self.clients_dir / f"{client_id}.json"
        if not file_path.exists():
            return None
        with open(file_path, 'r') as f:
            return json.load(f)

    def save_client(self, client_data):
        """Save client data to JSON file"""
        client_id = client_data.get('client_id')
        if not client_id:
            raise ValueError("Client ID is required")
        
        file_path = self.clients_dir / f"{client_id}.json"
        with open(file_path, 'w') as f:
            json.dump(client_data, f, indent=4)

    def delete_client(self, client_id):
        """Delete client JSON file"""
        file_path = self.clients_dir / f"{client_id}.json"
        if file_path.exists():
            file_path.unlink()
            return True
        return False

    def update_client_section(self, client_id, section, data):
        """Update a specific section of client data"""
        client_data = self.get_client(client_id)
        if client_data is None:
            return False
        
        client_data[section] = data
        self.save_client(client_data)
        return True 

    @loading_spinner
    def backup_client_data(self, client_id: str):
        """Create a backup of client data"""
        client_data = self.get_client(client_id)
        if client_data:
            backup_dir = self.clients_dir / "backups" / client_id
            backup_dir.mkdir(parents=True, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = backup_dir / f"backup_{timestamp}.json"
            with open(backup_path, 'w') as f:
                json.dump(client_data, f, indent=4)
            return True
        return False 