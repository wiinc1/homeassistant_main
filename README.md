# Home Assistant Configuration

This is a comprehensive Home Assistant setup for a family home with multiple automation systems.

## Overview

This Home Assistant installation manages:
- **Security**: Window sensors, motion detection, water leak monitoring
- **Cleaning**: Automated vacuum scheduling and room-by-room cleaning
- **Lighting**: Smart lighting control throughout the home
- **Media**: Alexa device integration and media control
- **Weather**: Severe weather alerts and notifications
- **Presence**: Family member presence detection via phone IP tracking

## Key Features

### Security & Monitoring
- Water leak detection in 4 locations (kitchen, laundry, bathrooms)
- Window open notifications for all bedrooms and basement
- Motion sensor monitoring for outdoor areas
- Low battery alerts for all sensors

### Automation Systems
- **Vacuum Smart Rotation**: Automated cleaning based on room usage counters
- **Weather Alerts**: Severe weather announcements via Alexa
- **Presence Detection**: Family member tracking via phone IP addresses
- **Battery Monitoring**: Automated alerts for low battery levels

### Custom Integrations
- `alexa_media`: Enhanced Alexa device control
- `wyzeapi`: Wyze device integration
- `pirateweather`: Weather data
- `presence_simulation`: Presence simulation for testing
- `gasbuddy`: Gas price tracking
- `nest_protect`: Nest Protect smoke detectors
- `auto_backup`: Automated configuration backups
- `iphonedetect`: Phone presence detection
- `hacs`: Home Assistant Community Store
- `nws_alerts`: National Weather Service alerts
- `simple_wyze_vac`: Wyze vacuum control
- `reolink_discovery`: Reolink camera discovery

## Configuration Structure

```
├── configuration.yaml          # Main configuration file
├── secrets.yaml               # Sensitive data (not in git)
├── groups.yaml                # Entity groupings
├── automations/               # Automation files organized by category
│   ├── cleaning/             # Vacuum and cleaning automations
│   ├── notifications/        # Alert and notification automations
│   ├── security/            # Security-related automations
│   └── seasonal/            # Seasonal automations
├── packages/                 # Modular configuration packages
├── custom_components/        # Custom integrations
├── scripts/                  # Reusable scripts
└── inputs/                   # Input helpers
```

## Maintenance

### Regular Tasks
1. **Monitor Logs**: Check `home-assistant.log` for errors
2. **Update Integrations**: Keep custom integrations updated
3. **Battery Management**: Replace batteries when low battery alerts occur
4. **Database Maintenance**: Monitor InfluxDB storage usage

### Known Issues
- Wyze API authentication may need periodic refresh
- Some custom integrations show warnings but are functional
- Consider DHCP reservations for device tracker IP addresses

### Performance Optimization
- Recorder configuration excludes high-frequency updates
- Battery sensors are excluded from recording
- Automation and script states are not recorded

## Security Notes

- Sensitive data is stored in `secrets.yaml` (not committed to git)
- Device tracker uses IP addresses (consider using device names)
- All custom integrations are from trusted sources

## Troubleshooting

### Common Issues
1. **Wyze API Errors**: Check credentials in integration settings
2. **Battery Alerts**: Replace batteries in affected sensors
3. **Network Issues**: Verify device tracker IP addresses are correct
4. **Custom Integration Warnings**: These are normal for untested integrations

### Log Analysis
- Check `home-assistant.log` for detailed error information
- Monitor `home-assistant.log.fault` for system crashes
- Use Home Assistant's built-in log viewer for real-time monitoring

## Version Information
- Home Assistant Version: 2025.7.4
- Last Updated: August 2025