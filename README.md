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

### Engineering
| Skill | Description |
|-------|-------------|
| `code-review` | Comprehensive code reviews following company standards |
| `fastapi-scaffold` | Scaffold FastAPI projects with async SQLAlchemy, JWT auth, Docker |
| `ai-agent-debugger` | Debug and optimize multi-agent LLM workflows (CrewAI, LangChain) |
| `rag-pipeline` | Build and optimize RAG pipelines with chunking, embeddings, reranking |
| `prompt-engineering` | Systematic prompt optimization with templates and A/B testing |
| `python-test-generator` | Generate pytest suites with async support and LLM API mocking |
| `git-workflow` | Conventional commits, branch naming, PR templates, release tagging |

### Operations
| Skill | Description |
|-------|-------------|
| `incident-response` | Incident workflow with runbooks and escalation |
| `docker-deploy` | Multi-stage Docker builds, docker-compose, K8s manifests |

### Integrations
| Skill | Description |
|-------|-------------|
| `confluence-docs` | Search, create, and update Confluence pages |

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
"Scaffold a new FastAPI project for the payment service"
"Debug why my CrewAI agents are stuck in a loop"
"Build a RAG pipeline for our documentation"
"Help me write a better prompt for classification"
"Generate tests for the user authentication module"
"Create a Dockerfile for this Python app"
"Write a commit message for these changes"
"Search Confluence for authentication docs"
"Review this PR for security issues"
"Help me respond to this production incident"
```

Or invoke explicitly:

```
/fastapi-scaffold create new project
/ai-agent-debugger trace agent tool calls
/rag-pipeline optimize retrieval quality
/prompt-engineering improve this system prompt
/python-test-generator generate tests for app/services/
/docker-deploy create k8s manifests
/git-workflow write commit message
/confluence-docs search for API documentation
/code-review analyze the changes in this PR
/incident-response start incident workflow
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding new skills.

## Support

- GitHub Issues: https://github.com/georgey/claude-skills/issues
