# Claude Code Configuration

Personal Claude Code configuration directory containing MCP integrations, GitHub templates, and development workflows.

## Overview

This directory contains configuration files and templates for Claude Code, enhancing AI-assisted development with external tool integrations and structured workflows.

## Features

### MCP Server Integrations
- **LinkedIn MCP**: Profile management and content posting
- **Weather MCP**: Weather data and alerts
- **GitHub MCP**: GitHub API integration via Copilot
- **Playwright**: Browser automation and testing

### GitHub Templates
- Issue creation with comprehensive research phases
- Pull request templates with quality assurance
- Todo management for complex development tasks

### Session Management
- Project-specific session tracking
- Shell command history persistence
- Cross-session todo state management

## Structure

```
.claude/
├── .mcp.json              # MCP server configurations
├── settings.json          # Permissions and user settings
├── commands/              # GitHub operation templates
│   ├── issue.md          # Issue creation template
│   ├── pr.md             # Pull request template
│   └── todos.md          # Todo management guide
├── projects/             # Session histories by project
├── shell-snapshots/      # Shell session persistence
├── todos/               # Individual todo tracking files
└── statsig/             # Analytics cache
```

## Usage

The configuration automatically loads when using Claude Code in any project. Templates in `commands/` provide structured approaches for GitHub operations and task management.

## Privacy

Personal session data and todos are gitignored. Only shared templates and base configuration are version controlled.