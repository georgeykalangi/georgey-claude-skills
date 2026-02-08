# Georgey's Claude Skills

A curated collection of Claude Skills for productivity, integrations, and workflows.

## Quick Start

### Installation

```bash
# Add the marketplace
claude --plugin marketplace add georgey/claude-skills

# Install all skills
claude --plugin install georgey-claude-skills

# Or install specific skills
claude --plugin install confluence-docs@georgey-claude-skills
claude --plugin install code-review@georgey-claude-skills
```

### Manual Installation

```bash
# Clone the repository
git clone https://github.com/georgey/claude-skills.git

# Copy skills to Claude Code config
cp -r georgey-claude-skills/skills/* ~/.config/claude-code/skills/
```

## Available Skills

### Integrations
| Skill | Description |
|-------|-------------|
| `confluence-docs` | Search, create, and update Confluence pages |

### Engineering
| Skill | Description |
|-------|-------------|
| `code-review` | Comprehensive code reviews following company standards |

### Operations
| Skill | Description |
|-------|-------------|
| `incident-response` | Incident workflow with runbooks and escalation |

### Documentation
| Skill | Description |
|-------|-------------|
| `technical-spec` | Create technical specifications from company template |

### Business
| Skill | Description |
|-------|-------------|
| `internal-comms` | Status updates, announcements, newsletters |

## Using Skills

Skills activate automatically based on context:

```
"Search Confluence for authentication docs"
"Review this PR for security issues"
"Help me respond to this production incident"
"Create a technical spec for the new payment service"
"Write a team status update for this week"
```

Or invoke explicitly:

```
/confluence-docs search for API documentation
/code-review analyze the changes in this PR
/incident-response start incident workflow
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding new skills.

## Support

- GitHub Issues: https://github.com/georgey/claude-skills/issues
