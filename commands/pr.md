# Enhanced GitHub Pull Request Creation Template

You are an AI assistant tasked with creating exceptional GitHub pull requests that follow best practices and project conventions. Your goal is to generate comprehensive PR content that facilitates effective code review and maintains project quality.

## Input Parameters

<change_description>

# $ARGUMENTS

</change_description>

<repository_url>

# $REPO_URL

</repository_url>

<branch_info>
Source Branch: #$SOURCE_BRANCH
Target Branch: #$TARGET_BRANCH
</branch_info>

<related_issues>

# $RELATED_ISSUES (optional: comma-separated issue numbers)

</related_issues>

<pull_request_template_path>

# ~/.claude/templates/GH_PR_TEMPLATE.md

</pull_request_template_path>

<reviewers>
#$REVIEWERS (optional: comma-separated GitHub usernames)
</reviewers>

<labels>
#$LABELS (optional: comma-separated labels)
</labels>

<pr_type>

# $PR_TYPE (optional: feature|bugfix|hotfix|refactor|docs|test|chore)

</pr_type>

## Instructions

1. First, read the pull request template from the specified path:
   - Load the template from: ~/.claude/templates/GH_PR_TEMPLATE.md
   - Use this template structure for ALL sub-issues you create

2. Analyze the feature and create sub-issues using the loaded template

## Comprehensive Analysis Process

### Phase 1: Template Detection & Repository Analysis

**CRITICAL FIRST STEP**:

1. Check for existing PR templates at:
   - `.github/pull_request_template.md`
   - `.github/PULL_REQUEST_TEMPLATE.md`
   - `.github/PULL_REQUEST_TEMPLATE/` (directory with multiple templates)
   - `docs/pull_request_template.md`
   - Root directory `pull_request_template.md`

2. **If template exists**:
   - Use it as the PRIMARY structure
   - Fill ALL sections with appropriate content
   - Maintain exact formatting and section order
   - Never skip required fields

3. **If no template exists**:
   - Analyze recent PRs to understand conventions
   - Use the comprehensive fallback template below

4. Repository convention analysis:
   - Review 10-20 recent merged PRs for patterns
   - Identify title format (conventional commits, prefixes, issue numbers)
   - Note common labels and their usage
   - Understand reviewer assignment patterns
   - Check merge strategy (squash, merge, rebase)
   - Look for required status checks
   - Review CONTRIBUTING.md guidelines
   - Check CODEOWNERS file
   - Identify CI/CD requirements

### Phase 2: Change Classification & Impact Analysis

Analyze the changes to determine:

1. **Change Type**:
   - Feature: New functionality added
   - Bugfix: Issue resolution
   - Hotfix: Critical production fix
   - Refactor: Code improvement without functional change
   - Docs: Documentation updates
   - Test: Test additions or modifications
   - Chore: Maintenance tasks
   - Performance: Optimization changes
   - Security: Security improvements

2. **Impact Level**:
   - **Critical**: Breaking changes, API modifications, data migrations
   - **High**: Major features, significant refactoring, security fixes
   - **Medium**: Standard features, bug fixes, performance improvements
   - **Low**: Documentation, minor fixes, code style changes

3. **Risk Assessment**:
   - Breaking changes identification
   - Backward compatibility check
   - Dependency updates impact
   - Database schema changes
   - Configuration modifications
   - API contract changes

### Phase 3: Content Generation Strategy

Based on your analysis, generate:

1. **Title** following detected patterns:
   - Conventional: `type(scope): description`
   - GitHub: `[TYPE] Description (#issue)`
   - Descriptive: `Add/Fix/Update X for Y`
   - Jira: `[PROJ-123] Description`

2. **Description** that includes:
   - Clear problem statement
   - Solution approach
   - Implementation details
   - User impact
   - Technical considerations

3. **Context** sections:
   - Why this change is needed
   - Alternative approaches considered
   - Trade-offs made
   - Future considerations

## Your Output Structure

### SECTION 1: Repository Analysis Summary

```markdown
## Repository Analysis

### Template Detection
- Template found: [Yes/No]
- Template location: [path if found]
- Template type: [standard/custom/multiple]

### Conventions Observed
- Title format: [pattern detected]
- Common labels: [list]
- Reviewer patterns: [auto-assign/manual/CODEOWNERS]
- Merge strategy: [squash/merge/rebase]
- Required checks: [list]

### Change Classification
- Type: [feature/bugfix/refactor/etc]
- Impact: [critical/high/medium/low]
- Risk level: [high/medium/low]
- Breaking changes: [yes/no]
