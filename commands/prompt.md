---
description: Generate effective, well-structured prompts using advanced prompt engineering techniques
args:
  - name: task
    description: "The task or goal for which you need a prompt"
    required: true
  - name: audience
    description: "Target audience or model (e.g., 'Claude Sonnet', 'developer', 'non-technical user')"
    required: false
  - name: style
    description: "Desired output style (e.g., 'technical', 'conversational', 'concise', 'detailed')"
    required: false
  - name: format
    description: "Expected output format (e.g., 'code', 'markdown', 'json', 'step-by-step')"
    required: false
---

# Prompt Engineering Workflow

You are an expert prompt engineer. Your task is to create a highly effective, well-structured prompt based on the provided parameters.

## Input Parameters

- **Task**: {task}
- **Audience**: {audience || "general AI assistant"}
- **Style**: {style || "professional and clear"}
- **Format**: {format || "flexible"}

## Prompt Engineering Framework

Follow these steps to create an optimal prompt:

### 1. Context Analysis

First, analyze the task requirements:
- What is the core objective?
- What domain knowledge is required?
- What are potential edge cases or ambiguities?
- What constraints or requirements exist?

### 2. Prompt Structure Design

Build the prompt using this proven structure:

**A. Role Assignment** (if beneficial)
- Assign relevant expertise/persona to focus the AI's responses
- Example: "You are an expert software architect..."

**B. Clear Objective**
- State the primary goal explicitly and unambiguously
- Use action verbs: analyze, create, explain, refactor, design, etc.

**C. Context Provision**
- Provide necessary background information
- Define key terms and constraints
- Specify the environment or domain

**D. Requirements & Constraints**
- List specific requirements (format, length, technical level)
- Define boundaries (what to avoid, what must be included)
- Specify any quality criteria

**E. Examples** (when helpful)
- Include input/output examples for complex tasks
- Show desired format and style through examples
- Use XML tags or clear delimiters for multi-part examples

**F. Output Format Specification**
- Define the expected structure explicitly
- Use templates or schemas when applicable
- Specify any required sections or elements

**G. Thinking Process** (for complex tasks)
- Request step-by-step reasoning when needed
- Ask for analysis before conclusions
- Include reflection or validation steps

### 3. Prompt Optimization Techniques

Apply these advanced techniques:

- **Specificity**: Replace vague terms with precise requirements
- **Decomposition**: Break complex tasks into clear sub-steps
- **Chain-of-Thought**: For reasoning tasks, explicitly request thinking steps
- **Few-Shot Learning**: Provide 2-3 examples for pattern recognition
- **Constraints**: Use positive constraints (do X) over negative (don't do Y)
- **Validation**: Include self-checking or quality verification steps
- **XML Tags**: Use `<context>`, `<requirements>`, `<examples>` for structure
- **Iterative Refinement**: Build in feedback loops for multi-step tasks

### 4. Quality Checklist

Before finalizing, verify:
- [ ] Objective is clear and unambiguous
- [ ] Context is sufficient but not excessive
- [ ] Requirements are specific and measurable
- [ ] Examples are provided where helpful
- [ ] Output format is well-defined
- [ ] Prompt is concise (no unnecessary verbosity)
- [ ] Language is precise and professional
- [ ] Edge cases are addressed
- [ ] Success criteria are implicit or explicit

## Output

Generate the optimized prompt following this template:

```markdown
# [Prompt Title]

## Role & Context
[Assign role if beneficial, provide essential context]

## Objective
[Clear, specific goal statement]

## Requirements
[Bulleted list of specific requirements]

## Constraints
[Any limitations, boundaries, or things to avoid]

## Input Format
[If applicable, describe expected input structure]

## Output Format
[Detailed specification of expected output]

## Examples
[If applicable, provide 1-3 examples with clear input/output]

## Thinking Process
[If applicable, request step-by-step reasoning]

## Quality Criteria
[How to evaluate success]

---

## Prompt Text (Final Version)

[The complete, optimized prompt ready to use]
```

## Additional Analysis

After generating the prompt, provide:

1. **Rationale**: Explain key design decisions
2. **Strengths**: What makes this prompt effective
3. **Potential Improvements**: Optional enhancements for specific use cases
4. **Usage Tips**: How to adapt or iterate on this prompt

## Advanced Patterns (when applicable)

Consider these patterns for specific scenarios:

- **Multi-Agent Pattern**: Split task across specialized agents
- **Validation Loop**: Include review and refinement steps
- **Progressive Disclosure**: Start simple, add complexity iteratively
- **Socratic Method**: Guide through questions rather than direct answers
- **Meta-Prompting**: Ask the AI to improve or analyze the prompt itself

---

**Begin by analyzing the task and then generate the optimized prompt.**
