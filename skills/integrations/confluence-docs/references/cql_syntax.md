# Confluence Query Language (CQL) Reference

## Basic Syntax

```
field operator value
```

## Common Fields

| Field | Description | Example |
|-------|-------------|---------|
| `text` | Full-text search | `text ~ "authentication"` |
| `title` | Page title | `title ~ "API Guide"` |
| `space` | Space key | `space = "ENG"` |
| `type` | Content type | `type = page` |
| `label` | Page labels | `label = "runbook"` |
| `creator` | Page author | `creator = "john.doe"` |
| `lastmodified` | Last update | `lastmodified >= now("-7d")` |
| `created` | Creation date | `created >= "2024-01-01"` |

## Operators

| Operator | Description | Example |
|----------|-------------|---------|
| `=` | Exact match | `space = "ENG"` |
| `!=` | Not equal | `type != blogpost` |
| `~` | Contains | `text ~ "deploy"` |
| `!~` | Not contains | `title !~ "draft"` |
| `>`, `>=`, `<`, `<=` | Comparison | `created >= "2024-01-01"` |
| `in` | Multiple values | `space in ("ENG", "OPS")` |
| `not in` | Exclude values | `label not in ("archived")` |

## Logical Operators

```
# AND - both conditions
text ~ "api" AND space = "ENG"

# OR - either condition
label = "runbook" OR label = "procedure"

# NOT - exclude
type = page AND NOT label = "archived"

# Parentheses for grouping
(space = "ENG" OR space = "OPS") AND text ~ "deploy"
```

## Date Functions

```
# Relative dates
lastmodified >= now("-7d")     # Last 7 days
created >= now("-1M")          # Last month
lastmodified >= startOfDay()   # Today
lastmodified >= startOfWeek()  # This week

# Absolute dates
created >= "2024-01-01"
lastmodified <= "2024-12-31"
```

## User Functions

```
creator = currentUser()           # Your pages
contributor = currentUser()       # Pages you edited
watcher = currentUser()          # Pages you watch
mention = currentUser()          # Pages mentioning you
```

## Common Queries

```
# Recent engineering docs
space = "ENG" AND lastmodified >= now("-7d") ORDER BY lastmodified DESC

# All runbooks
label = "runbook" AND type = page

# Your draft pages
creator = currentUser() AND label = "draft"

# API documentation
space = "API" AND type = page AND NOT label = "archived"

# Search across multiple spaces
text ~ "authentication" AND space in ("ENG", "API", "SECURITY")
```

## Sorting

```
ORDER BY title ASC
ORDER BY lastmodified DESC
ORDER BY created DESC
```

## Pagination

Results are paginated. Use `start` and `limit` parameters:
- `limit`: Number of results (max 100)
- `start`: Starting index (0-based)
