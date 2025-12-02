#!/usr/bin/env python3
"""
Script to extract entities from Home Assistant configuration files
This script parses YAML configuration files to find defined entities.
"""

import yaml
import os
import glob
from datetime import datetime

def load_yaml_file(file_path):
    """Load and parse a YAML file"""
    try:
        with open(file_path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def extract_entities_from_yaml(data, file_path):
    """Extract entity information from YAML data"""
    entities = []
    
    if not data:
        return entities
    
    # Handle different types of YAML structures
    if isinstance(data, dict):
        for key, value in data.items():
            if key in ['input_boolean', 'input_button', 'counter', 'group', 'automation', 'script']:
                if isinstance(value, dict):
                    for entity_id, config in value.items():
                        entities.append({
                            'entity_id': f"{key}.{entity_id}",
                            'type': key,
                            'config': config,
                            'file': file_path
                        })
    
    return entities

def scan_config_directory(config_dir):
    """Scan configuration directory for YAML files"""
    entities = []
    
    # Look for YAML files
    yaml_files = glob.glob(os.path.join(config_dir, "*.yaml"))
    yaml_files.extend(glob.glob(os.path.join(config_dir, "*.yml")))
    
    # Look for YAML files in subdirectories
    for subdir in ['automations', 'scripts', 'packages']:
        subdir_path = os.path.join(config_dir, subdir)
        if os.path.exists(subdir_path):
            yaml_files.extend(glob.glob(os.path.join(subdir_path, "*.yaml")))
            yaml_files.extend(glob.glob(os.path.join(subdir_path, "*.yml")))
    
    print(f"Found {len(yaml_files)} YAML files to scan")
    
    for yaml_file in yaml_files:
        print(f"Scanning: {os.path.basename(yaml_file)}")
        data = load_yaml_file(yaml_file)
        if data:
            file_entities = extract_entities_from_yaml(data, yaml_file)
            entities.extend(file_entities)
    
    return entities

def print_entities_summary(entities):
    """Print a summary of found entities"""
    if not entities:
        print("No entities found in configuration files")
        return
    
    print(f"\n{'='*80}")
    print(f"ENTITIES FOUND IN CONFIGURATION FILES")
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Total Entities: {len(entities)}")
    print(f"{'='*80}")
    
    # Group by type
    by_type = {}
    for entity in entities:
        entity_type = entity['type']
        if entity_type not in by_type:
            by_type[entity_type] = []
        by_type[entity_type].append(entity)
    
    print(f"\nEntities by Type:")
    print(f"{'-'*50}")
    
    for entity_type in sorted(by_type.keys()):
        count = len(by_type[entity_type])
        print(f"{entity_type:20} : {count:3d} entities")
    
    print(f"\n{'='*80}")

def print_detailed_entities(entities, limit=50):
    """Print detailed information about entities"""
    if not entities:
        return
    
    print(f"\nDETAILED ENTITY LIST (showing first {limit}):")
    print(f"{'='*80}")
    
    # Sort by entity_id
    entities.sort(key=lambda x: x['entity_id'])
    
    for i, entity in enumerate(entities[:limit]):
        entity_id = entity['entity_id']
        entity_type = entity['type']
        file_name = os.path.basename(entity['file'])
        
        # Get friendly name if available
        friendly_name = "N/A"
        if 'config' in entity and isinstance(entity['config'], dict):
            friendly_name = entity['config'].get('name', 'N/A')
        
        print(f"{entity_id:40} | {entity_type:15} | {friendly_name:30} | {file_name}")
    
    if len(entities) > limit:
        print(f"... and {len(entities) - limit} more entities")

def main():
    """Main function"""
    print("Home Assistant Configuration Entity Extractor")
    print("=" * 50)
    
    config_dir = "/opt/homeassistant"
    
    if not os.path.exists(config_dir):
        print(f"Configuration directory not found: {config_dir}")
        return
    
    print(f"Scanning configuration directory: {config_dir}")
    
    # Scan for entities
    entities = scan_config_directory(config_dir)
    
    # Print results
    print_entities_summary(entities)
    print_detailed_entities(entities)
    
    print(f"\nScript completed successfully!")

if __name__ == "__main__":
    main()
