# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Architecture

This is a Claude Code configuration directory containing:

### Core Configuration Files
- `.mcp.json` - MCP server configurations for LinkedIn, Weather, GitHub, and Playwright integrations
- `settings.json` - Permissions, enabled MCP servers, and user settings
- `.gitignore` - Configured to track only the `commands/` folder while ignoring personal session data

### Directory Structure

**`commands/`** - Contains prompt templates for common GitHub operations:
- `issue.md` - Template for creating well-structured GitHub issues
- `pr.md` - Template for creating comprehensive pull requests  
- `task.md` - Duplicate PR template (same as pr.md)
- `todos.md` - Documentation for todo management workflow

**`projects/`** - Session history files (`.jsonl`) organized by project path, tracking development sessions across various repositories

**`shell-snapshots/`** - Shell session snapshots for persistence across Claude Code sessions

**`todos/`** - Individual todo files (`.json`) for tracking task progress across sessions

**`statsig/`** - Analytics and feature flag cache files

**`ide/`** - IDE integration lock files

## Available Tools and Integrations

### MCP Servers
- **LinkedIn MCP**: Profile data, education, courses, posting capabilities
- **Weather MCP**: Weather forecasts and alerts  
- **GitHub MCP**: GitHub integration via Copilot API
- **Playwright**: Browser automation and testing

### Command Templates
The `commands/` directory contains sophisticated templates for:
- **GitHub Issue Creation**: Comprehensive issue templates with research phases, quality assurance checklists, and best practices
- **Pull Request Creation**: Detailed PR templates with repository analysis, template detection, and quality guidelines
- **Todo Management**: Structured approach to task tracking with states (pending, in_progress, completed)

## Development Workflow

### Todo Management
- Use the TodoWrite tool to track complex tasks
- Limit to ONE task in_progress at a time
- Mark tasks completed immediately after finishing
- Todo files are project-specific and persist across sessions

### GitHub Operations
- Issue and PR templates emphasize thorough repository analysis before creation
- Templates automatically detect and use existing repository templates
- Focus on quality, completeness, and following project conventions

### Session Persistence
- Shell snapshots maintain command history across sessions
- Project-specific session files track development context
- Personal configuration is gitignored while shared templates are tracked

## Permissions
The `settings.json` file grants specific permissions for:
- UV/Python package management
- Git operations including commits
- Web fetching from approved domains
- File system operations

## Notes
- This is a personal Claude Code configuration directory, not a software project
- The `commands/` folder contains templates that can be referenced for GitHub operations
- Session data and personal todos are kept separate from shared configuration