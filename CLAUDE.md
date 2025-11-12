# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal Claude Code configuration directory containing command templates, specialized AI agents, and GitHub workflow automation tools.

## Key Architecture

### Command Templates (`commands/`)

Sophisticated prompt templates for GitHub operations:

- **`issue.md`**: Multi-phase issue creation workflow with sub-issue decomposition
  - Analyzes repository conventions and existing templates
  - Breaks complex features into assignable sub-tasks
  - Creates dependency graphs and integration points
  - Template path: `~/.claude/templates/GH_SUB_ISSUE_TEMPLATE.md`

- **`pr.md`**: Comprehensive pull request creation workflow
  - Detects and uses existing PR templates (`.github/pull_request_template.md`)
  - Analyzes recent PRs for conventions (title format, labels, merge strategy)
  - Performs change classification and risk assessment
  - Template path: `~/.claude/templates/GH_PR_TEMPLATE.md`

- **`todos.md`**: Advanced todo tracking with agent orchestration
  - Supports orchestrated multi-agent workflows
  - Phase-based progress tracking (analysis, implementation, integration)
  - Tree view and status dashboard output

### Specialized Agents (`agents/` - Git Submodule)

Collection of specialized AI subagents from [wshobson/agents](https://github.com/wshobson/agents) repository.

Provides domain-specific specialists optimized across Claude model tiers (Haiku/Sonnet/Opus) for:

- Architecture & Design
- Programming Languages
- Infrastructure & Operations
- Security & Quality
- AI/ML & Data
- Documentation & Business

See `agents/README.md` for:

- Complete agent catalog and capabilities
- Model distribution and selection criteria
- Multi-agent orchestration patterns
- Usage examples and best practices

### Templates (`templates/`)

GitHub-specific templates:

- `GH_PR_TEMPLATE.md`: Standard PR structure with checklists
- `GH_PARENT_ISSUE_TEMPLATE.md`: Parent issue/epic format with task breakdown and story points
- `GH_SUB_ISSUE_TEMPLATE.md`: Sub-issue format with scope, dependencies, interfaces
- `GH_USER_STORY_TEMPLATE.md`: BDD user story with Gherkin syntax

## Directory Structure

```
.claude/
├── commands/           # GitHub operation prompt templates
├── agents/            # Specialized AI subagent definitions
├── templates/         # GitHub PR and issue templates
├── projects/          # Session history (.jsonl) by project path
├── shell-snapshots/   # Shell session persistence
├── todos/            # Individual task tracking (.json)
├── statsig/          # Analytics cache
├── plugins/          # Claude Code plugins
└── ide/              # IDE integration
```

## GitHub Workflow Commands

### Issue Creation

Uses `commands/issue.md` workflow:

1. Reads templates:
   - Parent issue: `~/.claude/templates/GH_PARENT_ISSUE_TEMPLATE.md`
   - Sub-issues: `~/.claude/templates/GH_SUB_ISSUE_TEMPLATE.md`
2. Analyzes repository for conventions (CONTRIBUTING.md, existing issues)
3. Decomposes complex features into sub-issues with dependencies
4. Estimates complexity using Fibonacci story points (1, 2, 3, 5, 8, 13, 21)
5. Creates dependency graphs and agent/team assignments
6. Generates parent epic with task breakdown table and integration points

**Progress Tracking:**
- Status updates are made by editing the parent issue description
- Check boxes in the "Completed" column track sub-issue progress
- Single source of truth - DO NOT use comments for status updates

### Pull Request Creation

Uses `commands/pr.md` workflow:

1. Reads template from `~/.claude/templates/GH_PR_TEMPLATE.md`
2. Checks for existing PR templates (`.github/pull_request_template.md`)
3. Analyzes 10-20 recent PRs for title format and conventions
4. Classifies change type (feature/bugfix/refactor/etc.) and impact level
5. Generates comprehensive PR with context and testing evidence

### Todo Management

Uses `commands/todos.md` workflow:

- Initialize: `claude todos --init --project="NAME" --repo="URL"`
- Add issue: `claude todos --add --issue="123" --type="orchestration"`
- Update: `claude todos --update --issue="123" --phase="integration" --progress="75"`
- Status: `claude todos --status [--tree]`

## Agent Orchestration Patterns

**Sequential Processing:**

```
backend-architect → frontend-developer → test-automator → security-auditor
```

**Parallel Execution:**

```
performance-engineer + database-optimizer → Merged analysis
```

**Validation Pipeline:**

```
payment-integration → security-auditor → Validated implementation
```

## Session Management

- **Project sessions**: Tracked in `projects/` as `.jsonl` files
- **Shell persistence**: Snapshots in `shell-snapshots/` for command history
- **Todo state**: Individual JSON files in `todos/` for cross-session tracking
- **Privacy**: Personal data gitignored, only shared templates versioned

## Settings

`settings.json` contains:

- `alwaysThinkingEnabled: true` - Extended reasoning for complex tasks

## Calendar Management

**Personal Calendar:** `ronnyangelo.freites@gmail.com`

When creating personal calendar events (appointments, personal tasks, non-work activities), always use the `ronnyangelo.freites@gmail.com` calendar instead of the default "Home" calendar.

**AppleScript Example:**
```applescript
tell application "Calendar"
    tell calendar "ronnyangelo.freites@gmail.com"
        make new event with properties {summary:"Event Name", start date:startDate, end date:endDate}
    end tell
end tell
```

## Usage Notes

1. **Command templates** reference specific file paths - always load templates first
2. **Repository analysis** is critical - check CONTRIBUTING.md, existing issues/PRs
3. **Agent selection** happens automatically based on task, or invoke explicitly
4. **Todo tracking** uses orchestration mode for multi-agent coordination
5. **Templates paths** are fixed:
   - Parent issues: `~/.claude/templates/GH_PARENT_ISSUE_TEMPLATE.md`
   - Sub-issues: `~/.claude/templates/GH_SUB_ISSUE_TEMPLATE.md`
   - Pull requests: `~/.claude/templates/GH_PR_TEMPLATE.md`
   - User stories: `~/.claude/templates/GH_USER_STORY_TEMPLATE.md`
