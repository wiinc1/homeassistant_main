#!/usr/bin/env python3
"""
Script to list all entities in Home Assistant
This script accesses the Home Assistant API to retrieve all entities and their states.
"""

import requests
import json
import sys
from datetime import datetime

# Home Assistant API configuration
HA_URL = "http://localhost:8123"
API_ENDPOINT = f"{HA_URL}/api/states"

def get_all_entities():
    """Fetch all entities from Home Assistant API"""
    try:
        # Make request to Home Assistant API
        response = requests.get(API_ENDPOINT, timeout=10)
        response.raise_for_status()
        
        entities = response.json()
        return entities
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Home Assistant API: {e}")
        print(f"Make sure Home Assistant is running at {HA_URL}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON response: {e}")
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

def print_detailed_entities(entities, domain_filter=None):
    """Print detailed information about entities"""
    if not entities:
        return
    
    print(f"\nDETAILED ENTITY LIST")
    print(f"{'='*80}")
    
    # Filter by domain if specified
    if domain_filter:
        entities = [e for e in entities if e['entity_id'].startswith(f"{domain_filter}.")]
        print(f"Filtered by domain: {domain_filter}")
    
    # Sort entities by entity_id
    entities.sort(key=lambda x: x['entity_id'])
    
    for entity in entities:
        entity_id = entity['entity_id']
        state = entity['state']
        friendly_name = entity['attributes'].get('friendly_name', 'N/A')
        
        print(f"{entity_id:40} | {state:15} | {friendly_name}")
    
    print(f"\nTotal entities shown: {len(entities)}")

def print_entity_details(entities, entity_id=None):
    """Print detailed information about a specific entity or all entities"""
    if not entities:
        return
    
    if entity_id:
        # Find specific entity
        entity = next((e for e in entities if e['entity_id'] == entity_id), None)
        if entity:
            print(f"\nDETAILED INFORMATION FOR: {entity_id}")
            print(f"{'='*80}")
            print(json.dumps(entity, indent=2))
        else:
            print(f"Entity '{entity_id}' not found")
        return
    
    # Print details for all entities
    print(f"\nDETAILED ENTITY INFORMATION")
    print(f"{'='*80}")
    
    for entity in sorted(entities, key=lambda x: x['entity_id']):
        entity_id = entity['entity_id']
        print(f"\n{entity_id}:")
        print(f"  State: {entity['state']}")
        print(f"  Friendly Name: {entity['attributes'].get('friendly_name', 'N/A')}")
        print(f"  Last Updated: {entity['last_updated']}")
        print(f"  Last Changed: {entity['last_changed']}")
        
        # Print some key attributes
        attrs = entity['attributes']
        if attrs:
            print(f"  Key Attributes:")
            for key, value in attrs.items():
                if key not in ['friendly_name']:  # Skip already shown attributes
                    print(f"    {key}: {value}")

def main():
    """Main function"""
    print("Home Assistant Entity Lister")
    print("=" * 50)
    
    # Get command line arguments
    args = sys.argv[1:]
    
    # Parse arguments
    show_summary = True
    show_detailed = False
    show_full_details = False
    domain_filter = None
    specific_entity = None
    
    i = 0
    while i < len(args):
        if args[i] == '--detailed':
            show_detailed = True
        elif args[i] == '--full-details':
            show_full_details = True
        elif args[i] == '--domain' and i + 1 < len(args):
            domain_filter = args[i + 1]
            i += 1
        elif args[i] == '--entity' and i + 1 < len(args):
            specific_entity = args[i + 1]
            i += 1
        elif args[i] == '--no-summary':
            show_summary = False
        i += 1
    
    # Get entities from Home Assistant
    print("Connecting to Home Assistant...")
    entities = get_all_entities()
    
    if not entities:
        sys.exit(1)
    
    # Print results based on arguments
    if show_summary:
        print_entity_summary(entities)
    
    if specific_entity:
        print_entity_details(entities, specific_entity)
    elif show_full_details:
        print_entity_details(entities)
    elif show_detailed:
        print_detailed_entities(entities, domain_filter)
    
    print(f"\nScript completed successfully!")

if __name__ == "__main__":
    main()
