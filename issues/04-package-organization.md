# Complete Package Organization Structure

## Issue Description
Many package directories are empty, suggesting incomplete organization of configuration files.

## Current State
```
packages/
├── core/          # Empty
├── lighting/      # Empty  
├── media/         # Empty
├── security/      # Empty
├── climate/       # Empty
├── groups.yaml    # Empty
├── sensors.yaml   # Empty
├── lights.yaml    # Empty
└── switches.yaml  # Empty
```

## Impact
- Inconsistent configuration organization
- Difficult to maintain and understand
- Poor separation of concerns

## Recommended Actions
1. Move related configurations into appropriate package directories
2. Create package files for each domain (lighting, security, etc.)
3. Implement consistent naming conventions
4. Add documentation for each package

## Priority
**Medium** - Improves maintainability

## Labels
- `enhancement`
- `organization`
- `documentation`

## Implementation Steps
1. Audit current configuration files
2. Create package files for each domain
3. Move configurations to appropriate packages
4. Update main configuration.yaml references
5. Add package documentation

## Example Package Structure
```yaml
# packages/lighting/lights.yaml
light:
  - platform: mqtt
    name: "Kitchen Light"
    # ... configuration
```
