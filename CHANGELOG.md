# Home Assistant Automation Changelog

See [CHANGELOG_TEMPLATE.md](CHANGELOG_TEMPLATE.md) for entry format guidelines.

---

## 2025-12-18 - Lights Off When Away (Issue #35)

### Added
- **Madelyn Lights Off When Away**
  - Automatically turns off all Madelyn's room lights when she leaves home
  - Triggers after 5 minutes of `not_home` state (prevents GPS glitch false triggers)
  - Entities: `light.madelynlamp`, `light.madelynroomlights`, `switch.madelynroomswitch`, `switch.madelynvanitylight`
  - Tracker: `device_tracker.madelyn_phone`
  - File: `automations/lights/madelyn_lights_off_away.yaml`

- **Laurel Lights Off When Away**
  - Automatically turns off all Laurel's room lights when she leaves home
  - Triggers after 5 minutes of `not_home` state (prevents GPS glitch false triggers)
  - Entities: `light.laurellamp`, `light.laurelroomlights`, `switch.laurelroomswitch`, `switch.christmastreelaurel`, `switch.laurel_vanity`
  - Tracker: `device_tracker.laurel_watch`
  - File: `automations/lights/laurel_lights_off_away.yaml`

---

## 2025-12-18 - Presence-Based Christmas Tree Automations

### Changed - Madelyn & Laurel Christmas Tree Triggers

**WHY (Motivation):**
- User requested Christmas trees turn on based on presence detection rather than fixed schedules
- Trees should turn on when the person arrives home (between 8AM-9PM) and turn off when they leave
- Existing evening cutoff times should be preserved as a hard stop

**WHAT (Solution):**
- Replaced time-based "on" triggers with presence-based triggers using device trackers
- Added time window condition (8AM-9PM) for presence-triggered turn-on
- Preserved existing evening cutoff times (hard stop regardless of presence)
- Created new away automation for Madelyn (Laurel's already existed)

**IMPACT:**
- **Madelyn's tree** (`switch.madelynvanitydesk`):
  - Turns ON when `device_tracker.madelyn_phone` arrives home (8AM-9PM)
  - Turns OFF when she leaves home (5-minute delay)
  - Turns OFF at 10:30PM weekday / 11PM weekend (hard cutoff)
- **Laurel's tree** (`switch.basementchristmastree`):
  - Turns ON when `device_tracker.laurel_watch` arrives home (8AM-9PM)
  - Turns OFF when she leaves home (5-minute delay)
  - Turns OFF at 9PM all days (hard cutoff)

**FILES MODIFIED:**
- `/opt/homeassistant/automations/seasonal/madelyn_christmas_tree_weekday.yaml` - presence trigger + 10:30pm off
- `/opt/homeassistant/automations/seasonal/madelyn_christmas_tree_weekend.yaml` - presence trigger + 11pm off
- `/opt/homeassistant/automations/seasonal/laurel_christmas_tree_weekday.yaml` - presence trigger + 9pm off
- `/opt/homeassistant/automations/seasonal/laurel_christmas_tree_weekend.yaml` - presence trigger + 9pm off

### Added - Madelyn Christmas Tree Off When Away

**WHAT (Solution):**
- New automation file to turn off Madelyn's tree when she leaves home
- Mirrors existing Laurel away automation pattern
- 5-minute delay prevents false triggers from GPS glitches

**FILES CREATED:**
- `/opt/homeassistant/automations/seasonal/madelyn_christmas_tree_off_away.yaml`

### Added - Changelog Template

**WHAT (Solution):**
- Created changelog template file with guidelines for future entries
- Adapted from detailed template to fit Home Assistant automation context

**FILES CREATED:**
- `/opt/homeassistant/changelog_template.md`

---

## 2025-12-11 09:15 CST

### Fixed - Automation Watchdog Schedule Loading (Log Error)

**WHY (Motivation):**
- Watchdog automation failed with `from_json` template error on every HA restart
- Previous fix (adding condition + default) didn't resolve it - `input_text.set_value` also has 255 char limit
- Root cause: Home Assistant has a hard-coded 255 character limit on `input_text` values regardless of `max:` setting
- Impact: Watchdog couldn't monitor scheduled automations, no Discord alerts for automation failures

**WHAT (Solution):**
- Moved schedule data from `input_text` entity to external JSON file (`/config/automation_schedule.json`)
- Updated automation to read file directly using Jinja's `read_file` filter
- Removed `input_text.automation_schedule` entity entirely (no longer needed)

**IMPACT:**
- Eliminated all startup errors related to watchdog
- Watchdog now reliably monitors all 22 scheduled automation events
- Schedule is easier to maintain - standard JSON file with no character limits
- No dependency on entity state initialization timing

**FILES MODIFIED:**
- `/opt/homeassistant/packages/automation_watchdog.yaml` - removed input_text, updated schedule variable
- `/opt/homeassistant/automation_schedule.json` - new file containing schedule data

**VERIFICATION:**
```bash
docker logs homeassistant --since 5m | grep -iE "watchdog|from_json|255"
# Result: No errors
```

---

## 2025-12-11 08:45 CST

### Fixed - Automation Watchdog Error Handling (Log Error)

**WHY (Motivation):**
- Watchdog automation was throwing errors in logs at scheduled check times (e.g., 08:32, 23:02)
- Error: `ValueError: Template error: from_json got invalid input 'unknown'`
- Occurred because `input_text.automation_schedule` was 'unknown' after HA restarts before initialization
- Impact: Log spam, potential missed monitoring of scheduled automations

**WHAT (Solution):**
- Added condition to skip automation execution when schedule state is 'unknown' or 'unavailable'
- Added `default=[]` to `from_json` filter as safety net

**IMPACT:**
- Eliminated template errors in logs
- Watchdog gracefully skips execution during HA startup phase
- Note: This was later superseded by the JSON file solution above

**FILES MODIFIED:**
- `/opt/homeassistant/packages/automation_watchdog.yaml`

---

## 2025-12-11 08:23 CST

### Changed - Stairway Light Timing Adjustments (User Request)

**WHY (Motivation):**
- User requested stairway light turn off later in the morning (was turning off at sunrise)
- During winter months, sunrise occurs but interior light levels remain low
- User also wanted lights to turn on earlier in the evening before it gets dark inside

**WHAT (Solution):**
- Modified sunrise trigger offset from `0` to `"02:00:00"` (2 hours after sunrise)
- Added sunset trigger offset `"-01:30:00"` (90 minutes before sunset)

**IMPACT:**
- Stairway light stays on 2 hours longer in the morning for adequate interior lighting
- Stairway light turns on 90 minutes earlier in the evening, before house gets dark
- Better matches actual interior lighting needs vs astronomical sunrise/sunset times

**FILES MODIFIED:**
- `/opt/homeassistant/automations/lights/lights_stairway_sunrise.yaml` - added 2hr offset
- `/opt/homeassistant/automations/lights/stairway_light_level_adjustment.yaml` - added -90min offset

---

## 2025-12-11 08:23 CST

### Fixed - Multiple Automations Silently Disabled Since Nov 30 (User Report)

**WHY (Motivation):**
- User reported Christmas outdoor lights didn't turn off at 11 PM on 2025-12-10
- User also reported stairway lights were off at 6:30 AM when they should have been on
- Investigation revealed 5 automations had been silently disabled since 2025-11-30
- Root cause: YAML files had `max_exceeded: 1` (integer) instead of `max_exceeded: silent` (string)
- HA validated and rejected the automations but `core.restore_state` still showed `state: on` - misleading

**WHAT (Solution):**
- Verified YAML files had been corrected to use `max_exceeded: silent`
- Restarted Home Assistant container to reload automations fresh
- Confirmed all automations loaded without validation errors

**IMPACT:**
- Restored automatic control of Christmas outdoor lights (sunset on, 11 PM off)
- Restored automatic control of stairway lights (dark/cloudy on, sunrise+2hr off, bright off)
- 5 automations now functioning after ~11 days of being silently disabled

**FILES MODIFIED:**
- No files modified (YAML was already corrected)
- Docker container restarted to clear cached disabled state

**AFFECTED AUTOMATIONS:**
1. `Lights - Stairway Off At Sunrise` - controls `light.lightstairway`
2. `Lights - Stairway Off When Bright` - controls `light.lightstairway`
3. `Lights - Stairway On When Dark or Cloudy` - controls `light.lightstairway`
4. `Lights - Christmas: Outside Decorations On` - controls `switch.christmasoutdoorplug` (1-4)
5. `Lights - Christmas: Outside Decorations Off` - controls `switch.christmasoutdoorplug` (1-4)

**VERIFICATION:**
```bash
# Check for validation errors after restart
docker logs homeassistant --since 5m 2>&1 | grep -iE "stairway|christmas.*decoration" | grep -iE "error|disabled"
# Result: No errors found

# Check automation states
grep -E "automation.*(stairway|christmas_decorations|christmas_outside)" /opt/homeassistant/.storage/core.restore_state
# Result: All show state: on with fresh timestamps
```

**LESSONS LEARNED:**
1. Don't trust `restore_state` alone - always check startup logs for validation errors
2. `max_exceeded` requires strings (`silent`, `warn`, `error`) not integers
3. HA can cache disabled state that persists even after YAML is fixed - restart required
4. Useful diagnostic command:
   ```bash
   docker logs homeassistant 2>&1 | grep -i "could not be validated\|disabled"
   ```

---
