---
name: confluence-docs
description: Search, read, create, and update Confluence pages. This skill should be used when working with company wiki, documentation, knowledge base content, or when users mention Confluence, wiki, or internal docs.
---

# Confluence Documentation Skill

## Overview

This skill enables interaction with Confluence for searching, reading, creating, and updating documentation. It integrates with the company's Confluence instance via MCP or API.

## When to Use This Skill

- Searching for internal documentation
- Reading wiki pages or knowledge base articles
- Creating new documentation pages
- Updating existing Confluence content
- Finding information across spaces

## Prerequisites

### MCP Configuration

Add to your Claude settings or `~/.claude.json`:

```json
{
  "mcpServers": {
    "confluence": {
      "command": "uvx",
      "args": ["mcp-atlassian"],
      "env": {
        "CONFLUENCE_URL": "https://company.atlassian.net/wiki",
        "CONFLUENCE_USERNAME": "${CONFLUENCE_USER}",
        "CONFLUENCE_API_TOKEN": "${CONFLUENCE_TOKEN}"
      }
    }
  }
}
```

### Environment Variables

Set these before using:
```bash
export CONFLUENCE_USER="your.email@company.com"
export CONFLUENCE_TOKEN="your-api-token"
```

## Available Operations

### 1. Search Confluence

**Triggers**: "search confluence", "find in wiki", "look up docs"

**Usage**:
```
Search Confluence for authentication documentation
Find pages about API rate limiting
Look up the deployment runbook
```

**CQL Search Syntax**:
- `text ~ "keyword"` - Full text search
- `space = "ENGINEERING"` - Search specific space
- `type = page` - Page type filter
- `creator = currentUser()` - Your pages
- `lastmodified >= now("-7d")` - Recent changes

### 2. Read Page Content

**Triggers**: "read confluence page", "get wiki content", "show me the doc"

**Usage**:
```
Read the onboarding guide from Confluence
Get the content of the API authentication page
Show me the incident response runbook
```

### 3. Create New Page

**Triggers**: "create confluence page", "add to wiki", "document this"

**Usage**:
```
Create a new Confluence page for the payment service architecture
Add a wiki page documenting this API endpoint
Create documentation for this new feature
```

**Best Practices**:
- Always specify the target space
- Use clear, descriptive titles
- Add appropriate labels for discoverability
- Include a summary at the top

### 4. Update Existing Page

**Triggers**: "update confluence", "edit wiki page", "modify documentation"

**Usage**:
```
Update the deployment guide with the new steps
Add a section to the troubleshooting page
Fix the outdated information in the API docs
```

## Common Spaces

| Space Key | Name | Purpose |
|-----------|------|---------|
| `ENG` | Engineering | Technical docs, architecture |
| `OPS` | Operations | Runbooks, procedures |
| `PRODUCT` | Product | Specs, roadmaps |
| `ONBOARD` | Onboarding | New hire guides |
| `API` | API Docs | API documentation |

## Workflow Examples

### Example 1: Research and Summarize

**User**: "Find all documentation about our authentication system and summarize it"

**Workflow**:
1. Search: `text ~ "authentication" AND space in (ENG, API)`
2. Read top relevant pages
3. Synthesize into summary
4. Cite sources with page links

### Example 2: Create Technical Doc

**User**: "Document the new caching layer I just implemented"

**Workflow**:
1. Gather information about the implementation
2. Create page in ENG space
3. Structure with Overview, Architecture, Usage, Configuration
4. Add labels: `caching`, `infrastructure`, `technical`
5. Return page URL

### Example 3: Update Runbook

**User**: "Add the new rollback procedure to the deployment runbook"

**Workflow**:
1. Search for deployment runbook
2. Read current content
3. Add new section maintaining existing format
4. Update page with version note
5. Confirm changes

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| 401 Unauthorized | Invalid/expired token | Regenerate API token |
| 403 Forbidden | No space permissions | Request access from space admin |
| 404 Not Found | Page doesn't exist | Verify page ID or search again |
| Rate Limited | Too many requests | Wait and retry |

## Tips

- Use CQL for precise searches
- Check page labels for related content
- Link to existing pages rather than duplicating
- Follow space-specific templates when creating
- Add meaningful labels for discoverability

## References

- Load `references/cql_syntax.md` for advanced search patterns
- Load `references/page_templates.md` for standard formats
