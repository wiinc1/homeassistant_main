#!/usr/bin/env python3
"""
Comprehensive Home Assistant Entity Viewer
This script provides multiple methods to view all entities in Home Assistant.
"""

import subprocess
import os
import sys
from datetime import datetime

def print_header():
    """Print script header"""
    print("="*80)
    print("HOME ASSISTANT ENTITY VIEWER")
    print("="*80)
    print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("This script provides multiple ways to view all entities in your Home Assistant system.")
    print("="*80)

def check_home_assistant_status():
    """Check if Home Assistant is running"""
    print("\n1. CHECKING HOME ASSISTANT STATUS")
    print("-" * 50)
    
    try:
        result = subprocess.run(["docker", "ps", "--filter", "name=homeassistant"], 
                              capture_output=True, text=True, timeout=10)
        
        if "homeassistant" in result.stdout:
            print("✓ Home Assistant container is running")
            
            # Check if port 8123 is listening
            result2 = subprocess.run(["ss", "-tlnp", "|", "grep", "8123"], 
                                   shell=True, capture_output=True, text=True)
            if "8123" in result2.stdout:
                print("✓ Home Assistant web interface is accessible on port 8123")
                print("  Web Interface: http://localhost:8123")
            else:
                print("✗ Home Assistant web interface not accessible on port 8123")
            
            return True
        else:
            print("✗ Home Assistant container is not running")
            return False
            
    except Exception as e:
        print(f"✗ Error checking Home Assistant status: {e}")
        return False

def show_web_interface_method():
    """Show how to view entities via web interface"""
    print("\n2. VIEW ENTITIES VIA WEB INTERFACE")
    print("-" * 50)
    print("The easiest way to view all entities:")
    print()
    print("1. Open your web browser and go to: http://localhost:8123")
    print("2. Log in to your Home Assistant account")
    print("3. Go to Developer Tools (in the sidebar)")
    print("4. Click on the 'States' tab")
    print("5. You'll see 'Current entity states' with all entities listed")
    print("6. Use the filter boxes to search for specific entities")
    print("7. Clear all filters to see all entities")
    print()
    print("This is the same interface you were looking at in the image!")

def show_api_method():
    """Show how to use the API method"""
    print("\n3. VIEW ENTITIES VIA API")
    print("-" * 50)
    print("To access entities programmatically via the API:")
    print()
    print("1. Create a long-lived access token:")
    print("   - Go to your profile in Home Assistant web interface")
    print("   - Scroll down to 'Long-Lived Access Tokens'")
    print("   - Click 'Create Token' and give it a name")
    print("   - Copy the generated token")
    print()
    print("2. Use the provided script:")
    print("   python3 get_entities_via_api.py")
    print()
    print("3. Or use curl directly:")
    print("   curl -H 'Authorization: Bearer YOUR_TOKEN' \\")
    print("        http://localhost:8123/api/states")

def show_cli_method():
    """Show how to use CLI methods"""
    print("\n4. VIEW ENTITIES VIA COMMAND LINE")
    print("-" * 50)
    print("Try these commands to view entities:")
    print()
    
    commands = [
        ("Check if Home Assistant CLI is available:", 
         "docker exec homeassistant ha entity list"),
        ("Check Home Assistant version:", 
         "docker exec homeassistant ha core info"),
        ("View Home Assistant logs:", 
         "docker logs homeassistant --tail 50"),
        ("Access Home Assistant shell:", 
         "docker exec -it homeassistant /bin/bash")
    ]
    
    for desc, cmd in commands:
        print(f"{desc}")
        print(f"  {cmd}")
        print()

def show_database_method():
    """Show how to access the database directly"""
    print("\n5. VIEW ENTITIES VIA DATABASE")
    print("-" * 50)
    print("The database contains all entity states:")
    print()
    print("Database location: /opt/homeassistant/home-assistant_v2.db")
    print()
    print("To query the database directly:")
    print("  sqlite3 /opt/homeassistant/home-assistant_v2.db")
    print("  SELECT DISTINCT entity_id FROM states WHERE entity_id IS NOT NULL;")
    print("  .quit")
    print()
    print("Note: The database contains historical data, so you'll see many entries.")

def show_configuration_method():
    """Show how to view entities from configuration"""
    print("\n6. VIEW ENTITIES FROM CONFIGURATION")
    print("-" * 50)
    print("Configuration files define many entities:")
    print()
    print("Key configuration files:")
    print("  - /opt/homeassistant/configuration.yaml (main config)")
    print("  - /opt/homeassistant/groups.yaml (group entities)")
    print("  - /opt/homeassistant/automations/ (automation entities)")
    print("  - /opt/homeassistant/scripts/ (script entities)")
    print("  - /opt/homeassistant/packages/ (package configurations)")
    print()
    print("To view configuration entities:")
    print("  python3 extract_entities_from_config.py")

def show_entity_registry():
    """Show how to view the entity registry"""
    print("\n7. VIEW ENTITY REGISTRY")
    print("-" * 50)
    print("The entity registry contains metadata about all entities:")
    print()
    print("Registry file: /opt/homeassistant/.storage/core.entity_registry")
    print()
    print("This file contains:")
    print("  - Entity IDs and their configurations")
    print("  - Device associations")
    print("  - Area assignments")
    print("  - Custom names and icons")
    print()
    print("Note: This is a JSON file that can be quite large.")

def show_recommendations():
    """Show recommendations"""
    print("\n8. RECOMMENDATIONS")
    print("-" * 50)
    print("For the best experience viewing all entities:")
    print()
    print("1. PRIMARY METHOD: Use the web interface (Developer Tools > States)")
    print("   - Most user-friendly")
    print("   - Real-time data")
    print("   - Built-in filtering and search")
    print()
    print("2. PROGRAMMATIC ACCESS: Use the API with a long-lived token")
    print("   - Best for automation and scripts")
    print("   - Can export data to files")
    print("   - Integrate with other tools")
    print()
    print("3. TROUBLESHOOTING: Check the database directly")
    print("   - When web interface is not accessible")
    print("   - For debugging entity issues")
    print("   - To understand entity history")

def main():
    """Main function"""
    print_header()
    
    # Check Home Assistant status
    ha_running = check_home_assistant_status()
    
    # Show all methods
    show_web_interface_method()
    show_api_method()
    show_cli_method()
    show_database_method()
    show_configuration_method()
    show_entity_registry()
    show_recommendations()
    
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print("You have multiple ways to view all entities in your Home Assistant system:")
    print()
    print("✓ Web Interface (Recommended): http://localhost:8123 → Developer Tools → States")
    print("✓ API Access: Use the provided scripts with a long-lived token")
    print("✓ Database: Direct SQLite access to entity states")
    print("✓ Configuration: Parse YAML files for defined entities")
    print("✓ Entity Registry: View metadata about all entities")
    print()
    print("The web interface method is the same as what you were viewing in the image!")
    print("="*80)

if __name__ == "__main__":
    main()
