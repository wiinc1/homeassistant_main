#!/usr/bin/env python3
"""
Script to create missing GitHub issues for Home Assistant improvements
"""

import requests
import json
import os
import sys

# GitHub repository details
REPO_OWNER = "wiinc1"
REPO_NAME = "homeassistant_main"
API_BASE = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}"

def create_issue(title, body, labels=None):
    """Create a GitHub issue"""
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
        "Authorization": f"token {os.getenv('GITHUB_TOKEN')}"
    }
    
    data = {
        "title": title,
        "body": body
    }
    
    if labels:
        data["labels"] = labels
    
    response = requests.post(f"{API_BASE}/issues", headers=headers, json=data)
    
    if response.status_code == 201:
        issue_data = response.json()
        print(f"✅ Created issue: {issue_data['title']} (#{issue_data['number']})")
        print(f"   URL: {issue_data['html_url']}")
        return True
    else:
        print(f"❌ Failed to create issue: {title}")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

def main():
    """Main function to create missing issues"""
    print("Creating missing GitHub issues for Home Assistant improvements...")
    print("=" * 60)
    
    issues = [
        {
            "title": "Improve Secrets Management and Security",
            "body": """## Issue Description
Current secrets management and security practices need improvement for better protection of sensitive data.

## Current Issues
- Hardcoded coordinates in secrets.yaml
- Exposed API tokens in configuration
- No environment variable usage for sensitive data
- Limited access control for configuration files

## Impact
- Potential security vulnerabilities
- Risk of credential exposure
- Difficult to manage secrets across environments

## Recommended Actions
1. Implement environment variables for sensitive data
2. Use Home Assistant's built-in secrets management more effectively
3. Review and rotate API tokens regularly
4. Implement proper file permissions for configuration files
5. Consider using external secrets management solutions

## Priority
**Medium** - Security improvement

## Labels
- `enhancement`
- `security`
- `configuration`

## Implementation Steps
1. Audit current secrets usage
2. Migrate to environment variables where appropriate
3. Update documentation for secrets management
4. Implement regular token rotation schedule
5. Review file permissions

## Additional Notes
Consider using Docker secrets or Kubernetes secrets for containerized deployments.""",
            "labels": ["enhancement", "security", "configuration"]
        },
        {
            "title": "Create System Health Monitoring Dashboard",
            "body": """## Issue Description
No centralized monitoring dashboard exists for system health, automation status, and performance metrics.

## Current Issues
- No visibility into system performance
- Difficult to identify automation failures
- No alerts for system issues
- Limited monitoring of custom integrations

## Impact
- Reactive rather than proactive maintenance
- Difficult to identify performance bottlenecks
- No early warning system for issues

## Recommended Actions
1. Create a comprehensive monitoring dashboard
2. Implement system health sensors
3. Add automation failure tracking
4. Create performance monitoring
5. Set up alerting for critical issues

## Priority
**Medium** - Improves maintainability and reliability

## Labels
- `enhancement`
- `monitoring`
- `dashboard`

## Implementation Steps
1. Design dashboard layout and metrics
2. Create system health sensors
3. Implement automation monitoring
4. Set up alerting rules
5. Test and refine monitoring

## Example Dashboard Components
- System uptime and performance
- Automation success/failure rates
- Custom integration status
- Database size and performance
- Network connectivity status""",
            "labels": ["enhancement", "monitoring", "dashboard"]
        },
        {
            "title": "Update and Maintain Custom Integrations",
            "body": """## Issue Description
Multiple custom integrations show warnings and may need updates for compatibility and security.

## Current Custom Integrations
- alexa_media
- wyzeapi
- pirateweather
- presence_simulation
- gasbuddy
- nest_protect
- auto_backup
- iphonedetect
- hacs
- nws_alerts
- simple_wyze_vac
- reolink_discovery

## Impact
- Potential security vulnerabilities
- Compatibility issues with Home Assistant updates
- Performance problems
- Reduced functionality

## Recommended Actions
1. Regularly update all custom integrations
2. Monitor integration compatibility with Home Assistant updates
3. Replace deprecated integrations with official alternatives
4. Test integrations after updates
5. Maintain a list of integration dependencies

## Priority
**Medium** - Security and compatibility

## Labels
- `enhancement`
- `maintenance`
- `integrations`

## Implementation Steps
1. Audit current custom integrations
2. Check for official alternatives
3. Update integrations regularly
4. Test functionality after updates
5. Document integration dependencies

## Additional Notes
Consider setting up automated monitoring for integration updates and compatibility.""",
            "labels": ["enhancement", "maintenance", "integrations"]
        },
        {
            "title": "Implement Automated Configuration Backup Strategy",
            "body": """## Issue Description
Current backup strategy is manual and may not capture all necessary configuration data.

## Current Issues
- Manual backup process
- No automated backup scheduling
- Limited backup retention
- No backup verification
- No disaster recovery plan

## Impact
- Risk of configuration loss
- Difficult recovery process
- No version control for configuration changes

## Recommended Actions
1. Implement automated backup scheduling
2. Create comprehensive backup strategy
3. Add backup verification
4. Implement backup retention policies
5. Create disaster recovery procedures

## Priority
**Medium** - Data protection and recovery

## Labels
- `enhancement`
- `backup`
- `maintenance`

## Implementation Steps
1. Design backup strategy
2. Implement automated backups
3. Add backup verification
4. Test recovery procedures
5. Document backup and recovery processes

## Backup Components
- Configuration files
- Custom components
- Database backups
- Custom scripts
- Integration configurations""",
            "labels": ["enhancement", "backup", "maintenance"]
        },
        {
            "title": "Optimize Database Performance and Storage",
            "body": """## Issue Description
Database performance and storage optimization needed for long-term reliability.

## Current Issues
- Large database size (146MB home-assistant_v2.db)
- No database maintenance schedule
- Potential performance degradation over time
- No data retention policies

## Impact
- Slower system performance
- Increased disk space usage
- Potential data corruption
- Difficult troubleshooting

## Recommended Actions
1. Implement database maintenance schedule
2. Set up data retention policies
3. Optimize recorder configuration
4. Monitor database performance
5. Implement database cleanup procedures

## Priority
**Low** - Performance optimization

## Labels
- `enhancement`
- `performance`
- `database`

## Implementation Steps
1. Analyze current database usage
2. Implement maintenance procedures
3. Set up monitoring
4. Test performance improvements
5. Document maintenance procedures

## Additional Notes
Consider using external databases (PostgreSQL) for better performance with large datasets.""",
            "labels": ["enhancement", "performance", "database"]
        },
        {
            "title": "Improve Code Quality with Templates and Helpers",
            "body": """## Issue Description
Automation code could benefit from better use of templates, helper entities, and improved structure.

## Current Issues
- Repetitive code in automations
- No helper entities for common conditions
- Limited use of templates
- Inconsistent automation structure

## Impact
- Difficult to maintain automations
- Code duplication
- Reduced readability
- Harder to debug issues

## Recommended Actions
1. Create helper entities for common conditions
2. Implement template-based automations
3. Standardize automation structure
4. Add input validation
5. Create reusable automation components

## Priority
**Low** - Code quality improvement

## Labels
- `enhancement`
- `automation`
- `code-quality`

## Implementation Examples
```yaml
# Helper entity example
input_boolean:
  everyone_home:
    name: Everyone Home
    icon: mdi:home-group

# Template example
template:
  - sensor.everyone_home:
      friendly_name: "Everyone Home"
      value_template: >
        {{ is_state('device_tracker.brian_phone', 'home') and
           is_state('device_tracker.kathryn_phone', 'home') and
           is_state('device_tracker.graham_phone', 'home') and
           is_state('device_tracker.madelyn_phone', 'home') }}
```

## Implementation Steps
1. Identify common automation patterns
2. Create helper entities
3. Refactor automations to use templates
4. Standardize automation structure
5. Document best practices""",
            "labels": ["enhancement", "automation", "code-quality"]
        }
    ]
    
    success_count = 0
    total_count = len(issues)
    
    for issue in issues:
        print(f"\nCreating issue: {issue['title']}")
        if create_issue(issue['title'], issue['body'], issue['labels']):
            success_count += 1
    
    print("\n" + "=" * 60)
    print(f"Summary: {success_count}/{total_count} additional issues created successfully")
    if success_count > 0:
        print(f"You can view them at: https://github.com/{REPO_OWNER}/{REPO_NAME}/issues")
    
    return success_count == total_count

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

