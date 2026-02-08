---
name: ai-agent-debugger
description: Debug and optimize multi-agent LLM workflows built with CrewAI, LangChain, and similar frameworks. This skill should be used when agents are looping, hallucinating, producing wrong tool calls, or when optimizing token usage and costs.
---

# AI Agent Debugger Skill

## Overview

This skill helps debug and optimize multi-agent LLM workflows. It covers tracing agent tool calls, analyzing token usage, fixing hallucination and looping issues, debugging RAG retrieval quality, and troubleshooting multi-LLM routing.

## When to Use This Skill

- Agent stuck in infinite loops
- Tool calls returning errors or wrong results
- High token usage / unexpected API costs
- Agent hallucinating or ignoring instructions
- RAG retrieval returning irrelevant context
- Multi-agent orchestration failures
- CrewAI or LangChain pipeline debugging

## Debugging Framework

### Step 1: Identify the Failure Mode

| Symptom | Likely Cause | Section |
|---------|-------------|---------|
| Agent loops forever | Bad stop condition or circular tool calls | Looping Issues |
| Wrong tool selected | Ambiguous tool descriptions | Tool Call Debugging |
| Hallucinated output | Missing context or weak system prompt | Hallucination Fixes |
| High token costs | Verbose prompts, unnecessary retries | Token Optimization |
| Bad RAG results | Poor chunking or embedding mismatch | RAG Debugging |
| Agent ignores instructions | System prompt too long or conflicting | Prompt Issues |

### Step 2: Enable Tracing

#### LangChain / LangSmith

```python
import os
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-key"
os.environ["LANGCHAIN_PROJECT"] = "debug-session"

# Or use callback handler
from langchain_core.tracers import ConsoleCallbackHandler
chain.invoke(input, config={"callbacks": [ConsoleCallbackHandler()]})
```

#### CrewAI

```python
import litellm
litellm.set_verbose = True

# Enable crew verbose mode
crew = Crew(
    agents=[...],
    tasks=[...],
    verbose=True,
)
```

#### Custom Logging

```python
import logging
import json
from datetime import datetime

class AgentTracer:
    def __init__(self):
        self.traces = []

    def log_call(self, agent: str, action: str, input_data: dict, output_data: dict, tokens: int):
        self.traces.append({
            "timestamp": datetime.utcnow().isoformat(),
            "agent": agent,
            "action": action,
            "input": input_data,
            "output": output_data,
            "tokens": tokens,
        })

    def dump(self):
        return json.dumps(self.traces, indent=2)
```

## Debugging Patterns

### Looping Issues

**Diagnosis checklist:**
- [ ] Check if agent has a clear stop/exit condition
- [ ] Verify tool output is being parsed correctly
- [ ] Check for circular dependencies between agents
- [ ] Ensure max_iterations is set

**Common fixes:**

```python
# CrewAI - Set max iterations
agent = Agent(
    role="researcher",
    goal="...",
    max_iter=5,  # Prevent infinite loops
    max_rpm=10,  # Rate limit
)

# LangChain - Set recursion limit
chain.invoke(input, config={"recursion_limit": 10})
```

**Anti-pattern: Agent A calls Agent B which calls Agent A**
```
Fix: Add explicit task boundaries and output validators
between agents. Use a supervisor pattern instead of
peer-to-peer communication.
```

### Tool Call Debugging

**Diagnosis checklist:**
- [ ] Are tool descriptions clear and unambiguous?
- [ ] Does the tool schema match what the LLM expects?
- [ ] Is the tool returning structured output the agent can parse?
- [ ] Are there overlapping tools confusing the agent?

**Fix ambiguous tools:**

```python
# BAD - overlapping descriptions
search_tool = Tool(name="search", description="Search for information")
lookup_tool = Tool(name="lookup", description="Look up information")

# GOOD - specific descriptions
web_search_tool = Tool(
    name="web_search",
    description="Search the internet for current information. Use when you need real-time data, news, or public web content. Input: search query string."
)
db_lookup_tool = Tool(
    name="database_lookup",
    description="Query the internal PostgreSQL database for user or order data. Use when you need data from our system. Input: SQL-like filter expression."
)
```

### Hallucination Fixes

**Diagnosis checklist:**
- [ ] Is the context window being exceeded (truncated context)?
- [ ] Is the system prompt grounding the agent to available data?
- [ ] Are retrieved documents actually relevant?
- [ ] Is temperature too high for factual tasks?

**Grounding strategies:**

```python
# Add explicit grounding instructions
system_prompt = """You are a research assistant.

IMPORTANT RULES:
- ONLY use information from the provided context
- If the context doesn't contain the answer, say "I don't have enough information"
- NEVER make up facts, statistics, or citations
- Quote the source when providing information

Context:
{context}
"""

# Lower temperature for factual tasks
llm = ChatOpenAI(model="gpt-4o", temperature=0.0)

# Add output validation
from pydantic import BaseModel, Field

class FactualAnswer(BaseModel):
    answer: str = Field(description="Answer based only on provided context")
    sources: list[str] = Field(description="Exact quotes from context supporting the answer")
    confidence: float = Field(ge=0, le=1, description="Confidence score")
```

### Token Usage Optimization

**Analysis approach:**

```python
# Track token usage per agent/step
from langchain_community.callbacks import get_openai_callback

with get_openai_callback() as cb:
    result = chain.invoke(input)
    print(f"Total tokens: {cb.total_tokens}")
    print(f"Prompt tokens: {cb.prompt_tokens}")
    print(f"Completion tokens: {cb.completion_tokens}")
    print(f"Total cost: ${cb.total_cost:.4f}")
```

**Optimization strategies:**

| Strategy | Impact | Effort |
|----------|--------|--------|
| Shorten system prompts | 10-30% reduction | Low |
| Use smaller model for simple steps | 50-70% cost reduction | Medium |
| Cache repeated tool calls | 20-40% reduction | Low |
| Reduce context window stuffing | 15-25% reduction | Medium |
| Batch similar operations | 30-50% reduction | Medium |

```python
# Multi-model routing - use cheap model for simple tasks
from litellm import completion

def route_to_model(task_complexity: str, prompt: str):
    if task_complexity == "simple":
        return completion(model="claude-haiku-4-5-20251001", messages=[...])
    elif task_complexity == "medium":
        return completion(model="claude-sonnet-4-5-20250929", messages=[...])
    else:
        return completion(model="claude-opus-4-6", messages=[...])
```

### RAG Retrieval Debugging

**Diagnosis checklist:**
- [ ] Are chunks too large or too small?
- [ ] Is the embedding model appropriate for the content?
- [ ] Are queries being reformulated before retrieval?
- [ ] Is similarity threshold too strict or too loose?
- [ ] Are metadata filters working correctly?

**Debug retrieval quality:**

```python
# Inspect what's actually being retrieved
results = vectorstore.similarity_search_with_score(query, k=10)
for doc, score in results:
    print(f"Score: {score:.4f}")
    print(f"Source: {doc.metadata.get('source', 'unknown')}")
    print(f"Content: {doc.page_content[:200]}...")
    print("---")
```

## Multi-LLM Routing Troubleshooting

**Common issues:**
- API key misconfiguration across providers
- Different message formats (system prompt handling)
- Inconsistent tool calling formats
- Rate limiting across providers

**Debug checklist:**
- [ ] Verify API keys are set for each provider
- [ ] Check model name strings match provider format
- [ ] Ensure tool schemas are compatible across models
- [ ] Test fallback chain independently

## Quick Reference: Error Messages

| Error | Provider | Fix |
|-------|----------|-----|
| `context_length_exceeded` | OpenAI | Reduce prompt or use larger context model |
| `rate_limit_error` | Any | Add exponential backoff / reduce concurrency |
| `invalid_tool_call` | Any | Check tool schema matches model expectations |
| `max_tokens_exceeded` | Anthropic | Set explicit `max_tokens` parameter |
| `overloaded_error` | Anthropic | Retry with backoff |

## Debugging Workflow Summary

1. **Reproduce** - Get a minimal failing example
2. **Trace** - Enable verbose logging / LangSmith
3. **Isolate** - Test each agent/tool independently
4. **Identify** - Match symptom to debugging pattern above
5. **Fix** - Apply targeted fix
6. **Validate** - Run the full pipeline again
7. **Monitor** - Add assertions/guardrails to prevent regression
