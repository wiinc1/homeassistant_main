# Changelog Entry Template & Guidelines

This document provides the template and guidelines for adding entries to `CHANGELOG.md`. Follow these standards to ensure consistency and clarity in documenting project changes.

## Format Overview

Our changelog follows the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format and adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) (SemVer).

### Structure

```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added
- New features

### Changed
- Changes to existing functionality

### Deprecated
- Features soon to be removed

### Removed
- Removed features

### Fixed
- Bug fixes

### Security
- Security fixes

## [Version] - YYYY-MM-DD

### Added
- Feature entries

### Changed
- Change entries

### Fixed
- Fix entries

### Security
- Security entries
```

---

## Entry Template

### Basic Entry Format

```markdown
- **Feature/Change Title**
  - Primary description of the change
  - Key implementation details
  - Impact on users/devices
  - Breaking changes (if any)
```

### Detailed Entry Format

```markdown
- **Feature/Change Title**
  - Brief summary (1-2 sentences)
  - **Technical Details:**
    - Specific implementation points
    - Entities affected
    - Trigger/condition changes
  - **User Impact:**
    - What users will notice
    - Behavioral changes
  - **Breaking Changes:**
    - What changed that might affect existing automations
```

---

## Change Categories

### Added
Use for new automations, entities, or capabilities.

**When to use:**
- New automation files
- New template sensors
- New input helpers
- New integrations

### Changed
Use for changes to existing automations that modify behavior.

**When to use:**
- Trigger changes (time-based to presence-based, etc.)
- Condition modifications
- Action sequence changes
- Schedule adjustments

### Deprecated
Use for automations or features that will be removed.

### Removed
Use for deleted automations or features.

### Fixed
Use for bug fixes and corrections.

**When to use:**
- Timing fixes
- Entity reference corrections
- Condition logic fixes

### Security
Use for security-related changes.

---

## Writing Guidelines

### 1. Write for Human Impact
Focus on **user impact** rather than technical implementation details.

**Bad:**
```markdown
- Refactored trigger platform from time to state
```

**Good:**
```markdown
- Christmas tree now turns on automatically when arriving home instead of fixed schedule
```

### 2. Include Relevant Details
- Mention affected entities and devices
- Note time windows or conditions
- Include any schedule changes

### 3. Group Related Changes
Group multiple related changes under a single entry with bullet points.

### 4. Highlight Breaking Changes
Always clearly mark breaking changes.

---

## Examples

### Example 1: Automation Change

```markdown
### Changed
- **Laurel Christmas Tree - Presence-Based Control**
  - Changed from fixed time schedule to presence-based triggers
  - Tree turns on when Laurel arrives home (8AM-9PM window)
  - Tree turns off when Laurel leaves home (5-minute delay)
  - Evening cutoff at 9PM preserved
  - Entities: `switch.basementchristmastree`, `device_tracker.laurel_watch`
```

### Example 2: New Automation

```markdown
### Added
- **Madelyn Christmas Tree Off When Away**
  - New automation to turn off tree when Madelyn leaves home
  - Triggers after 5 minutes of `not_home` state
  - Entity: `switch.madelynvanitydesk`
  - Tracker: `device_tracker.madelyn_phone`
```

### Example 3: Bug Fix

```markdown
### Fixed
- **Christmas Tree Timing Issue**
  - Fixed incorrect trigger times for weekend schedule
  - Corrected morning on time from 8:30 to 9:00
```

---

## Quick Reference Checklist

When adding a changelog entry, ensure:

- [ ] Entry is in the correct category (Added/Changed/Fixed/etc.)
- [ ] Entry is written for user impact
- [ ] Affected entities are mentioned
- [ ] Breaking changes are clearly marked
- [ ] Entry is placed under `[Unreleased]` or appropriate version
- [ ] Entry follows the template format

---

**Last Updated**: 2025-12-18
