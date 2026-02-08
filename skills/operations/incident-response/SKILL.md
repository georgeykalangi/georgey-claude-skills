---
name: incident-response
description: Guide incident response workflow with runbooks, communication templates, and escalation procedures. This skill should be used during production incidents, outages, service degradation, or when starting/managing incident response.
---

# Incident Response Skill

## Overview

This skill guides structured incident response following company procedures, including detection, communication, resolution, and post-mortem.

## When to Use This Skill

- Production incidents or outages
- Service degradation
- Security incidents
- Customer-impacting issues
- On-call escalations

## Incident Severity Levels

| Severity | Description | Response Time | Examples |
|----------|-------------|---------------|----------|
| **SEV1** | Critical - Major outage | Immediate | Complete service down, data breach |
| **SEV2** | High - Significant impact | < 30 min | Partial outage, major feature broken |
| **SEV3** | Medium - Limited impact | < 2 hours | Minor feature broken, performance degraded |
| **SEV4** | Low - Minimal impact | < 24 hours | Cosmetic issues, minor bugs |

## Incident Response Workflow

### Phase 1: Detection & Triage (0-5 min)

1. **Acknowledge the incident**
   ```
   /incident acknowledge
   ```

2. **Assess severity** using criteria above

3. **Create incident channel**
   ```
   Slack: #inc-YYYYMMDD-brief-description
   ```

4. **Assign roles**
   - Incident Commander (IC)
   - Technical Lead
   - Communications Lead

### Phase 2: Communication (5-10 min)

**Internal Notification** (Slack #incidents):
```
:rotating_light: INCIDENT DECLARED

Severity: SEV[X]
Summary: [Brief description]
Impact: [Who/what is affected]
Status: Investigating
IC: @[name]
Channel: #inc-[name]
```

**Status Page Update** (for SEV1/SEV2):
```
Title: [Service] - [Issue Type]
Status: Investigating
Message: We are currently investigating issues with [service].
Some users may experience [symptoms]. We will provide updates
as we learn more.
```

**Customer Communication** (for SEV1):
```
Subject: [Service] Status Update

We are aware of an issue affecting [service] and are actively
working to resolve it. [X]% of users may experience [symptoms].

Current status: Investigating
Next update: [time]

We apologize for any inconvenience.
```

### Phase 3: Investigation (Ongoing)

**Diagnostic Checklist**:
- [ ] Check monitoring dashboards
- [ ] Review recent deployments
- [ ] Check error logs
- [ ] Verify infrastructure status
- [ ] Check external dependencies

**Useful Commands**:
```bash
# Check service health
kubectl get pods -n production

# View recent logs
kubectl logs -f deployment/[service] --tail=100

# Check recent deployments
kubectl rollout history deployment/[service]

# Rollback if needed
kubectl rollout undo deployment/[service]
```

**Update Timeline** (every 30 min or on significant change):
```
[HH:MM] Update: [What was checked/discovered]
[HH:MM] Action: [What action was taken]
[HH:MM] Result: [Outcome of action]
```

### Phase 4: Resolution

1. **Confirm fix**
   - Verify metrics returning to normal
   - Confirm customer reports stopped

2. **Update status page**
   ```
   Status: Resolved
   Message: The issue affecting [service] has been resolved.
   All systems are operating normally.
   ```

3. **Close incident channel**
   ```
   :white_check_mark: INCIDENT RESOLVED

   Duration: [X hours Y minutes]
   Root Cause: [Brief description]
   Resolution: [What fixed it]
   Follow-ups: [Any action items]

   Post-mortem scheduled: [date/time]
   ```

### Phase 5: Post-Mortem (Within 48 hours)

**Post-Mortem Template**:

```markdown
# Incident Post-Mortem: [Title]

**Date**: [Date]
**Duration**: [Start] - [End] ([Duration])
**Severity**: SEV[X]
**Author**: [Name]

## Summary
[2-3 sentence summary]

## Impact
- Users affected: [number/percentage]
- Revenue impact: [if applicable]
- Duration: [time]

## Timeline
| Time | Event |
|------|-------|
| HH:MM | [Event] |

## Root Cause
[Detailed explanation]

## Resolution
[What fixed the issue]

## Lessons Learned
### What went well
- [Item]

### What could be improved
- [Item]

## Action Items
| Action | Owner | Due Date |
|--------|-------|----------|
| [Action] | @name | [Date] |
```

## Escalation Paths

| Service | Primary | Secondary | Escalation |
|---------|---------|-----------|------------|
| API | @api-oncall | @platform-lead | @vp-engineering |
| Database | @dba-oncall | @infra-lead | @vp-engineering |
| Auth | @security-oncall | @security-lead | @ciso |

## Quick Reference

**Key Channels**:
- #incidents - Incident declarations
- #oncall - On-call coordination
- #status-updates - Customer-facing updates

**Key Links**:
- [Status Page Admin]
- [Monitoring Dashboard]
- [Runbook Index]
- [Escalation Matrix]

## Assets

- `assets/postmortem_template.md` - Full post-mortem template
- `assets/communication_templates.md` - All comms templates
