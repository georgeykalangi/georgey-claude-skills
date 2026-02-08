#!/usr/bin/env python3
"""
Initialize a new Claude skill with the standard directory structure.

Usage:
    python init_skill.py <skill-name> --path <output-directory>
    python init_skill.py my-new-skill --path ./skills/engineering/

Example:
    python init_skill.py api-integration --path ./skills/integrations/
"""

import argparse
import os
from pathlib import Path

SKILL_MD_TEMPLATE = '''---
name: {skill_name}
description: TODO - Add a description of when this skill should be used. Be specific about trigger conditions.
---

# {skill_title}

## Overview

TODO - Describe the purpose and capabilities of this skill.

## When to Use This Skill

- TODO - Trigger condition 1
- TODO - Trigger condition 2
- TODO - Trigger condition 3

## Workflow

### Step 1: [Action]

TODO - Instructions for Claude

### Step 2: [Action]

TODO - Instructions for Claude

## Examples

**User Request**: "TODO - Example prompt"

**Expected Output**:
```
TODO - Show expected output
```

## Error Handling

- If [error condition], then [action]

## References

- Load `references/example.md` for additional context (delete if not needed)
'''

REFERENCE_TEMPLATE = '''# Reference Documentation

TODO - Add reference documentation that Claude should load as needed.

This file should contain:
- Detailed specifications
- API documentation
- Schema definitions
- Extended examples

Keep this separate from SKILL.md to avoid loading unnecessary context.
'''

SCRIPT_TEMPLATE = '''#!/usr/bin/env python3
"""
TODO - Description of what this script does.

Usage:
    python {script_name}.py <args>
"""

import argparse


def main():
    parser = argparse.ArgumentParser(description="TODO - Script description")
    parser.add_argument("input", help="TODO - Input description")
    args = parser.parse_args()

    # TODO - Implement script logic
    print(f"Processing: {{args.input}}")


if __name__ == "__main__":
    main()
'''


def create_skill(skill_name: str, output_path: str) -> None:
    """Create a new skill directory with template files."""

    # Validate skill name
    if not skill_name.replace("-", "").replace("_", "").isalnum():
        raise ValueError(f"Invalid skill name: {skill_name}. Use only letters, numbers, and hyphens.")

    skill_path = Path(output_path) / skill_name

    if skill_path.exists():
        raise FileExistsError(f"Skill directory already exists: {skill_path}")

    # Create directories
    (skill_path / "scripts").mkdir(parents=True, exist_ok=True)
    (skill_path / "references").mkdir(parents=True, exist_ok=True)
    (skill_path / "assets").mkdir(parents=True, exist_ok=True)

    # Create SKILL.md
    skill_title = skill_name.replace("-", " ").replace("_", " ").title()
    skill_md_content = SKILL_MD_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    )
    (skill_path / "SKILL.md").write_text(skill_md_content)

    # Create example reference
    (skill_path / "references" / "example.md").write_text(REFERENCE_TEMPLATE)

    # Create example script
    script_content = SCRIPT_TEMPLATE.format(script_name="example")
    (skill_path / "scripts" / "example.py").write_text(script_content)

    # Create .gitkeep for assets
    (skill_path / "assets" / ".gitkeep").write_text("")

    print(f"Created skill: {skill_path}")
    print(f"")
    print(f"Next steps:")
    print(f"  1. Edit {skill_path}/SKILL.md with your skill instructions")
    print(f"  2. Add scripts to {skill_path}/scripts/ if needed")
    print(f"  3. Add reference docs to {skill_path}/references/ if needed")
    print(f"  4. Add templates/assets to {skill_path}/assets/ if needed")
    print(f"  5. Update .claude-plugin/marketplace.json to register the skill")


def main():
    parser = argparse.ArgumentParser(
        description="Initialize a new Claude skill",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    python init_skill.py my-skill --path ./skills/engineering/
    python init_skill.py api-helper --path ./skills/integrations/
        """
    )
    parser.add_argument("skill_name", help="Name of the skill (use kebab-case)")
    parser.add_argument("--path", "-p", default=".", help="Output directory (default: current directory)")

    args = parser.parse_args()

    try:
        create_skill(args.skill_name, args.path)
    except (ValueError, FileExistsError) as e:
        print(f"Error: {e}")
        exit(1)


if __name__ == "__main__":
    main()
