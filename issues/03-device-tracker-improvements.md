# Improve Device Tracker Configuration

## Issue Description
Device tracker configuration uses hardcoded IP addresses which can become unreliable when IP addresses change.

## Current Configuration
```yaml
hosts:
  brian_phone: 192.168.1.34 
  graham_phone: 192.168.1.225
  madelyn_phone: 192.168.1.155
  kathryn_phone: 192.168.1.23
```

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
- `enhancement`
- `device-tracker`
- `network`

## Implementation Steps
1. Configure router DHCP reservations
2. Update device tracker configuration
3. Test presence detection reliability
4. Add monitoring and alerts

## Additional Notes
DHCP reservations provide more reliable device tracking than hardcoded IP addresses.
