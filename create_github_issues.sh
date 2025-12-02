#!/bin/bash

# Script to create GitHub issues for Home Assistant improvements
# Usage: ./create_github_issues.sh

echo "Creating GitHub issues for Home Assistant improvements..."

# Issue 1: Wyze API Authentication
echo "Creating issue: Fix Wyze API Authentication Issues"
gh issue create \
  --title "Fix Wyze API Authentication Issues" \
  --body "## Issue Description
The Simple Wyze Vac integration is failing with a 400 Bad Request error during authentication.

## Current Error
\`\`\`
requests.exceptions.HTTPError: 400 Client Error: Bad Request for url: https://auth-prod.api.wyze.com/api/user/login
\`\`\`

## Impact
- Vacuum automation functionality is broken
- Integration setup fails on Home Assistant startup

## Recommended Actions
1. Check Wyze account credentials in the integration settings
2. Verify 2FA settings if enabled
3. Consider regenerating API keys
4. Update the simple_wyze_vac custom integration to latest version

## Priority
**High** - This affects core automation functionality

## Labels
- \`bug\`
- \`integration\`
- \`high-priority\`

## Steps to Reproduce
1. Check Home Assistant logs
2. Look for Wyze API authentication errors
3. Verify integration configuration

## Additional Notes
This appears to be a credential/authentication issue rather than a code problem." \
  --label "bug,integration,high-priority"

# Issue 2: Segmentation Faults
echo "Creating issue: Address Python Segmentation Faults"
gh issue create \
  --title "Address Python Segmentation Faults" \
  --body "## Issue Description
Home Assistant is experiencing fatal Python segmentation faults, indicating memory corruption or compatibility issues.

## Current Error
\`\`\`
Fatal Python error: Segmentation fault
Thread 0x0000709da4d1fb30 (most recent call first):
  File \"/usr/local/lib/python3.13/concurrent/futures/thread.py\", line 89 in _worker
\`\`\`

## Impact
- System crashes and instability
- Potential data loss
- Reduced reliability

## Recommended Actions
1. Update Python dependencies to latest compatible versions
2. Check for memory leaks in custom integrations
3. Consider updating Home Assistant to latest version
4. Monitor system resources (CPU, memory usage)
5. Review custom integration compatibility

## Priority
**High** - System stability issue

## Labels
- \`bug\`
- \`system\`
- \`high-priority\`
- \`stability\`

## Steps to Reproduce
1. Monitor \`home-assistant.log.fault\` for crash reports
2. Check system resource usage during crashes
3. Review custom integration activity before crashes

## Additional Notes
Segmentation faults often indicate memory management issues or incompatible library versions." \
  --label "bug,system,high-priority,stability"

# Issue 3: Device Tracker Improvements
echo "Creating issue: Improve Device Tracker Configuration"
gh issue create \
  --title "Improve Device Tracker Configuration" \
  --body "## Issue Description
Device tracker configuration uses hardcoded IP addresses which can become unreliable when IP addresses change.

## Current Configuration
\`\`\`yaml
hosts:
  brian_phone: 192.168.1.34 
  graham_phone: 192.168.1.225
  madelyn_phone: 192.168.1.155
  kathryn_phone: 192.168.1.23
\`\`\`

## Impact
- Device tracking fails when IP addresses change
- Manual configuration updates required
- Reduced reliability of presence detection

## Recommended Actions
1. Set up DHCP reservations for family phones
2. Consider using device names instead of IP addresses
3. Implement fallback detection methods
4. Add monitoring for device tracker failures

## Priority
**Medium** - Affects presence detection reliability

## Labels
- \`enhancement\`
- \`device-tracker\`
- \`network\`

## Implementation Steps
1. Configure router DHCP reservations
2. Update device tracker configuration
3. Test presence detection reliability
4. Add monitoring and alerts

## Additional Notes
DHCP reservations provide more reliable device tracking than hardcoded IP addresses." \
  --label "enhancement,device-tracker,network"

# Issue 4: Package Organization
echo "Creating issue: Complete Package Organization Structure"
gh issue create \
  --title "Complete Package Organization Structure" \
  --body "## Issue Description
Many package directories are empty, suggesting incomplete organization of configuration files.

## Current State
\`\`\`
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
\`\`\`

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
- \`enhancement\`
- \`organization\`
- \`documentation\`

## Implementation Steps
1. Audit current configuration files
2. Create package files for each domain
3. Move configurations to appropriate packages
4. Update main configuration.yaml references
5. Add package documentation

## Example Package Structure
\`\`\`yaml
# packages/lighting/lights.yaml
light:
  - platform: mqtt
    name: \"Kitchen Light\"
    # ... configuration
\`\`\`" \
  --label "enhancement,organization,documentation"

# Issue 5: Automation Error Handling
echo "Creating issue: Add Error Handling to Automations"
gh issue create \
  --title "Add Error Handling to Automations" \
  --body "## Issue Description
Automations lack error handling for network failures, API errors, and other potential issues.

## Current Issues
- No fallback behavior when services fail
- No retry logic for transient failures
- No logging of automation failures
- No user notification when automations fail

## Impact
- Silent failures reduce reliability
- Difficult to troubleshoot issues
- Poor user experience when automations don't work

## Recommended Actions
1. Add try-catch blocks for critical automations
2. Implement retry logic for network-dependent actions
3. Add failure notifications to users
4. Create monitoring dashboard for automation health
5. Add logging for automation failures

## Priority
**Medium** - Improves reliability and debugging

## Labels
- \`enhancement\`
- \`automation\`
- \`reliability\`
- \`monitoring\`

## Implementation Examples
\`\`\`yaml
# Example with error handling
action:
  - service: notify.mobile_app
    data:
      message: \"Automation started\"
  - try:
      - service: light.turn_on
        target:
          entity_id: light.kitchen
    except:
      - service: notify.mobile_app
        data:
          message: \"Failed to turn on kitchen light\"
\`\`\`

## Affected Automations
- Water leak detection
- Weather alerts
- Vacuum scheduling
- Window notifications" \
  --label "enhancement,automation,reliability,monitoring"

# Issue 6: Log Rotation
echo "Creating issue: Implement Log Rotation"
gh issue create \
  --title "Implement Log Rotation" \
  --body "## Issue Description
Log files are growing without rotation, potentially consuming significant disk space.

## Current Issues
- \`home-assistant.log\` is 19KB and growing
- \`home-assistant.log.fault\` is 22KB
- No automatic log rotation configured
- Potential disk space issues over time

## Impact
- Disk space consumption
- Difficult to find recent log entries
- Potential system performance impact

## Recommended Actions
1. Configure logrotate for Home Assistant logs
2. Set up automatic log compression and cleanup
3. Implement log level filtering
4. Create log monitoring and alerts

## Priority
**Low** - Maintenance improvement

## Labels
- \`enhancement\`
- \`maintenance\`
- \`logging\`

## Implementation Steps
1. Create logrotate configuration
2. Test log rotation functionality
3. Monitor disk space usage
4. Set up alerts for log size thresholds

## Example logrotate config
\`\`\`
/opt/homeassistant/*.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 homeassistant homeassistant
}
\`\`\`" \
  --label "enhancement,maintenance,logging"

echo "All issues created successfully!"
echo "You can view them at: https://github.com/wiinc1/homeassistant_main/issues"
