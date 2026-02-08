---
name: code-review
description: Perform comprehensive code reviews following company standards. This skill should be used when reviewing pull requests, checking code quality, security issues, or ensuring engineering best practices are followed.
---

# Code Review Skill

## Overview

This skill provides structured code review following company engineering standards, covering security, performance, maintainability, and best practices.

## When to Use This Skill

- Reviewing pull requests
- Checking code quality before merge
- Security vulnerability assessment
- Performance review
- Best practices verification

## Review Framework

### 1. Security Review

Check for:
- [ ] Input validation and sanitization
- [ ] SQL injection vulnerabilities
- [ ] XSS vulnerabilities
- [ ] Authentication/authorization issues
- [ ] Hardcoded secrets or credentials
- [ ] Insecure dependencies
- [ ] Proper error handling (no stack traces exposed)

### 2. Performance Review

Check for:
- [ ] N+1 query problems
- [ ] Missing database indexes
- [ ] Unnecessary loops or iterations
- [ ] Memory leaks
- [ ] Blocking operations in async code
- [ ] Missing caching opportunities
- [ ] Large payload sizes

### 3. Code Quality Review

Check for:
- [ ] Clear, descriptive naming
- [ ] Appropriate function/method length
- [ ] Single responsibility principle
- [ ] DRY (Don't Repeat Yourself)
- [ ] Proper error handling
- [ ] Adequate logging
- [ ] Code comments where necessary

### 4. Testing Review

Check for:
- [ ] Unit tests for new functionality
- [ ] Edge cases covered
- [ ] Integration tests where appropriate
- [ ] Test naming clarity
- [ ] Mocking done correctly

### 5. Documentation Review

Check for:
- [ ] Updated README if needed
- [ ] API documentation
- [ ] Inline comments for complex logic
- [ ] Changelog entry

## Review Process

### Step 1: Understand Context

1. Read PR description and linked issues
2. Understand the purpose of changes
3. Identify scope and impact

### Step 2: High-Level Review

1. Review file changes overview
2. Check architecture/design decisions
3. Identify major concerns

### Step 3: Detailed Review

1. Review each file systematically
2. Check against review framework
3. Note specific issues with line numbers

### Step 4: Provide Feedback

Structure feedback as:

```markdown
## Summary
[Overall assessment]

## Critical Issues
- [ ] **[File:Line]** [Issue description]

## Suggestions
- [ ] **[File:Line]** [Improvement suggestion]

## Questions
- [Clarification needed]

## Positive Feedback
- [What was done well]
```

## Severity Levels

| Level | Description | Action |
|-------|-------------|--------|
| **Critical** | Security vulnerability, data loss risk | Must fix before merge |
| **Major** | Bug, significant issue | Should fix before merge |
| **Minor** | Code quality, style | Consider fixing |
| **Nitpick** | Personal preference | Optional |

## Language-Specific Guidelines

### Python
- Follow PEP 8
- Use type hints
- Prefer list comprehensions
- Use context managers

### TypeScript/JavaScript
- Use TypeScript strict mode
- Avoid `any` types
- Prefer `const` over `let`
- Use async/await over callbacks

### Go
- Follow effective Go guidelines
- Handle all errors
- Use meaningful variable names
- Prefer composition

## Example Review Output

```markdown
## Summary
This PR adds user authentication endpoints. Overall well-structured with good test coverage. A few security concerns need addressing.

## Critical Issues
- [ ] **auth/handler.go:45** SQL injection vulnerability - use parameterized queries
- [ ] **auth/handler.go:78** Password stored in plain text - must hash with bcrypt

## Major Issues
- [ ] **auth/service.go:23** Missing rate limiting on login endpoint

## Suggestions
- [ ] **auth/handler.go:12** Consider extracting validation to middleware
- [ ] **auth/service.go:56** Add logging for failed auth attempts

## Positive Feedback
- Excellent test coverage
- Clear separation of concerns
- Good error messages
```

## Integration with GitHub

To review a specific PR:

```bash
# Fetch PR details
gh pr view <number>

# Get diff
gh pr diff <number>

# Add review
gh pr review <number> --comment --body "..."
```

## References

- Load `references/security_checklist.md` for detailed security review
- Load `references/language_standards.md` for language-specific rules
