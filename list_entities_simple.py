#!/usr/bin/env python3
"""
Simple script to list Home Assistant entities
Tries multiple methods to access entity information
"""

import requests
import json
import sys
import subprocess
import os
from datetime import datetime

def try_api_without_auth():
    """Try to access Home Assistant API without authentication"""
    try:
        response = requests.get("http://localhost:8123/api/", timeout=5)
        if response.status_code == 200:
            print("✓ Home Assistant API is accessible")
            return True
    except:
        pass
    
    try:
        response = requests.get("http://localhost:8123/api/states", timeout=5)
        if response.status_code == 200:
            print("✓ Entity API accessible without authentication")
            return response.json()
    except:
        pass
    
    return False

def try_docker_exec():
    """Try to execute commands inside the Home Assistant container"""
    try:
        # Try to get entities using ha CLI inside the container
        result = subprocess.run([
            "docker", "exec", "homeassistant", 
            "ha", "core", "info"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print("✓ Home Assistant CLI accessible via Docker")
            return True
    except:
        pass
    
    return False

def try_database_direct():
    """Try to read entities directly from the database"""
    db_path = "/opt/homeassistant/home-assistant_v2.db"
    if os.path.exists(db_path):
        print(f"✓ Database found at {db_path}")
        try:
            import sqlite3
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # Get current states only (not historical data)
            cursor.execute("""
                SELECT DISTINCT entity_id, state, attributes 
                FROM states 
                WHERE entity_id IS NOT NULL 
                ORDER BY entity_id
            """)
            entities = cursor.fetchall()
            
            # If that returns too many, try a different approach
            if len(entities) > 10000:
                print(f"Found {len(entities)} total states, trying to get unique current entities...")
                cursor.execute("""
                    SELECT entity_id, state, attributes 
                    FROM states 
                    WHERE entity_id IS NOT NULL 
                    GROUP BY entity_id 
                    ORDER BY entity_id
                """)
                entities = cursor.fetchall()
            
            conn.close()
            
            if entities:
                print(f"✓ Found {len(entities)} unique entities in database")
                return entities
        except Exception as e:
            print(f"✗ Error reading database: {e}")
    
    return False

def try_config_files():
    """Try to find entities from configuration files"""
    config_dir = "/opt/homeassistant"
    entities = []
    
    # Check various config files for entity definitions
    config_files = [
        "configuration.yaml",
        "groups.yaml",
        "automations/",
        "scripts/",
        "packages/"
    ]
    
    for file_path in config_files:
        full_path = os.path.join(config_dir, file_path)
        if os.path.exists(full_path):
            print(f"✓ Found config: {file_path}")
    
    return entities

def try_curl_api():
    """Try using curl to access the API"""
    try:
        result = subprocess.run([
            "curl", "-s", "http://localhost:8123/api/states"
        ], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and result.stdout:
            try:
                entities = json.loads(result.stdout)
                print(f"✓ Retrieved {len(entities)} entities via curl")
                return entities
            except:
                pass
    except:
        pass
    
    return False

def print_entities_summary(entities):
    """Print a summary of entities"""
    if not entities:
        return
    
    print(f"\n{'='*80}")
    print(f"HOME ASSISTANT ENTITIES SUMMARY")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Entities: {len(entities)}")
    print(f"{'='*80}")
    
    # Categorize entities
    categories = {}
    for entity in entities:
        if isinstance(entity, dict):
            entity_id = entity.get('entity_id', 'unknown')
        else:
            # Handle database tuple format (entity_id, state, attributes)
            entity_id = entity[0] if len(entity) > 0 and entity[0] is not None else 'unknown'
        
        if entity_id and entity_id != 'unknown' and '.' in entity_id:
            domain = entity_id.split('.')[0]
            if domain not in categories:
                categories[domain] = 0
            categories[domain] += 1
    
    print(f"\nEntities by Domain:")
    print(f"{'-'*50}")
    
    for domain in sorted(categories.keys()):
        count = categories[domain]
        print(f"{domain:20} : {count:3d} entities")
    
    print(f"\n{'='*80}")

def print_sample_entities(entities, count=20):
    """Print a sample of entities"""
    if not entities:
        return
    
    print(f"\nSAMPLE ENTITIES (showing first {count}):")
    print(f"{'='*80}")
    
    valid_entities = []
    for entity in entities:
        if isinstance(entity, dict):
            entity_id = entity.get('entity_id', 'unknown')
            state = entity.get('state', 'unknown')
            friendly_name = entity.get('attributes', {}).get('friendly_name', 'N/A')
        else:
            # Handle database tuple format
            entity_id = entity[0] if len(entity) > 0 and entity[0] is not None else 'unknown'
            state = entity[1] if len(entity) > 1 and entity[1] is not None else 'unknown'
            friendly_name = 'N/A'
        
        if entity_id and entity_id != 'unknown':
            valid_entities.append((entity_id, state, friendly_name))
    
    for i, (entity_id, state, friendly_name) in enumerate(valid_entities[:count]):
        print(f"{entity_id:40} | {state:15} | {friendly_name}")
    
    if len(valid_entities) > count:
        print(f"... and {len(valid_entities) - count} more entities")

def main():
    """Main function"""
    print("Home Assistant Entity Discovery")
    print("=" * 50)
    
    entities = None
    
    # Try different methods to get entities
    print("\nTrying different methods to access Home Assistant entities...")
    
    # Method 1: Try API without auth
    print("\n1. Trying API without authentication...")
    entities = try_api_without_auth()
    if entities:
        print_entities_summary(entities)
        print_sample_entities(entities)
        return
    
    # Method 2: Try curl
    print("\n2. Trying curl to API...")
    entities = try_curl_api()
    if entities:
        print_entities_summary(entities)
        print_sample_entities(entities)
        return
    
    # Method 3: Try Docker exec
    print("\n3. Trying Docker exec...")
    if try_docker_exec():
        print("Home Assistant CLI is available via Docker")
        print("You can run: docker exec homeassistant ha entity list")
    
    # Method 4: Try direct database access
    print("\n4. Trying direct database access...")
    entities = try_database_direct()
    if entities:
        print_entities_summary(entities)
        print_sample_entities(entities)
        return
    
    # Method 5: Check config files
    print("\n5. Checking configuration files...")
    try_config_files()
    
    print(f"\n{'='*80}")
    print("RECOMMENDATIONS:")
    print("1. Check if Home Assistant is running: docker ps | grep homeassistant")
    print("2. Try accessing the web interface: http://localhost:8123")
    print("3. Create a long-lived access token in Home Assistant")
    print("4. Use the CLI: docker exec homeassistant ha entity list")
    print("5. Check the Developer Tools > States tab in the web interface")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()
