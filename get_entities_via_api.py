#!/usr/bin/env python3
"""
Script to get Home Assistant entities via API with authentication
This script helps create a long-lived access token and then uses it to get all entities.
"""

import requests
import json
import sys
import os
from datetime import datetime

def check_home_assistant_running():
    """Check if Home Assistant is running"""
    try:
        response = requests.get("http://localhost:8123/api/", timeout=5)
        if response.status_code in [200, 401]:  # 401 means it's running but needs auth
            print("✓ Home Assistant is running and accessible")
            return True
    except:
        pass
    
    print("✗ Home Assistant is not accessible at http://localhost:8123")
    print("   Make sure Home Assistant is running and accessible")
    return False

def create_long_lived_token():
    """Instructions for creating a long-lived access token"""
    print("\n" + "="*80)
    print("CREATING A LONG-LIVED ACCESS TOKEN")
    print("="*80)
    print("To access the Home Assistant API, you need to create a long-lived access token:")
    print()
    print("1. Open your Home Assistant web interface: http://localhost:8123")
    print("2. Go to your profile (click your username in the sidebar)")
    print("3. Scroll down to 'Long-Lived Access Tokens'")
    print("4. Click 'Create Token'")
    print("5. Give it a name (e.g., 'Entity Lister')")
    print("6. Copy the generated token")
    print("7. Save it in a file called 'token.txt' in this directory")
    print()
    print("Example token.txt content:")
    print("eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...")
    print()
    print("="*80)

def get_token_from_file():
    """Get the access token from token.txt file"""
    token_file = "token.txt"
    if os.path.exists(token_file):
        with open(token_file, 'r') as f:
            token = f.read().strip()
        if token:
            print(f"✓ Found access token in {token_file}")
            return token
    
    print(f"✗ No access token found in {token_file}")
    return None

def get_entities_with_token(token):
    """Get all entities using the access token"""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            "http://localhost:8123/api/states",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            entities = response.json()
            print(f"✓ Successfully retrieved {len(entities)} entities")
            return entities
        else:
            print(f"✗ API request failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Error making API request: {e}")
        return None

def categorize_entities(entities):
    """Categorize entities by domain"""
    categories = {}
    
    for entity in entities:
        domain = entity['entity_id'].split('.')[0]
        if domain not in categories:
            categories[domain] = []
        categories[domain].append(entity)
    
    return categories

def print_entity_summary(entities):
    """Print a summary of all entities"""
    if not entities:
        return
    
    print(f"\n{'='*80}")
    print(f"HOME ASSISTANT ENTITIES SUMMARY")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Entities: {len(entities)}")
    print(f"{'='*80}")
    
    # Categorize entities
    categories = categorize_entities(entities)
    
    print(f"\nEntities by Domain:")
    print(f"{'-'*50}")
    
    for domain in sorted(categories.keys()):
        count = len(categories[domain])
        print(f"{domain:20} : {count:3d} entities")
    
    print(f"\n{'='*80}")

def print_sample_entities(entities, count=30):
    """Print a sample of entities"""
    if not entities:
        return
    
    print(f"\nSAMPLE ENTITIES (showing first {count}):")
    print(f"{'='*80}")
    
    # Sort entities by entity_id
    entities.sort(key=lambda x: x['entity_id'])
    
    for i, entity in enumerate(entities[:count]):
        entity_id = entity['entity_id']
        state = entity['state']
        friendly_name = entity['attributes'].get('friendly_name', 'N/A')
        
        print(f"{entity_id:40} | {state:15} | {friendly_name}")
    
    if len(entities) > count:
        print(f"... and {len(entities) - count} more entities")

def save_entities_to_file(entities, filename="all_entities.json"):
    """Save all entities to a JSON file"""
    if not entities:
        return
    
    try:
        with open(filename, 'w') as f:
            json.dump(entities, f, indent=2)
        print(f"✓ Saved all entities to {filename}")
    except Exception as e:
        print(f"✗ Error saving to file: {e}")

def main():
    """Main function"""
    print("Home Assistant Entity Lister via API")
    print("=" * 50)
    
    # Check if Home Assistant is running
    if not check_home_assistant_running():
        return
    
    # Get access token
    token = get_token_from_file()
    if not token:
        create_long_lived_token()
        return
    
    # Get entities
    print("\nFetching entities from Home Assistant...")
    entities = get_entities_with_token(token)
    
    if not entities:
        print("Failed to retrieve entities. Please check your access token.")
        return
    
    # Print results
    print_entity_summary(entities)
    print_sample_entities(entities)
    
    # Save to file
    save_entities_to_file(entities)
    
    print(f"\nScript completed successfully!")
    print(f"You can now view all entities in the 'all_entities.json' file")

if __name__ == "__main__":
    main()
