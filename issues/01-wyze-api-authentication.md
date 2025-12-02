# Fix Wyze API Authentication Issues

## Issue Description
The Simple Wyze Vac integration is failing with a 400 Bad Request error during authentication.

## Current Error
```
requests.exceptions.HTTPError: 400 Client Error: Bad Request for url: https://auth-prod.api.wyze.com/api/user/login
```

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
- `bug`
- `integration`
- `high-priority`

## Steps to Reproduce
1. Check Home Assistant logs
2. Look for Wyze API authentication errors
3. Verify integration configuration

## Additional Notes
This appears to be a credential/authentication issue rather than a code problem.
