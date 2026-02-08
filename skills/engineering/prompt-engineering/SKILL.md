---
name: prompt-engineering
description: Systematic prompt optimization framework with templates, patterns, A/B testing methodology, and provider-specific tips for Claude, OpenAI, and Gemini. This skill should be used when writing, improving, or debugging LLM prompts.
---

# Prompt Engineering Skill

## Overview

This skill provides a systematic framework for writing, optimizing, and testing prompts across LLM providers. It includes reusable templates, proven patterns, A/B testing methodology, and provider-specific guidance.

## When to Use This Skill

- Writing new system prompts or task prompts
- Improving prompt quality or reliability
- Debugging inconsistent LLM outputs
- Optimizing prompts for cost or latency
- Adapting prompts across providers (Claude, OpenAI, Gemini)
- Setting up prompt evaluation pipelines

## Core Patterns

### 1. Role + Context + Task + Format

The fundamental prompt structure:

```
You are a {role} with expertise in {domain}.

Context:
{relevant background information}

Task:
{specific instruction}

Output Format:
{expected structure}
```

### 2. Chain-of-Thought (CoT)

Force step-by-step reasoning for complex tasks:

```
Analyze the following code for security vulnerabilities.

Think through this step by step:
1. First, identify all user inputs
2. Then, trace how each input flows through the code
3. Check if any input reaches a sensitive operation without sanitization
4. For each vulnerability found, classify its severity

Code:
{code}
```

### 3. Few-Shot Examples

Provide examples to guide output format and quality:

```
Classify the following support tickets by priority.

Examples:
- "Site is completely down" → P0 (Critical)
- "Search results are slow" → P2 (Medium)
- "Typo in footer" → P3 (Low)

Now classify:
- "{ticket_text}" →
```

### 4. Structured Output

Force reliable structured responses:

```
Extract the following information from the text. Respond ONLY with valid JSON matching this schema:

{
  "name": "string",
  "email": "string or null",
  "company": "string or null",
  "intent": "buy | sell | inquire | other"
}

Text: {input_text}
```

### 5. Self-Verification

Have the model check its own work:

```
{main task instruction}

After generating your response:
1. Verify each claim against the provided context
2. Check for logical consistency
3. Ensure all required fields are present
4. If you find any errors, correct them before responding
```

## Task-Specific Templates

### Code Generation

```
Write a {language} function that {description}.

Requirements:
- {requirement 1}
- {requirement 2}

Constraints:
- {constraint}

Include:
- Type hints
- Docstring with examples
- Error handling for edge cases

Do not include tests or example usage unless asked.
```

### Data Extraction

```
Extract structured data from the following {document_type}.

Fields to extract:
{field_list with descriptions}

Rules:
- If a field is not found, set it to null
- Dates should be in ISO 8601 format
- Numbers should be numeric types, not strings
- Return valid JSON only

Document:
{document}
```

### Summarization

```
Summarize the following {content_type} in {length} sentences.

Focus on:
- Key decisions or outcomes
- Action items
- Unresolved questions

Audience: {audience description}
Tone: {formal/casual/technical}

Content:
{content}
```

### Classification

```
Classify the following {item_type} into one of these categories: {categories}.

For each classification, provide:
1. Category (must be one of the listed categories)
2. Confidence (high/medium/low)
3. Brief reasoning (1 sentence)

{item}
```

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| "Be creative" | Vague, inconsistent output | Specify exact format and constraints |
| Mega-prompt (2000+ words) | Instruction following degrades | Split into focused sub-prompts |
| "Do NOT do X" | Negation is unreliable | State what TO do instead |
| Implicit context | Model guesses wrong | Provide explicit context and examples |
| No output format | Inconsistent structure | Always specify expected format |
| Mixing multiple tasks | Partial completion | One prompt per task, chain them |

## A/B Testing Methodology

### 1. Define Metrics

```python
evaluation_criteria = {
    "correctness": "Does the output match ground truth?",
    "completeness": "Are all required elements present?",
    "format_compliance": "Does output match expected format?",
    "relevance": "Is the response relevant to the query?",
}
```

### 2. Create Test Dataset

- Minimum 50 diverse test cases
- Include edge cases and adversarial inputs
- Have human-labeled ground truth where possible

### 3. Run Evaluation

```python
import json
from anthropic import Anthropic

client = Anthropic()

def evaluate_prompt(prompt_template: str, test_cases: list[dict]) -> list[dict]:
    results = []
    for case in test_cases:
        prompt = prompt_template.format(**case["inputs"])
        response = client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}],
        )
        results.append({
            "input": case["inputs"],
            "output": response.content[0].text,
            "expected": case.get("expected"),
        })
    return results

# Compare two prompts
results_a = evaluate_prompt(prompt_v1, test_cases)
results_b = evaluate_prompt(prompt_v2, test_cases)
```

### 4. Score and Compare

```python
def score_results(results: list[dict], criteria: dict) -> dict:
    """Use LLM-as-judge to score outputs."""
    scores = {k: [] for k in criteria}
    for result in results:
        judge_prompt = f"""Score this output on a scale of 1-5 for each criterion.
Output: {result['output']}
Expected: {result['expected']}

Criteria:
{json.dumps(criteria, indent=2)}

Respond with JSON: {{"criterion": score, ...}}"""
        # Score with a strong model
        ...
    return {k: sum(v)/len(v) for k, v in scores.items()}
```

## Provider-Specific Tips

### Claude (Anthropic)

- **System prompt**: Use for role and persistent instructions; Claude follows system prompts closely
- **XML tags**: Claude responds well to `<context>`, `<instructions>`, `<examples>` tags for structure
- **Thinking**: Use extended thinking for complex reasoning tasks
- **Be direct**: Claude prefers clear, direct instructions over elaborate framing
- **Prefill**: Start the assistant response to guide format:
  ```python
  messages=[
      {"role": "user", "content": "Extract entities..."},
      {"role": "assistant", "content": "{"},  # Forces JSON output
  ]
  ```

### OpenAI (GPT-4o)

- **System prompt**: Use for persona and rules; keep concise
- **JSON mode**: Use `response_format={"type": "json_object"}` for reliable JSON
- **Function calling**: Prefer structured outputs via tool definitions over free-form JSON
- **Temperature**: Use 0 for deterministic tasks, 0.7-1.0 for creative tasks
- **Seed parameter**: Set for reproducible outputs in testing

### Google (Gemini)

- **Safety settings**: Configure safety filters to avoid false blocks on technical content
- **Grounding**: Use Google Search grounding for factual queries
- **Multi-modal**: Gemini excels at image + text prompts
- **System instruction**: Use the dedicated system instruction field
- **Structured output**: Use `response_mime_type="application/json"` with `response_schema`

## Prompt Optimization Workflow

1. **Draft** - Write initial prompt using a template above
2. **Test** - Run against 5-10 representative inputs
3. **Identify failures** - Categorize what goes wrong
4. **Iterate** - Apply targeted fixes (add examples, clarify instructions, add constraints)
5. **Evaluate** - Run full A/B test against previous version
6. **Document** - Record the winning prompt with version and rationale
