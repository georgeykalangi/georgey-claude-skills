---
name: git-workflow
description: Git workflow automation with conventional commits, branch naming, PR templates, rebase guidance, and release tagging. This skill should be used when committing code, creating branches, writing PR descriptions, or managing releases.
---

# Git Workflow Skill

## Overview

This skill automates and standardizes Git workflows including conventional commit messages, branch naming conventions, PR description templates, interactive rebase guidance, and release tagging with changelogs.

## When to Use This Skill

- Writing commit messages
- Creating feature/fix branches
- Writing PR descriptions
- Performing interactive rebases
- Tagging releases and generating changelogs
- Setting up Git hooks

## Conventional Commits

### Format

```
<type>(<scope>): <subject>

[optional body]

[optional footer(s)]
```

### Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(auth): add OAuth2 login` |
| `fix` | Bug fix | `fix(api): handle null user in response` |
| `docs` | Documentation | `docs(readme): update installation steps` |
| `style` | Formatting (no logic change) | `style: fix linting errors` |
| `refactor` | Code restructure (no behavior change) | `refactor(db): extract query builder` |
| `perf` | Performance improvement | `perf(search): add index on user_email` |
| `test` | Adding/updating tests | `test(auth): add JWT expiry tests` |
| `build` | Build system/dependencies | `build: upgrade FastAPI to 0.110` |
| `ci` | CI/CD changes | `ci: add staging deploy step` |
| `chore` | Maintenance tasks | `chore: clean up unused imports` |

### Commit Message Rules

- Subject line: max 72 characters, imperative mood ("add" not "added")
- Body: explain **why**, not **what** (the diff shows what)
- Footer: reference issues (`Closes #123`, `Refs #456`)

### Breaking Changes

```
feat(api)!: change authentication to OAuth2

BREAKING CHANGE: Bearer token format changed from JWT to OAuth2 access token.
Clients must update their token refresh logic.

Migration guide: docs/migration-v2.md
```

## Branch Naming

### Convention

```
<type>/<ticket-id>-<short-description>
```

### Examples

| Pattern | Example |
|---------|---------|
| Feature | `feature/PROJ-123-user-auth` |
| Bug fix | `fix/PROJ-456-null-pointer-login` |
| Hotfix | `hotfix/PROJ-789-prod-crash` |
| Refactor | `refactor/PROJ-101-extract-service` |
| Docs | `docs/update-api-reference` |
| Experiment | `experiment/try-qdrant-vector-db` |

### Branch Commands

```bash
# Create and switch to new branch
git checkout -b feature/PROJ-123-user-auth

# Push and set upstream
git push -u origin feature/PROJ-123-user-auth

# Delete after merge
git branch -d feature/PROJ-123-user-auth
git push origin --delete feature/PROJ-123-user-auth
```

## PR Description Template

```markdown
## Summary
[1-3 sentences describing what this PR does and why]

## Changes
- [Change 1]
- [Change 2]
- [Change 3]

## Type of Change
- [ ] New feature
- [ ] Bug fix
- [ ] Refactor
- [ ] Documentation
- [ ] CI/CD
- [ ] Dependencies

## Testing
- [ ] Unit tests added/updated
- [ ] Integration tests pass
- [ ] Manual testing completed

## Screenshots
[If UI changes, add before/after screenshots]

## Related Issues
Closes #[issue_number]

## Checklist
- [ ] Code follows project conventions
- [ ] Self-reviewed the diff
- [ ] No secrets or credentials committed
- [ ] Documentation updated if needed
```

### Creating PRs with `gh`

```bash
# Create PR with template
gh pr create \
  --title "feat(auth): add OAuth2 login support" \
  --body "$(cat <<'EOF'
## Summary
Add OAuth2 login support with Google and GitHub providers.

## Changes
- Add OAuth2 router with callback endpoints
- Integrate python-social-auth
- Add provider configuration via environment variables

## Testing
- [x] Unit tests for token exchange
- [x] Integration tests with mock OAuth provider
- [ ] Manual testing with real providers

Closes #123
EOF
)"
```

## Interactive Rebase Guide

### When to Rebase

- Clean up commits before merging to main
- Squash WIP commits into logical units
- Reorder commits for clarity
- Fix commit messages

### Commands

```bash
# Rebase last N commits
git rebase -i HEAD~N

# Rebase onto main
git rebase -i main
```

### Rebase Actions

| Action | Short | Effect |
|--------|-------|--------|
| `pick` | `p` | Keep commit as-is |
| `reword` | `r` | Keep commit, edit message |
| `edit` | `e` | Pause to amend commit |
| `squash` | `s` | Merge into previous commit, combine messages |
| `fixup` | `f` | Merge into previous commit, discard message |
| `drop` | `d` | Remove commit entirely |

### Common Rebase Scenarios

**Squash WIP commits:**
```
pick abc1234 feat(auth): add login endpoint
squash def5678 wip: add validation
squash ghi9012 fix: typo in error message
```
Result: One clean commit with combined changes.

**Fix a commit message:**
```
pick abc1234 feat(auth): add login endpoint
reword def5678 fix typo   →   fix(auth): correct error message format
pick ghi9012 test(auth): add login tests
```

### Handling Rebase Conflicts

```bash
# During rebase, if conflict occurs:
# 1. Fix conflicts in files
# 2. Stage resolved files
git add <resolved-files>

# 3. Continue rebase
git rebase --continue

# Or abort if needed
git rebase --abort
```

## Release Tagging

### Semantic Versioning

```
MAJOR.MINOR.PATCH

MAJOR: Breaking changes
MINOR: New features (backwards compatible)
PATCH: Bug fixes (backwards compatible)
```

### Tagging Commands

```bash
# Create annotated tag
git tag -a v1.2.0 -m "Release v1.2.0: Add OAuth2 support"

# Push tag
git push origin v1.2.0

# Push all tags
git push origin --tags

# List tags
git tag -l "v1.*"
```

### Changelog Generation

```bash
# Generate changelog from conventional commits
# Between two tags:
git log v1.1.0..v1.2.0 --pretty=format:"- %s (%h)" --no-merges
```

**Changelog format:**

```markdown
# Changelog

## [1.2.0] - 2025-03-15

### Added
- OAuth2 login with Google and GitHub (#123)
- Rate limiting on API endpoints (#125)

### Fixed
- Null pointer in user profile endpoint (#130)
- Token refresh race condition (#132)

### Changed
- Upgrade FastAPI to 0.110 (#128)
```

## Git Hooks (Pre-commit)

### `.pre-commit-config.yaml`

```yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-json
      - id: check-added-large-files
        args: ['--maxkb=1000']
      - id: detect-private-key

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.3.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format

  - repo: https://github.com/compilerla/conventional-pre-commit
    rev: v3.1.0
    hooks:
      - id: conventional-pre-commit
        stages: [commit-msg]
```

```bash
# Install hooks
pre-commit install
pre-commit install --hook-type commit-msg
```

## Quick Reference

```bash
# Feature workflow
git checkout -b feature/PROJ-123-description
# ... make changes ...
git add -p                          # Stage interactively
git commit -m "feat(scope): description"
git push -u origin feature/PROJ-123-description
gh pr create --title "feat(scope): description"

# Hotfix workflow
git checkout -b hotfix/PROJ-456-critical-fix main
# ... fix ...
git commit -m "fix(scope): critical fix description"
git push -u origin hotfix/PROJ-456-critical-fix
gh pr create --title "fix(scope): critical fix" --label "hotfix"
```
