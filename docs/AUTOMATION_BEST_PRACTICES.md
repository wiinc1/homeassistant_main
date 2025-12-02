# Automation Best Practices

This document provides guidelines for creating and maintaining automations in this Home Assistant configuration. It covers the use of helper entities, template sensors, and standardized automation structure.

## Table of Contents

1. [Helper Entities](#helper-entities)
2. [Template Sensors](#template-sensors)
3. [Template Patterns](#template-patterns)
4. [Standard Automation Structure](#standard-automation-structure)
5. [Common Patterns](#common-patterns)
6. [Migration Guide](#migration-guide)

## Helper Entities

Helper entities are `input_boolean` entities that provide manual control and overrides for automation behavior.

### Available Helper Entities

- **`input_boolean.automation_enabled`**: Master toggle to enable/disable all automations
- **`input_boolean.everyone_home_override`**: Manual override for everyone home state
- **`input_boolean.anyone_home_override`**: Manual override for anyone home state
- **`input_boolean.vacation_mode`**: Existing vacation mode toggle (also available as `binary_sensor.vacation_mode_active`)

### Usage

Always check `automation_enabled` at the start of automation conditions:

```yaml
condition:
  - condition: state
      entity_id: input_boolean.automation_enabled
      state: 'on'
  # ... other conditions
```

## Template Sensors

Template sensors provide reusable logic for common conditions, reducing code duplication.

### Available Template Sensors

#### Presence Sensors

- **`binary_sensor.everyone_home`**: `on` when all family members are home
- **`binary_sensor.anyone_home`**: `on` when any family member is home
- **`sensor.family_presence_count`**: Count of family members currently at home (0-4)

#### Status Sensors

- **`binary_sensor.vacation_mode_active`**: `on` when vacation mode is active

### Usage

Instead of checking multiple device trackers:

```yaml
# ❌ DON'T: Repetitive device tracker checks
condition:
  - condition: state
      entity_id: device_tracker.brian_phone
      state: 'home'
  - condition: state
      entity_id: device_tracker.kathryn_phone
      state: 'home'
  - condition: state
      entity_id: device_tracker.graham_phone
      state: 'home'
  - condition: state
      entity_id: device_tracker.madelyn_phone
      state: 'home'
```

Use template sensors:

```yaml
# ✅ DO: Use template sensor
condition:
  - condition: state
      entity_id: binary_sensor.everyone_home
      state: 'on'
```

## Template Patterns

### Entity Availability Checks

Always check entity availability before using it in conditions or actions:

```yaml
# Single entity
- condition: template
    value_template: "{{ not is_state('entity.id', 'unavailable') and not is_state('entity.id', 'unknown') }}"

# Multiple entities
- condition: template
    value_template: >
      {{ not is_state('entity1', 'unavailable') and
         not is_state('entity1', 'unknown') and
         not is_state('entity2', 'unavailable') and
         not is_state('entity2', 'unknown') }}

# Trigger entity
- condition: template
    value_template: "{{ not is_state(trigger.entity_id, 'unavailable') and not is_state(trigger.entity_id, 'unknown') }}"
```

### Vacation Mode Checks

Use the template sensor instead of checking the input_boolean directly:

```yaml
# ✅ DO: Use template sensor
- condition: state
    entity_id: binary_sensor.vacation_mode_active
    state: 'off'

# ❌ DON'T: Check input_boolean directly (unless you have a specific reason)
- condition: template
    value_template: "{{ not is_state('input_boolean.vacation_mode', 'on') }}"
```

## Standard Automation Structure

Follow this structure for all automations:

```yaml
- id: 'unique_automation_id'
  alias: "Category - Descriptive Name"
  description: 'Clear description of what this automation does'
  
  trigger:
    # Define triggers here
  
  condition:
    # 1. Automation enabled (if using master toggle)
    - condition: state
        entity_id: input_boolean.automation_enabled
        state: 'on'
    
    # 2. Entity availability checks
    - condition: template
        value_template: "{{ not is_state('entity.id', 'unavailable') and not is_state('entity.id', 'unknown') }}"
    
    # 3. Business logic conditions
    - condition: state
        entity_id: binary_sensor.everyone_home
        state: 'on'
    
    # 4. Vacation mode (if applicable)
    - condition: state
        entity_id: binary_sensor.vacation_mode_active
        state: 'off'
  
  action:
    # Actions here
  
  mode: single
```

### Condition Order

1. **Automation enabled check** (if using master toggle)
2. **Entity availability checks** (validate entities before use)
3. **Business logic conditions** (presence, time, state, etc.)
4. **Vacation mode check** (if automation should be disabled during vacation)

## Common Patterns

### Presence-Based Automations

```yaml
# Everyone home
condition:
  - condition: state
      entity_id: binary_sensor.everyone_home
      state: 'on'

# Anyone home
condition:
  - condition: state
      entity_id: binary_sensor.anyone_home
      state: 'on'

# Everyone away
condition:
  - condition: state
      entity_id: binary_sensor.anyone_home
      state: 'off'
```

### Time-Based Conditions

```yaml
# Time range
- condition: time
    after: '07:00:00'
    before: '22:00:00'

# Daytime hours
- condition: time
    after: sunrise
    before: sunset

# Nighttime hours
- condition: time
    after: sunset
    before: sunrise
```

### Conditional Actions

```yaml
action:
  - choose:
      - conditions:
          - condition: state
              entity_id: sensor.example
              state: 'on'
        sequence:
          - service: light.turn_on
              target:
                entity_id: light.example
      - conditions: []  # Default case
        sequence:
          - service: light.turn_off
              target:
                entity_id: light.example
```

## Migration Guide

### Migrating Existing Automations

1. **Add automation enabled check** (if not present):
   ```yaml
   - condition: state
       entity_id: input_boolean.automation_enabled
       state: 'on'
   ```

2. **Replace device tracker checks** with template sensors:
   - Multiple "everyone home" checks → `binary_sensor.everyone_home`
   - Multiple "anyone home" checks → `binary_sensor.anyone_home`

3. **Standardize vacation mode checks**:
   - Replace `input_boolean.vacation_mode` template checks with `binary_sensor.vacation_mode_active` state checks

4. **Add entity availability checks**:
   - Add checks for all entities used in conditions and actions
   - Check both 'unavailable' and 'unknown' states

5. **Reorganize conditions**:
   - Move availability checks to the top
   - Group related conditions together
   - Place vacation mode check at the end (if applicable)

### Example Migration

**Before:**
```yaml
condition:
  - condition: state
      entity_id: device_tracker.brian_phone
      state: 'home'
  - condition: state
      entity_id: device_tracker.kathryn_phone
      state: 'home'
  - condition: template
      value_template: "{{ not is_state('input_boolean.vacation_mode', 'on') }}"
```

**After:**
```yaml
condition:
  - condition: state
      entity_id: input_boolean.automation_enabled
      state: 'on'
  - condition: state
      entity_id: binary_sensor.everyone_home
      state: 'on'
  - condition: state
      entity_id: binary_sensor.vacation_mode_active
      state: 'off'
```

## Naming Conventions

- **Automation IDs**: Use descriptive names like `category_specific_action` or timestamp-based IDs
- **Aliases**: Use format "Category - Specific Action" (e.g., "Light - Morning Kitchen Lights")
- **Descriptions**: Always include a clear description of what the automation does

## Mode Selection

- **`single`**: Default - only one instance can run at a time (prevents overlapping runs)
- **`restart`**: Restart automation if triggered again while running (useful for timers)
- **`queued`**: Queue multiple triggers (useful for notifications)
- **`parallel`**: Run multiple instances in parallel (use only when actions are truly independent)

## Additional Resources

- See `automations/_automation_template.yaml` for a complete template example
- See `packages/template_macros.yaml` for reusable template patterns
- Reference existing automations for examples of best practices

## Questions or Issues?

If you encounter issues or have questions about automation best practices, refer to:
- Home Assistant documentation: https://www.home-assistant.io/docs/automation/
- Template documentation: https://www.home-assistant.io/docs/configuration/templating/

