#!/usr/bin/env python3
"""
Validate a Claude skill structure and contents.

Usage:
    python validate_skill.py <path-to-skill>
    python validate_skill.py ./skills/engineering/code-review/

Checks:
    - SKILL.md exists and has valid YAML frontmatter
    - Required fields (name, description) are present
    - Description is descriptive enough
    - Directory structure is valid
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple


def parse_frontmatter(content: str) -> Tuple[dict, str]:
    """Parse YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return {}, content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content

    frontmatter = {}
    for line in parts[1].strip().split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            frontmatter[key.strip()] = value.strip().strip('"\'')

    return frontmatter, parts[2]


def validate_skill(skill_path: Path) -> List[str]:
    """Validate a skill and return list of errors."""
    errors = []

    # Check SKILL.md exists
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        errors.append("SKILL.md file not found")
        return errors

    content = skill_md.read_text()
    frontmatter, body = parse_frontmatter(content)

    # Check required fields
    if "name" not in frontmatter:
        errors.append("Missing required field 'name' in frontmatter")
    elif not re.match(r"^[a-z][a-z0-9-]*$", frontmatter["name"]):
        errors.append(f"Invalid name format: {frontmatter['name']}. Use lowercase letters, numbers, and hyphens.")

    if "description" not in frontmatter:
        errors.append("Missing required field 'description' in frontmatter")
    else:
        desc = frontmatter["description"]
        if len(desc) < 50:
            errors.append(f"Description too short ({len(desc)} chars). Should be at least 50 characters.")
        if "TODO" in desc:
            errors.append("Description contains TODO placeholder")
        if not any(trigger in desc.lower() for trigger in ["when", "use", "should", "for"]):
            errors.append("Description should explain when to use this skill")

    # Check body content
    if len(body.strip()) < 100:
        errors.append("SKILL.md body is too short. Add detailed instructions.")

    if "TODO" in body:
        errors.append("SKILL.md body contains TODO placeholders")

    # Check for recommended sections
    recommended_sections = ["When to Use", "Workflow", "Example"]
    for section in recommended_sections:
        if section.lower() not in body.lower():
            errors.append(f"Missing recommended section: '{section}'")

    # Check directory structure
    for subdir in ["scripts", "references", "assets"]:
        subpath = skill_path / subdir
        if subpath.exists() and subpath.is_dir():
            files = list(subpath.glob("*"))
            # Check for placeholder files
            for f in files:
                if f.name != ".gitkeep" and f.is_file():
                    file_content = f.read_text()
                    if "TODO" in file_content:
                        errors.append(f"File {subdir}/{f.name} contains TODO placeholders")

    return errors


def main():
    parser = argparse.ArgumentParser(
        description="Validate a Claude skill structure",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("skill_path", help="Path to the skill directory")
    parser.add_argument("--strict", action="store_true", help="Fail on warnings too")

    args = parser.parse_args()
    skill_path = Path(args.skill_path)

    if not skill_path.exists():
        print(f"Error: Path does not exist: {skill_path}")
        sys.exit(1)

    if not skill_path.is_dir():
        print(f"Error: Path is not a directory: {skill_path}")
        sys.exit(1)

    print(f"Validating skill: {skill_path}")
    print("-" * 50)

    errors = validate_skill(skill_path)

    if errors:
        print("Validation FAILED:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("Validation PASSED")
        print("Skill is ready for use!")
        sys.exit(0)


if __name__ == "__main__":
    main()
