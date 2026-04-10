# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

Personal Claude Code configuration directory with 83+ specialized AI agents, 13 custom skills, 13 slash commands, and three development methodologies.

## Development Methodologies

Three progressive approaches — always reference `README.md` for full workflow diagrams:

1. **Individual: Issue-Driven** — `/issue` -> `/task` -> `/pr`
2. **Behavioral: BDD** — `/user-story` -> `/issue` -> `/task` -> `/pr`
3. **Scaled: Epic-Driven (Agent Teams)** — `/work-on-opens` (wraps `/task` + `/pr`, uses `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` and git worktrees)

**Supporting planning commands:** `/architecture` and `/mvp-requirements` feed into any methodology.

## Key Architecture

### Commands (`commands/`)

13 slash command templates for GitHub workflows, planning, research, and content generation. See `commands/README.md` for full documentation.

**Key behaviors:**
- `/issue` reads templates from `~/.claude/templates/GH_*_TEMPLATE.md`, analyzes repo conventions, maps skills to sub-issues, estimates with Fibonacci story points
- `/pr` detects existing PR templates, analyzes recent PRs for conventions
- `/work-on-opens` processes priority boards with tier-based parallel execution

**Progress Tracking:** Status updates are made by editing the parent issue description. Check boxes in the "Completed" column track progress. Single source of truth — DO NOT use comments for status updates.

### Skills (`skills/`)

13 specialized skills in two categories. See `skills/README.md` for full catalog.

- **Claude Code Customization** (6): create-skill, create-subagent, create-command, create-hooks, create-claude-plugin, connect-mcp-server
- **Domain Expertise** (7): webgl-expert, nightingale-expert, argus-deployment, notebooklm, secure-web-search, analyzing-financial-statements, creating-financial-models

### Agents (`agents/` - Git Submodule)

83+ specialized AI subagents from [wshobson/agents](https://github.com/wshobson/agents), optimized across Haiku/Sonnet/Opus tiers. See `agents/README.md` for catalog and orchestration patterns.

### Templates (`templates/`)

Fixed paths — always load before workflow execution:
- Parent issues: `~/.claude/templates/GH_PARENT_ISSUE_TEMPLATE.md`
- Sub-issues: `~/.claude/templates/GH_SUB_ISSUE_TEMPLATE.md`
- Pull requests: `~/.claude/templates/GH_PR_TEMPLATE.md`
- User stories: `~/.claude/templates/GH_USER_STORY_TEMPLATE.md`

## Directory Structure

```
.claude/
├── commands/           # Slash command templates (13)
├── skills/            # Custom skills (13)
├── agents/            # AI subagents (83+, git submodule)
├── templates/         # GitHub PR/issue templates
├── projects/          # Session history (.jsonl)
├── shell-snapshots/   # Shell session persistence
├── todos/            # Task tracking (.json)
├── plugins/          # Claude Code plugins
├── statsig/          # Analytics cache
└── ide/              # IDE integration
```

## Settings

- `alwaysThinkingEnabled: true` — Extended reasoning for complex tasks

## Calendar Management

**Personal Calendar:** `ronnyangelo.freites@gmail.com`

When creating personal calendar events, always use the `ronnyangelo.freites@gmail.com` calendar instead of the default "Home" calendar.

```applescript
tell application "Calendar"
    tell calendar "ronnyangelo.freites@gmail.com"
        make new event with properties {summary:"Event Name", start date:startDate, end date:endDate}
    end tell
end tell
```

## MemPalace Memory System

MemPalace is active as an MCP server with 19 tools for persistent memory across sessions.

**At session start:** The `SessionStart` hook auto-initializes and mines the project if the palace doesn't exist yet. Always call `mempalace_status` at the beginning of every session to load the memory protocol and AAAK spec — even when already initialized.

**When to search (call `mempalace_search`):**
- Before answering questions about past decisions, architecture choices, or preferences
- When context references something that may have been discussed before
- When asked "why did we..." or "what did we decide about..."

**When to save (call `mempalace_add_drawer`):**
- After important decisions or architecture choices
- When solving a non-trivial bug (include root cause + fix)
- At task completion — file the outcome to the relevant wing/room

**Wing/room structure:** Use `mempalace_list_wings` and `mempalace_list_rooms` to navigate. File memories to the correct wing (person or project) and room (topic).

**Agents:** When spawning subagents for significant tasks, instruct them to call `mempalace_search` for context and `mempalace_add_drawer` to persist findings.

**Palace location:** Each project stores its own palace at `<project_dir>/.mempalace`. The `SessionStart` hook updates `~/.mempalace/config.json` at session start so the MCP server always points to the current project.

Auto-save hooks are active — Stop hook fires every 15 messages, PreCompact hook fires before context compression.

## Usage Notes

1. **Command templates** reference specific file paths — always load templates first
2. **Repository analysis** is critical — check CONTRIBUTING.md, existing issues/PRs
3. **Agent selection** happens automatically based on task, or invoke explicitly
4. **Skills** are invoked automatically or explicitly via `Skill(skill: "skill-name")`
5. **Git tracking**: Only `commands/`, `templates/`, `skills/`, `README.md`, `CLAUDE.md` are versioned
