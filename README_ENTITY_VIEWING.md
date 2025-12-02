# Home Assistant Entity Viewing Guide

This guide provides multiple methods to view all entities in your Home Assistant system.

## Quick Start

**The easiest way to view all entities is through the web interface:**

1. Open your web browser and go to: `http://localhost:8123`
2. Log in to your Home Assistant account
3. Go to **Developer Tools** (in the sidebar)
4. Click on the **States** tab
5. You'll see "Current entity states" with all entities listed
6. Use the filter boxes to search for specific entities
7. Clear all filters to see all entities

This is the same interface you were viewing in the image!

## Available Scripts

I've created several scripts to help you view entities:

### 1. `show_all_entities.py` - Comprehensive Guide
```bash
python3 show_all_entities.py
```
This script provides a complete overview of all methods to view entities.

### 2. `get_entities_via_api.py` - API Access
```bash
python3 get_entities_via_api.py
```
This script helps you create a long-lived access token and retrieve entities via the API.

### 3. `extract_entities_from_config.py` - Configuration Files
```bash
python3 extract_entities_from_config.py
```
This script parses configuration files to find defined entities.

### 4. `list_entities_simple.py` - Multiple Methods
```bash
python3 list_entities_simple.py
```
This script tries multiple methods to access entity information.

## Methods to View All Entities

### 1. Web Interface (Recommended)
- **URL**: `http://localhost:8123`
- **Path**: Developer Tools → States
- **Pros**: User-friendly, real-time data, built-in filtering
- **Cons**: Requires web browser access

### 2. API Access
- **Endpoint**: `http://localhost:8123/api/states`
- **Authentication**: Requires long-lived access token
- **Pros**: Programmatic access, can export data
- **Cons**: Requires token setup

**To create a long-lived access token:**
1. Go to your profile in Home Assistant web interface
2. Scroll down to 'Long-Lived Access Tokens'
3. Click 'Create Token' and give it a name
4. Copy the generated token
5. Save it in a file called `token.txt` in this directory

### 3. Database Direct Access
- **Database**: `/opt/homeassistant/home-assistant_v2.db`
- **Query**: `SELECT DISTINCT entity_id FROM states WHERE entity_id IS NOT NULL;`
- **Pros**: Direct access, historical data
- **Cons**: Requires SQLite knowledge

### 4. Entity Registry
- **File**: `/opt/homeassistant/.storage/core.entity_registry`
- **Content**: Entity metadata, device associations, area assignments
- **Pros**: Complete entity information
- **Cons**: Large JSON file

### 5. Configuration Files
- **Files**: Various YAML files in `/opt/homeassistant/`
- **Content**: Defined entities in configuration
- **Pros**: Shows configured entities
- **Cons**: Doesn't show discovered entities

## Command Line Examples

### Check Home Assistant Status
```bash
docker ps | grep homeassistant
```

### View Home Assistant Logs
```bash
docker logs homeassistant --tail 50
```

### Access Home Assistant Shell
```bash
docker exec -it homeassistant /bin/bash
```

### Query Database Directly
```bash
sqlite3 /opt/homeassistant/home-assistant_v2.db
SELECT DISTINCT entity_id FROM states WHERE entity_id IS NOT NULL;
.quit
```

### Use API with curl
```bash
curl -H 'Authorization: Bearer YOUR_TOKEN' \
     http://localhost:8123/api/states
```

## Entity Types

Home Assistant entities are organized by domains:

- **automation** - Automated actions
- **binary_sensor** - On/off sensors
- **climate** - HVAC systems
- **cover** - Blinds, garage doors, etc.
- **device_tracker** - Location tracking
- **fan** - Fans and ventilation
- **group** - Groups of entities
- **input_boolean** - Toggle switches
- **input_button** - Button inputs
- **light** - Lights and bulbs
- **lock** - Door locks
- **media_player** - Audio/video devices
- **person** - People
- **scene** - Scenes
- **script** - Scripts
- **sensor** - Various sensors
- **switch** - Switches and outlets
- **vacuum** - Robot vacuums
- **weather** - Weather information
- **zone** - Geographic zones

## Troubleshooting

### Home Assistant Not Accessible
1. Check if the container is running: `docker ps | grep homeassistant`
2. Check if port 8123 is listening: `ss -tlnp | grep 8123`
3. View logs: `docker logs homeassistant --tail 50`

### API Authentication Issues
1. Make sure you have a valid long-lived access token
2. Check that the token is properly formatted in `token.txt`
3. Verify the token hasn't expired

### Database Access Issues
1. Ensure you have read permissions on the database file
2. Check that the database file exists and isn't corrupted
3. Use the web interface as a fallback

## Summary

You have multiple ways to view all entities in your Home Assistant system:

✅ **Web Interface (Recommended)**: `http://localhost:8123` → Developer Tools → States  
✅ **API Access**: Use the provided scripts with a long-lived token  
✅ **Database**: Direct SQLite access to entity states  
✅ **Configuration**: Parse YAML files for defined entities  
✅ **Entity Registry**: View metadata about all entities  

The web interface method is the same as what you were viewing in the image and provides the most user-friendly experience for viewing all entities in your Home Assistant system.
