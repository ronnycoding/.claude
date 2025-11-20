# Claude Code Commands Reference

Comprehensive documentation for all Claude Code slash commands and workflows.

## Table of Contents

- [Overview](#overview)
- [GitHub Workflow Commands](#github-workflow-commands)
  - [/issue - Issue Creation](#issue---github-issue-creation)
  - [/pr - Pull Request Creation](#pr---github-pull-request-creation)
  - [/user-story - BDD User Stories](#user-story---bdd-user-story-creation)
- [Task Management Commands](#task-management-commands)
  - [/task - Task Orchestration](#task---task-orchestration)
  - [/todos - Todo Tracking](#todos---todo-tracking)
- [Content Generation Commands](#content-generation-commands)
  - [/nlm-research - Research Generator](#nlm-research---notebooklm-research-generator)
  - [/tiktok-tech - TikTok Scripts](#tiktok-tech---tiktok-tech-news-digest)
- [Development Commands](#development-commands)
  - [/prompt - Prompt Engineering](#prompt---prompt-engineering)

---

## Overview

These commands are sophisticated workflow templates that orchestrate multi-phase operations, integrate with GitHub, and leverage specialized agents for complex tasks.

**Key Features:**
- Multi-phase workflows with progress tracking
- GitHub CLI integration
- Template-based issue/PR creation
- Agent orchestration support
- Semantic versioning enforcement
- BDD/Gherkin syntax support

---

## GitHub Workflow Commands

### `/issue` - GitHub Issue Creation

Creates comprehensive GitHub issues with intelligent sub-issue decomposition and agent assignment.

**Template Used:** `~/.claude/templates/GH_PARENT_ISSUE_TEMPLATE.md`, `~/.claude/templates/GH_SUB_ISSUE_TEMPLATE.md`

**Usage:**
```bash
/issue Implement user authentication with OAuth2 support
```

**Workflow Phases:**

1. **Repository Research**
   - Examines project structure and codebase
   - Reviews existing issues for conventions
   - Checks CONTRIBUTING.md and templates
   - Analyzes coding style and patterns

2. **Skill & Tooling Analysis**
   - Lists available Claude Code skills
   - Maps skills to sub-tasks
   - Recommends new skill creation for specialized work
   - Documents skill-to-task mappings

3. **Best Practices Research**
   - Searches current GitHub issue best practices
   - Studies effective decomposition strategies
   - Reviews work breakdown structures (WBS)

4. **Issue Classification & Decomposition**
   - Determines issue type (feature/bug/improvement)
   - Identifies logical components
   - Maps dependencies between sub-issues
   - Estimates using Fibonacci story points (1, 2, 3, 5, 8, 13, 21)

5. **Parent Issue Structure**
   - Creates comprehensive description with task breakdown table
   - Includes "Completed" column for progress tracking
   - Defines integration points
   - Adds clear status update instructions

6. **Sub-Issue Creation**
   - Assigns specialized agents/team members
   - Defines clear scope and interfaces
   - Establishes dependency chains
   - Specifies required Claude Code skills

7. **Quality Assurance**
   - Validates completeness and actionability
   - Checks alignment with conventions
   - Verifies dependencies and assignments

**Story Points:**
- Uses Fibonacci sequence: 1, 2, 3, 5, 8, 13, 21
- Never uses time-based estimates
- Represents complexity and effort

**Example:**
```bash
/issue Add payment processing with Stripe integration and webhook handling
```

**Output:**
- Parent issue with task breakdown table
- Multiple sub-issues with clear scope
- Dependency graph
- Agent/team assignments
- Integration points defined

---

### `/pr` - GitHub Pull Request Creation

Generates well-structured pull requests following repository conventions with comprehensive analysis.

**Template Used:** `~/.claude/templates/GH_PR_TEMPLATE.md`

**Usage:**
```bash
/pr Add user authentication with OAuth2 and JWT tokens
```

**Workflow Phases:**

1. **Template Detection & Repository Analysis**
   - Checks for existing PR templates in `.github/`
   - Analyzes 10-20 recent PRs for conventions
   - Identifies title format patterns
   - Reviews CONTRIBUTING.md and CODEOWNERS
   - Checks merge strategy and CI/CD requirements

2. **Change Classification & Impact Analysis**
   - **Change Type**: feature, bugfix, hotfix, refactor, docs, test, chore, performance, security
   - **Impact Level**: Critical, High, Medium, Low
   - **Risk Assessment**: Breaking changes, backward compatibility, dependency updates

3. **Content Generation**
   - Title following detected patterns
   - Clear problem statement and solution approach
   - Implementation details and user impact
   - Technical considerations and trade-offs

**Title Formats Detected:**
- Conventional: `type(scope): description`
- GitHub: `[TYPE] Description (#issue)`
- Descriptive: `Add/Fix/Update X for Y`
- Jira: `[PROJ-123] Description`

**Example:**
```bash
/pr feat(auth): implement OAuth2 authentication with Google and GitHub providers
```

**Output:**
- Repository analysis summary
- Complete PR description with all sections
- Test evidence and validation steps
- Risk assessment and rollback plan

---

### `/user-story` - BDD User Story Creation

Creates comprehensive BDD user stories with Gherkin syntax, semantic versioning, and GitHub Projects integration.

**Template Used:** `~/.claude/templates/GH_USER_STORY_TEMPLATE.md`

**Usage:**
```bash
/user-story Create admin dashboard with analytics
```

**Workflow Phases:**

1. **Load Template & Context**
   - Reads user story template
   - Analyzes existing stories for conventions
   - Reviews project documentation

2. **Gather Story Overview**
   - Feature name and persona
   - User goal and benefit
   - Formats as: "As a [persona] I want [goal] So that [benefit]"

3. **Collect Version Information**
   - Version number (X.Y.Z format)
   - Change type (Feature/Bug Fix/Breaking Change)
   - Validates semantic versioning
   - Adds version label (e.g., `v2.1.0`)

4. **Define Gherkin Scenarios**
   - Primary happy path
   - Alternative paths
   - Error/edge cases
   - Proper Given/When/Then syntax

5. **Collect Business Context**
   - Problem statement
   - Priority and user segment
   - Expected usage frequency
   - Business value metrics

6. **Define Technical Context**
   - Dependencies and integration points
   - Data requirements
   - UI/UX needs
   - Accessibility requirements

7. **Specify Testing Strategy**
   - Test coverage requirements
   - Performance criteria
   - Definition of Done

8. **Collect Metadata**
   - Story points estimate
   - Epic linkage
   - Sprint target
   - Labels and related stories

9. **GitHub Project Integration**
   - Creates issue in specified repository
   - Adds to GitHub Project automatically
   - Includes version badge and labels

**Semantic Version Validation:**
```
Valid:   1.0.0, v2.3.4, 0.1.0, 10.20.30
Invalid: 1.2, 01.2.3, 1.2.3.4, abc, 1.2.x
```

**Version Impact:**
- **Feature**: Minor bump (1.0.0 → 1.1.0)
- **Bug Fix**: Patch bump (1.0.0 → 1.0.1)
- **Breaking Change**: Major bump (1.0.0 → 2.0.0)

**Example Gherkin:**
```gherkin
Feature: Admin Analytics Dashboard

  Scenario: View real-time user metrics
    Given I am logged in as an administrator
    And I navigate to the analytics dashboard
    When the page loads
    Then I should see current active users
    And I should see today's registration count
    And the data should refresh every 30 seconds
```

**Output:**
- Complete BDD user story with Gherkin scenarios
- Version badge and labels
- GitHub issue link
- Confirmation of Project addition

---

## Task Management Commands

### `/task` - Task Orchestration

Enhanced task resolution with agent orchestration, parallel execution, and comprehensive tracking.

**Usage:**
```bash
/task #123
```

**Workflow Phases:**

1. **Initial Setup & Issue Registration**
   - Fetches issue details via `gh`
   - Creates feature branch
   - Initializes orchestration tracking

2. **Analysis, Planning & Agent Discovery**
   - Comprehensive issue analysis
   - Agent capability assessment
   - Planning matrix creation
   - Complexity estimation

3. **Task Decomposition & Agent Assignment**
   - Intelligent task breakdown
   - Agent assignment with tracking
   - Subtask IDs (ST-001, ST-002, etc.)
   - Dependency mapping

4. **Parallel Agent Execution**
   - Launches agents in parallel
   - Real-time progress monitoring
   - Inter-agent communication
   - Conflict detection and resolution

5. **Integration & Testing**
   - Automated integration
   - Comprehensive test suite
   - Quality gate validation
   - Acceptance criteria verification

6. **Consolidated PR Creation**
   - Aggregates agent contributions
   - Co-author attribution
   - Test results and metrics
   - Quality reports

7. **Review & Completion**
   - Review monitoring
   - Feedback handling
   - Merge and tracking completion
   - Report generation

**Agent Assignment Example:**
```bash
BACKEND_TASK_ID=$(claude agent assign \
  --agent="backend-specialist" \
  --parent-issue="123" \
  --subtask-id="ST-001" \
  --description="Implement REST API endpoints" \
  --priority="high" \
  --dependencies="none" \
  --estimated-time="1d" \
  --success-criteria="All endpoints return correct status codes")
```

**Status Dashboard:**
```
┌─────────────────────────────────────────────────────────┐
│ Issue #123: Implement User Authentication              │
├─────────────────────────────────────────────────────────┤
│ Progress: ████████████████░░░░░░ 75%                   │
│ Phase: Integration                                      │
│ Agents: 5 active, 2 complete, 0 failed                 │
├─────────────────────────────────────────────────────────┤
│ Subtasks:                                              │
│ ✅ Backend API        (backend-specialist)    100%     │
│ ✅ Frontend UI        (frontend-specialist)   100%     │
│ 🔄 Testing           (test-specialist)       60%      │
│ ⏸️  Documentation     (docs-specialist)       0%       │
│ 🔄 Coordination      (coord-specialist)      Active    │
└─────────────────────────────────────────────────────────┘
```

**Advanced Commands:**
```bash
# Task decomposition
claude task decompose --issue="123"

# Agent orchestration
claude agent list --available
claude agent recommend --issue="123"
claude agent execute-all --parent-issue="123" --mode="parallel"

# Progress monitoring
claude agent monitor --parent-issue="123" --format="dashboard"
claude todos --status --issue="123" --show-subtasks --format="tree"

# Integration
claude integrate --parent-issue="123" --strategy="incremental"

# Reporting
claude report progress --issue="123"
claude report quality --issue="123"
```

---

### `/todos` - Todo Tracking

Advanced todo tracking with agent orchestration support and rich formatting.

**Usage:**
```bash
# Initialize project tracking
/todos --init --project="MyProject" --repo="https://github.com/user/repo"

# Add issue
/todos --add --issue="123" --title="Implement Auth" --branch="feature/auth" --type="orchestration" --priority="high"

# Update progress
/todos --update --issue="123" --phase="integration" --progress="75" --agents="backend,frontend,test"

# Add subtask
/todos --add-subtask --parent="123" --id="ST-001" --agent="backend-specialist" --task="Implement API endpoints"

# Update subtask
/todos --update-subtask --parent="123" --id="ST-001" --progress="100" --status="complete"

# View status
/todos --status [--issue="123"] [--tree]

# Complete
/todos --complete --issue="123" --pr="456"
```

**Output Format (todos.md):**
```markdown
# TODOs

> Project: MyProject | Updated: 2024-01-16 14:30:00
> Active: 4 | Review: 2 | Completed: 5

## 🚀 In Progress

### [#123] Implement User Authentication [ORCHESTRATED]

- **Branch**: `feature/auth`
- **Priority**: High | **Progress**: 75%
- **Phase**: Integration

#### Agents (3/5 complete)

- ✅ ST-001: Backend API (backend-specialist)
- ✅ ST-002: Frontend UI (frontend-specialist)
- 🔄 ST-003: Testing (test-specialist) - 60%
- ⏸️ ST-004: Docs (docs-specialist)
- 🔄 ST-000: Coordination (coord-specialist)

#### Tasks

- [x] Analysis complete
- [x] Agents assigned
- [x] Backend implemented
- [ ] Testing (in progress)
- [ ] Documentation
- [ ] Create PR
```

**Tree View:**
```
📁 MyProject (4 active, 2 review, 5 completed)
├── 🚀 In Progress
│   ├── #123: User Authentication [75%]
│   │   ├── ✅ Backend API
│   │   ├── ✅ Frontend UI
│   │   ├── 🔄 Testing (60%)
│   │   └── ⏸️ Documentation
│   └── #124: Memory Leak [60%]
├── 🔄 In Review
│   └── #122: Documentation (1/2)
└── ⏸️ Blocked
    └── #125: Payment Integration
```

**Status Codes:**
- 🚀 In Progress
- 🔄 In Review
- ⏸️ Blocked
- ✅ Completed
- 📋 Planned

**Priority Levels:**
- 🔴 Critical
- 🟠 High
- 🟡 Medium
- 🟢 Low

---

## Content Generation Commands

### `/nlm-research` - NotebookLM Research Generator

Generate comprehensive research reports using Google NotebookLM with multi-source aggregation.

**Usage:**
```bash
/nlm-research --project="Acme SaaS" --type=mvp-design \
  --urls="https://competitor1.com" \
  --files="./requirements.pdf" \
  --outputs="guide,audio" \
  --save-to="./research/acme-mvp"
```

**Research Types:**
- `mvp-design` - MVP product design with features, tech stack, timeline
- `market-analysis` - Market research, competitors, trends, opportunities
- `technical-doc` - Technical documentation and architecture guides
- `business-plan` - Business strategy, financials, go-to-market
- `competitive-intel` - Deep competitor analysis with SWOT
- `custom` - Flexible research with custom instructions

**Input Sources:**
- `--urls` - Web pages and articles (comma-separated)
- `--files` - Local PDFs, docs, markdown files
- `--docs` - Google Docs share links
- `--text` - Direct text content

**Output Options:**
- `guide` - Comprehensive structured summary
- `outline` - Hierarchical topic structure
- `section` - Focused content sections
- `audio` - AI-generated audio overview with transcript
- `all` - Generate everything

**Features:**
- Multi-source aggregation with rate limiting
- Automated workflow from setup to export
- Customizable audio tone and audience
- Organized directory structure with timestamps
- Quality assurance and error handling

See `nlm-research.md` for complete documentation.

---

### `/tiktok-tech` - TikTok Tech News Digest

Generate comprehensive, bilingual TikTok scripts covering multiple tech stories.

**Usage:**
```bash
/tiktok-tech [Paste your weekly tech digest or multiple tech stories]
```

**Format:** Single comprehensive news digest (90-120 seconds)

**Features:**
- **News Anchor Style**: Professional presenter format
- **Comprehensive Coverage**: 3-5 interconnected stories
- **Unified Narrative**: Connects developments
- **Analysis Section**: Industry implications
- **BILINGUAL**: Complete English AND Spanish scripts
- **Professional Production**: B-roll, graphics, lower thirds
- **Actionable Takeaways**: Developer action items
- **Auto-saved**: Saves to `docs/tiktok-scripts/`

**Output Includes:**
- Complete dialogue with timing marks (00:00 format)
- Visual cues and B-roll suggestions
- Story transition cues
- Lower thirds and text overlays
- Analysis connecting all stories
- Production notes (music, background, hashtags)
- Full Spanish translation with cultural adaptations

**Example:**
```bash
/tiktok-tech Vercel launched AI agents marketplace. LangChain clarified Framework vs Runtime. Python 3.14 removed GIL. Microsoft Edge released agentic browsing. Cloudflare partnered with Visa/Mastercard for AI agent transactions.
```

**Perfect For:**
- Weekly tech roundups
- Industry trend analysis
- Multi-story deep dives
- Educational tech content
- Professional developer updates

---

## Development Commands

### `/prompt` - Prompt Engineering

Generate effective, well-structured prompts using advanced prompt engineering techniques.

**Usage:**
```bash
/prompt task="Create a REST API client" audience="Claude Sonnet" style="technical" format="code"
```

**Parameters:**
- `task` (required): The task or goal
- `audience`: Target (e.g., "Claude Sonnet", "developer")
- `style`: Output style (e.g., "technical", "conversational")
- `format`: Expected format (e.g., "code", "markdown", "json")

**Prompt Engineering Framework:**

1. **Context Analysis**
   - Core objective identification
   - Domain knowledge requirements
   - Edge cases and ambiguities
   - Constraints and requirements

2. **Prompt Structure Design**
   - Role assignment
   - Clear objective statement
   - Context provision
   - Requirements & constraints
   - Examples (when helpful)
   - Output format specification
   - Thinking process (for complex tasks)

3. **Optimization Techniques**
   - Specificity over vagueness
   - Task decomposition
   - Chain-of-thought reasoning
   - Few-shot learning
   - Positive constraints
   - Validation steps
   - XML tags for structure

4. **Quality Checklist**
   - Clear and unambiguous objective
   - Sufficient context
   - Specific requirements
   - Well-defined output format
   - Concise language
   - Edge cases addressed

**Output Template:**
```markdown
# [Prompt Title]

## Role & Context
[Assign role, provide context]

## Objective
[Clear goal statement]

## Requirements
[Specific requirements]

## Constraints
[Limitations and boundaries]

## Output Format
[Detailed specification]

## Examples
[Input/output examples]

## Thinking Process
[Step-by-step reasoning]

## Quality Criteria
[Success evaluation]
```

**Advanced Patterns:**
- Multi-agent pattern
- Validation loop
- Progressive disclosure
- Socratic method
- Meta-prompting

---

## Tips & Best Practices

**GitHub Workflows:**
- Always review repository conventions first
- Use Fibonacci story points (1, 2, 3, 5, 8, 13, 21)
- Update parent issue descriptions for progress tracking
- Don't use comments for status updates
- Link related issues and PRs

**Task Management:**
- Initialize tracking before starting work
- Update progress regularly
- Use tree view for complex orchestrations
- Monitor agent conflicts
- Generate completion reports

**Content Generation:**
- Provide comprehensive input for better output
- Include dates and sources
- Use specific research types
- Request audio for accessibility

**Prompt Engineering:**
- Be specific about audience and format
- Include examples for complex patterns
- Use XML tags for structure
- Request chain-of-thought for reasoning

---

## Related Documentation

- Templates: `~/.claude/templates/`
- Skills: `~/.claude/skills/`
- Agents: `~/.claude/agents/`
- GitHub CLI: `gh help`

