# Contributing to Georgey's Claude Skills

Thank you for contributing to this skills repository!

## Before You Start

- Ensure your skill is based on a **real use case**
- Check existing skills to avoid duplicates
- Get approval from the category owner

## Skill Requirements

All skills must:

1. **Solve a real problem** - Based on actual usage
2. **Be well-documented** - Clear instructions and examples
3. **Be tested** - Verified across Claude.ai and Claude Code
4. **Be safe** - Confirm before destructive operations
5. **Follow security guidelines** - No hardcoded secrets

## Skill Structure

```
skill-name/
├── SKILL.md          # Required: Skill instructions
├── scripts/          # Optional: Helper scripts
├── references/       # Optional: Documentation
└── assets/           # Optional: Templates, images
```

## SKILL.md Template

```markdown
---
name: skill-name
description: One-sentence description with trigger conditions.
---

# Skill Name

## Overview
[Purpose and capabilities]

## When to Use
- [Trigger condition 1]
- [Trigger condition 2]

## Workflow
[Step-by-step instructions for Claude]

## Examples
[Real usage examples with expected output]
```

## Pull Request Process

1. Fork/branch: `git checkout -b add-skill-name`
2. Add skill folder with SKILL.md
3. Update `.claude-plugin/marketplace.json`
4. Submit PR with:
   - What problem it solves
   - Who uses this workflow
   - Example usage

## Questions?

Open an issue on GitHub or reach out directly.
