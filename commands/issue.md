# GitHub Issue Creation Template with Sub-Issue Management

You are an AI assistant tasked with creating well-structured GitHub issues for feature requests, bug reports, or improvement ideas, with the capability to decompose complex issues into manageable sub-issues that can be assigned to different team members or agents.

<feature_description>
$ARGUMENTS
</feature_description>

## Instructions

1. First, read the required templates:
   - Parent issue: ~/.claude/templates/GH_PARENT_ISSUE_TEMPLATE.md
   - Sub-issues: ~/.claude/templates/GH_SUB_ISSUE_TEMPLATE.md
   - Use these template structures for creating the parent issue and all sub-issues

2. Analyze the current repository context (you are already in the project directory)

3. Identify Claude Code skills and tooling:
   - Review available skills in `~/.claude/` for applicable domain expertise
   - Determine if existing skills can be used standalone or with agents
   - Identify highly technical/domain-specific tasks that may require new custom skills
   - Recommend skill creation for specialized workflows needing high-quality output

4. Decompose the feature and create issues using the loaded templates

5. Use story points for estimation:
   - Apply Fibonacci sequence: 1, 2, 3, 5, 8, 13, 21
   - Never use time-based estimates (hours/days)
   - Story points represent complexity and effort relative to other tasks

## TODO List

Follow these steps to complete the task systematically:

### Phase 1: Repository Research

- [ ] Examine the current project structure and codebase
- [ ] Use `gh` CLI to review existing issues and understand patterns/conventions
- [ ] Look for CONTRIBUTING.md, ISSUE_TEMPLATE.md, or .github/ISSUE_TEMPLATE/ files
- [ ] Identify the project's coding style and naming conventions
- [ ] Note any specific requirements for submitting issues
- [ ] Review the README.md for project context and contribution guidelines
- [ ] Use `gh` to check labels, milestones, and project boards
- [ ] Analyze how the project handles issue dependencies and sub-tasks
- [ ] Check if the project uses GitHub Projects or similar task tracking tools
- [ ] Use `gh api` to identify contributors and their areas of expertise

### Phase 2: Skill & Tooling Analysis

- [ ] List available Claude Code skills in `~/.claude/skills/` directory
- [ ] Review skill descriptions and capabilities for domain relevance
- [ ] Identify existing skills applicable to the feature requirements
- [ ] Determine if skills should be used standalone or combined with agents
- [ ] Analyze technical complexity and domain specificity of each sub-task
- [ ] Identify gaps where custom skills would improve output quality
- [ ] Recommend new skill creation for highly specialized workflows (e.g., financial modeling, legal compliance, medical data processing)
- [ ] Document skill-to-task mappings in the issue breakdown

### Phase 3: Best Practices Research

- [ ] Search for current best practices in writing GitHub issues
- [ ] Focus on clarity, completeness, and actionability principles
- [ ] Look for examples of well-written issues in popular projects for inspiration
- [ ] Research effective issue templates and structures
- [ ] Understand the importance of reproducible steps and clear acceptance criteria
- [ ] Research best practices for issue decomposition and task dependencies
- [ ] Study effective work breakdown structures (WBS) for software projects
- [ ] Learn about GitHub's task list syntax and issue linking mechanisms

### Phase 4: Issue Classification & Decomposition

- [ ] Determine if this is a feature request, bug report, or improvement
- [ ] Identify the appropriate issue template to follow (if available)
- [ ] Select relevant labels based on repository conventions
- [ ] Assess priority and complexity level
- [ ] Analyze if the issue should be broken down into sub-issues
- [ ] Identify logical components or modules that can be worked on independently
- [ ] Determine dependencies between potential sub-issues
- [ ] Estimate story points for each sub-task using Fibonacci sequence (1, 2, 3, 5, 8, 13, 21)
- [ ] Map sub-issues to appropriate team members/agents based on expertise

### Phase 5: Parent Issue Structure Creation

- [ ] Write a clear, descriptive title (50-72 characters recommended)
- [ ] Create a comprehensive description following this structure:
- [ ] **Summary**: Brief overview of the request/issue
- [ ] **Problem Statement**: What problem does this solve?
- [ ] **Proposed Solution**: Detailed description of the requested feature/fix
- [ ] **Task Breakdown**: Sub-issues table with "Completed" column for tracking progress
- [ ] **Status Update Instructions**: Include clear note to update completion status in issue description, NOT in comments
- [ ] **Acceptance Criteria**: Clear, testable conditions for completion
- [ ] **Additional Context**: Screenshots, examples, or related issues
- [ ] **Implementation Notes**: Technical considerations (if applicable)
- [ ] Create a task tracking section linking to sub-issues
- [ ] Define integration points between sub-issues

### Phase 6: Sub-Issue Creation

- [ ] For each identified sub-task, create a detailed sub-issue structure
- [ ] Assign appropriate specialized agents/team members with their expertise area
- [ ] Include story points for each sub-issue using Fibonacci sequence
- [ ] Establish clear scope boundaries for each sub-issue
- [ ] Define interfaces and handoff points between sub-issues
- [ ] Set up dependency chains and blocking relationships
- [ ] Create a timeline/roadmap for sub-issue completion
- [ ] Define integration testing requirements between components
- [ ] Document handoff checklists for agent-to-agent transitions
- [ ] Specify Claude Code skills needed for each sub-issue (if applicable)
- [ ] Note where new custom skills should be created for domain-specific work

### Phase 7: Quality Assurance

- [ ] Ensure the parent issue is actionable and specific
- [ ] Verify all necessary information is included
- [ ] Check for proper formatting and readability
- [ ] Confirm alignment with project conventions
- [ ] Add appropriate labels, assignees, and milestones
- [ ] Validate sub-issue dependencies are correctly mapped
- [ ] Ensure no critical tasks are missing from decomposition
- [ ] Verify team member assignments match their expertise
- [ ] Check that integration points are well-defined

## Output

Create the parent issue and all sub-issues following the loaded templates from:
- `~/.claude/templates/GH_PARENT_ISSUE_TEMPLATE.md`
- `~/.claude/templates/GH_SUB_ISSUE_TEMPLATE.md`
