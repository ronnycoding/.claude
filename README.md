# Claude Code Configuration

Personal Claude Code configuration directory featuring 83+ specialized AI agents, GitHub workflow automation, and multi-agent orchestration patterns.

## Overview

This repository extends Claude Code with:
- **83+ Specialized AI Agents** across Haiku/Sonnet/Opus model tiers
- **GitHub Workflow Automation** for issues, PRs, and task management
- **Multi-Agent Orchestration** patterns for complex development workflows
- **Session Persistence** across projects and shell environments

## Features

### 🤖 Specialized AI Agents

Collection of 83+ domain-specific subagents optimized for different Claude models:

#### Model Distribution
| Model  | Count | Use Case                                                 |
|--------|-------|----------------------------------------------------------|
| Haiku  | 11    | Fast, focused tasks (context management, SEO)            |
| Sonnet | 46    | Standard development (languages, frontend, infrastructure)|
| Opus   | 22    | Complex reasoning (architecture, security, analysis)     |

#### Key Agent Categories

**Architecture & Design**
- `backend-architect`, `cloud-architect`, `kubernetes-architect`
- `hybrid-cloud-architect`, `graphql-architect`, `terraform-specialist`

**Programming Languages** (18 agents)
- Systems: `c-pro`, `cpp-pro`, `rust-pro`, `golang-pro`
- Web: `javascript-pro`, `typescript-pro`, `python-pro`, `ruby-pro`, `php-pro`
- Enterprise: `java-pro`, `scala-pro`, `csharp-pro`
- Mobile: `ios-developer`, `flutter-expert`, `mobile-developer`

**Infrastructure & Operations**
- `devops-troubleshooter`, `deployment-engineer`, `incident-responder`
- `database-optimizer`, `database-admin`, `network-engineer`
- `performance-engineer`, `observability-engineer`

**Security & Quality**
- `code-reviewer`, `security-auditor`, `tdd-orchestrator`
- `backend-security-coder`, `frontend-security-coder`, `mobile-security-coder`
- `test-automator`, `debugger`, `error-detective`

**AI/ML & Data**
- `ai-engineer`, `ml-engineer`, `mlops-engineer`, `prompt-engineer`
- `data-scientist`, `data-engineer`

**Documentation & Business**
- `docs-architect`, `api-documenter`, `tutorial-engineer`, `mermaid-expert`
- `business-analyst`, `content-marketer`, `legal-advisor`, `hr-pro`

### 🔄 Multi-Agent Orchestration Patterns

#### Sequential Processing
Agents execute in sequence, passing context forward:
```
backend-architect → frontend-developer → test-automator → security-auditor
```

#### Parallel Execution
Multiple agents work simultaneously on different aspects:
```
performance-engineer + database-optimizer → Merged analysis
```

#### Validation Pipeline
Primary work followed by specialized review:
```
payment-integration → security-auditor → Validated implementation
```

#### Conditional Routing
Dynamic agent selection based on analysis:
```
debugger → [backend-architect | frontend-developer | devops-troubleshooter]
```

### 📋 Common Workflow Patterns

**Feature Development**
```
"Implement user authentication"
→ backend-architect → frontend-developer → test-automator → security-auditor
```

**Performance Optimization**
```
"Optimize checkout process"
→ performance-engineer → database-optimizer → frontend-developer → code-reviewer
```

**Production Incidents**
```
"Debug high memory usage"
→ incident-responder → devops-troubleshooter → error-detective → performance-engineer
```

**Infrastructure Setup**
```
"Set up disaster recovery"
→ cloud-architect → database-admin → terraform-specialist → observability-engineer
```

**ML Pipeline Development**
```
"Build ML pipeline with monitoring"
→ mlops-engineer → ml-engineer → data-engineer → performance-engineer → observability-engineer
```

**Security Hardening**
```
"Implement security best practices"
→ security-auditor → backend-security-coder → frontend-security-coder → code-reviewer
```

**API Development**
```
"Create RESTful API with documentation"
→ backend-architect → api-documenter → test-automator → security-auditor
```

### 🎯 GitHub Workflow Automation

#### Issue Creation (`commands/issue.md`)
Comprehensive multi-phase workflow:
1. **Repository Analysis**: Examines conventions, templates, contribution guidelines
2. **Best Practices Research**: Current standards for issue writing
3. **Issue Classification**: Determines type, priority, complexity
4. **Decomposition**: Breaks complex features into assignable sub-issues
5. **Dependency Mapping**: Creates dependency graphs and integration points
6. **Quality Assurance**: Validates completeness and alignment

**Features:**
- Automatic template detection from repository
- Sub-issue creation with team assignments
- Dependency graph generation (Mermaid diagrams)
- Integration point definition between components

#### Pull Request Creation (`commands/pr.md`)
Sophisticated PR generation workflow:
1. **Template Detection**: Finds existing PR templates (`.github/pull_request_template.md`)
2. **Convention Analysis**: Reviews 10-20 recent PRs for patterns
3. **Change Classification**: Categorizes type and impact level
4. **Risk Assessment**: Identifies breaking changes and compatibility issues
5. **Content Generation**: Creates comprehensive PR with context and evidence

**Features:**
- Auto-detects title format (conventional commits, GitHub, Jira)
- Analyzes merge strategy (squash/merge/rebase)
- Identifies required status checks and reviewers
- Generates testing evidence and migration notes

#### Todo Management (`commands/todos.md`)
Advanced task tracking with agent orchestration:

**Commands:**
```bash
# Initialize
claude todos --init --project="PROJECT_NAME" --repo="REPO_URL"

# Add orchestrated issue
claude todos --add --issue="123" --type="orchestration" --priority="high"

# Update progress
claude todos --update --issue="123" --phase="integration" --progress="75"

# Add subtask with agent assignment
claude todos --add-subtask --parent="123" --agent="backend-specialist" --task="Implement API"

# View status
claude todos --status [--tree]
```

**Features:**
- Multi-agent coordination tracking
- Phase-based progress (analysis, implementation, integration)
- Dependency management between subtasks
- Tree view visualization
- Status dashboard with completion metrics

## Directory Structure

```
.claude/
├── CLAUDE.md              # Repository guidance for Claude Code
├── README.md              # This file
├── settings.json          # Claude Code settings
├── .gitignore            # Git configuration
│
├── commands/             # GitHub operation templates
│   ├── issue.md         # Multi-phase issue creation workflow
│   ├── pr.md            # Comprehensive PR creation workflow
│   ├── task.md          # Task management workflow
│   └── todos.md         # Todo tracking with orchestration
│
├── agents/              # Specialized AI subagents (83+)
│   ├── README.md        # Agent documentation and usage guide
│   ├── [language]-pro.md    # Language-specific agents
│   ├── [domain]-[role].md   # Domain-specific specialists
│   └── examples/        # Usage examples and patterns
│
├── templates/           # GitHub templates
│   ├── GH_PR_TEMPLATE.md      # Standard PR template
│   └── GH_SUB_ISSUE_TEMPLATE.md # Sub-issue template
│
├── projects/            # Session histories (.jsonl)
├── shell-snapshots/     # Shell session persistence
├── todos/              # Task tracking files (.json)
├── statsig/            # Analytics cache
├── plugins/            # Claude Code plugins
└── ide/                # IDE integration
```

## Quick Start

### Installation

Clone to your Claude Code configuration directory:

```bash
cd ~/.claude
git clone git@github.com:ronnycoding/.claude.git .
```

The configuration loads automatically when using Claude Code.

### Basic Usage

#### Using Specialized Agents

**Automatic Selection** (recommended):
```
"Optimize this database query"
→ Claude Code automatically selects database-optimizer

"Build a React dashboard with authentication"
→ Orchestrates frontend-developer → backend-architect → security-auditor
```

**Explicit Invocation**:
```
"Use code-reviewer to analyze this component"
"Have security-auditor check for OWASP compliance"
"Get performance-engineer to profile this bottleneck"
```

#### GitHub Workflows

**Create Issue:**
```
"Create a GitHub issue for user authentication feature"
→ Uses commands/issue.md workflow
→ Analyzes repo, creates sub-issues, generates dependency graph
```

**Create Pull Request:**
```
"Create a PR for the authentication implementation"
→ Uses commands/pr.md workflow
→ Detects templates, analyzes conventions, generates comprehensive PR
```

**Track Todos:**
```
"Initialize todo tracking for this project"
→ Uses commands/todos.md workflow
→ Sets up orchestrated task management
```

## Agent Selection Guide

### By Task Type

| Task                    | Recommended Agent(s)                          | Workflow Pattern                  |
|-------------------------|-----------------------------------------------|-----------------------------------|
| API Design              | `backend-architect` → `api-documenter`        | Sequential                        |
| Full-Stack Feature      | `backend-architect` → `frontend-developer` → `test-automator` | Sequential |
| Security Audit          | `security-auditor` → `code-reviewer`          | Validation Pipeline              |
| Performance Issue       | `performance-engineer` + `database-optimizer` | Parallel Execution               |
| Production Incident     | `incident-responder` → `devops-troubleshooter` | Conditional Routing             |
| ML Pipeline             | `mlops-engineer` → `ml-engineer` → `data-engineer` | Sequential               |
| Infrastructure Setup    | `cloud-architect` → `terraform-specialist`    | Sequential                        |
| Database Optimization   | `database-optimizer` → `code-reviewer`        | Validation Pipeline              |

### By Technology Stack

| Stack                   | Primary Agents                                | Support Agents                    |
|-------------------------|-----------------------------------------------|-----------------------------------|
| React + Node.js         | `typescript-pro`, `javascript-pro`            | `frontend-developer`, `backend-architect` |
| Python/Django           | `python-pro`, `django-pro`                    | `backend-architect`, `database-optimizer` |
| Rust Systems            | `rust-pro`                                    | `c-pro`, `performance-engineer`   |
| Cloud Infrastructure    | `cloud-architect`, `terraform-specialist`     | `kubernetes-architect`, `network-engineer` |
| Mobile (iOS)            | `ios-developer`, `swift-pro`                  | `mobile-developer`, `ui-ux-designer` |
| Mobile (Cross-platform) | `flutter-expert`, `mobile-developer`          | `ui-ux-designer`, `performance-engineer` |
| ML/AI Applications      | `ai-engineer`, `ml-engineer`                  | `mlops-engineer`, `python-pro`    |
| Microservices           | `backend-architect`, `kubernetes-architect`   | `cloud-architect`, `observability-engineer` |

## Advanced Usage

### Custom Workflows

Create custom command templates in `commands/`:

```markdown
---
name: custom-workflow
description: Your workflow description
---

# Your Custom Workflow

Instructions and steps...
```

### Agent Coordination

For complex tasks requiring multiple specialists:

```
"Implement payment processing with full security audit and documentation"

→ Orchestrates:
   1. payment-integration (implementation)
   2. backend-security-coder (secure coding)
   3. security-auditor (vulnerability scan)
   4. api-documenter (documentation)
   5. code-reviewer (final validation)
```

### Session Persistence

All sessions persist across Claude Code invocations:
- **Project context**: Stored in `projects/[project-path].jsonl`
- **Shell history**: Saved in `shell-snapshots/[session-id]`
- **Todo state**: Tracked in `todos/[project-id].json`

## Configuration

### Settings (`settings.json`)

```json
{
  "alwaysThinkingEnabled": true
}
```

- `alwaysThinkingEnabled`: Enables extended reasoning for complex tasks

### Privacy & Git

The `.gitignore` is configured to:
- **Track**: `commands/`, `agents/`, `templates/`, `README.md`, `CLAUDE.md`
- **Ignore**: `projects/`, `shell-snapshots/`, `todos/`, `statsig/`, `ide/`, session data

Only shared configuration and templates are version controlled.

## Best Practices

### Task Delegation
1. **Automatic selection** - Let Claude Code analyze and select optimal agents
2. **Clear requirements** - Specify constraints, tech stack, quality standards
3. **Trust specialization** - Each agent is optimized for their domain

### Multi-Agent Workflows
1. **High-level requests** - Allow agents to coordinate multi-step tasks
2. **Context preservation** - Ensure agents have necessary background
3. **Integration review** - Verify how outputs work together

### GitHub Operations
1. **Template detection** - Always check for existing repository templates
2. **Convention analysis** - Review recent issues/PRs for patterns
3. **Quality validation** - Use checklists and acceptance criteria

### Performance Optimization
1. **Model selection** - Haiku for simple tasks, Opus for complex analysis
2. **Parallel execution** - Use concurrent agents when tasks are independent
3. **Sequential workflows** - Chain agents when context must flow forward

## Troubleshooting

### Agent Not Activating
- Ensure request clearly indicates the domain
- Be specific about task type and requirements
- Use explicit invocation if automatic selection fails

### Unexpected Agent Selection
- Provide more context about tech stack
- Include specific requirements in request
- Use direct agent naming for precise control

### GitHub Template Not Found
- Check paths: `~/.claude/templates/GH_*_TEMPLATE.md`
- Verify template exists before workflow execution
- Review `commands/issue.md` and `commands/pr.md` for template paths

### Todo Tracking Issues
- Initialize with `claude todos --init` before use
- Verify project context is set correctly
- Check `todos/` directory for state files

## Contributing

To add new agents or workflows:

1. **New Agent**: Create `.md` file in `agents/` with frontmatter
2. **New Workflow**: Add template to `commands/`
3. **New Template**: Add to `templates/`
4. **Documentation**: Update this README and CLAUDE.md

## Resources

- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Subagents Documentation](https://docs.anthropic.com/en/docs/claude-code/sub-agents)
- [Claude Code GitHub](https://github.com/anthropics/claude-code)

## License

MIT License - Personal configuration repository for Claude Code.
