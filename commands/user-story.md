---
description: Create BDD user stories with Gherkin syntax and add to GitHub Projects
---

You are creating a comprehensive BDD (Behavior-Driven Development) user story using Gherkin syntax. Follow this multi-phase workflow to gather all necessary information and create a complete user story issue in GitHub.

## Phase 1: Load Template and Understand Context

First, read the user story template:

```bash
cat ~/.claude/templates/GH_USER_STORY_TEMPLATE.md
```

If working in a repository, analyze existing context:
- Check for existing user stories or issues to understand conventions
- Look for CONTRIBUTING.md or project documentation
- Review recent issues for labeling patterns

## Phase 2: Gather Story Overview

Use the AskUserQuestion tool to collect the core user story information:

**Questions to ask:**
1. What is the feature or functionality name?
2. Who is the user persona? (e.g., "administrator", "end user", "developer")
3. What does the user want to accomplish?
4. What is the benefit or value they'll receive?

**Format the story as:**
```
As a [persona]
I want [goal]
So that [benefit]
```

## Phase 2.5: Collect Version Information

Use the AskUserQuestion tool to gather semantic versioning details:

**Questions to ask:**
1. What version will this be introduced in? (Format: X.Y.Z or vX.Y.Z)
2. What type of change is this?
   - **Feature**: New functionality (minor version bump: 1.0.0 → 1.1.0)
   - **Bug Fix**: Fixes existing functionality (patch version bump: 1.0.0 → 1.0.1)
   - **Breaking Change**: Requires user action (major version bump: 1.0.0 → 2.0.0)

**Semantic Version Validation:**
- Validate the version follows semver format: `MAJOR.MINOR.PATCH`
- Each component must be a non-negative integer
- No leading zeros (except 0 itself)
- Optional 'v' prefix is acceptable (e.g., v1.2.0 or 1.2.0)

**Validation Rules:**
```
Valid:   1.0.0, v2.3.4, 0.1.0, 10.20.30
Invalid: 1.2, 01.2.3, 1.2.3.4, abc, 1.2.x
```

**If validation fails:**
- Show the invalid format with clear error message
- Explain the semver format requirements
- Ask the user to provide a valid version number
- Suggest the appropriate version bump based on change type

**Version Impact Analysis:**
- For **Breaking Changes**: Explain what makes this breaking and why it requires a major version bump
- For **Features**: Describe the new capability being added
- For **Bug Fixes**: Explain what issue is being resolved

**Add to labels:**
Include the version label in format: `v[X.Y.Z]` (e.g., `v2.1.0`)

## Phase 3: Define Gherkin Scenarios

Use the AskUserQuestion tool to create detailed Gherkin scenarios. You need at least 3 scenarios:

**Scenario 1: Primary Happy Path**
Ask: "Describe the main success scenario step-by-step"
- What is the initial state? (Given)
- What action does the user take? (When)
- What should happen? (Then)

**Scenario 2: Alternative Path**
Ask: "Describe an alternative valid path or variation"
- Different starting conditions or actions
- Different but still successful outcome

**Scenario 3: Error/Edge Case**
Ask: "Describe an error scenario or edge case"
- Invalid input or conditions
- How should errors be handled?
- What feedback should the user receive?

**Additional Scenarios (if applicable)**
Ask: "Are there more scenarios to cover?" (validation, permissions, data boundaries, etc.)

Format each scenario in proper Gherkin syntax:
```gherkin
Feature: [Feature name]

  Scenario: [Descriptive scenario name]
    Given [precondition]
    And [additional context]
    When [action]
    And [additional action]
    Then [expected outcome]
    And [additional verification]
```

## Phase 4: Collect Business Context

Use the AskUserQuestion tool to gather:

1. **Problem Statement**: What problem does this solve?
2. **Priority**: High, Medium, or Low?
3. **User Segment**: Which users are affected?
4. **Expected Usage**: How frequently will this be used?
5. **Business Value**: Revenue impact, cost savings, user satisfaction metrics?

## Phase 5: Define Technical Context

Use the AskUserQuestion tool to identify:

1. **Dependencies**: What needs to be in place first?
   - Other features, APIs, services, or infrastructure
2. **Integration Points**: What systems/components does this interact with?
3. **Data Requirements**: What data entities or fields are needed?
4. **UI/UX Needs**: Are there design requirements, wireframes, or mockups?
5. **Accessibility Requirements**: Any specific accessibility needs beyond standard compliance?

## Phase 6: Specify Testing Strategy

Use the AskUserQuestion tool to define:

1. **Test Coverage**: What specific test cases are needed?
   - Unit tests
   - Integration tests
   - E2E tests (in Gherkin format)
2. **Performance Criteria**:
   - Response time requirements
   - Throughput expectations
   - Data volume considerations
3. **Definition of Done**: Any additional DoD criteria beyond the template defaults?

## Phase 7: Collect Metadata

Use the AskUserQuestion tool to gather:

1. **Story Points**: Estimate (or TBD)
2. **Epic**: Link to parent epic (if applicable)
3. **Sprint**: Target sprint (if known)
4. **Labels**: Component, priority, and other relevant labels
5. **Related Stories**: Links to related or dependent stories

## Phase 8: GitHub Project Integration

Use the AskUserQuestion tool to ask:

1. **Repository**: Which repository should this issue be created in?
2. **GitHub Project**: Provide the project number or URL
   - Format: `owner/project/NUMBER` or full project URL
   - Use `gh project list --owner [owner]` to see available projects if needed

## Phase 9: Generate and Create Issue

1. **Validate Version One Final Time**: Before creating the issue, validate the version number:
   ```
   Pattern: ^v?([0-9]+)\.([0-9]+)\.([0-9]+)$
   - Strip optional 'v' prefix
   - Ensure each component is numeric
   - Ensure no leading zeros (except 0 itself)
   ```

2. **Fill in the template** with all gathered information:
   - Replace `[X.Y.Z]` with the validated version number
   - Replace `[Feature (Minor) / Bug Fix (Patch) / Breaking Change (Major)]` with the change type
   - Fill in the version impact explanation
   - Ensure version badge shows correct version
   - Add version label to the labels list

3. **Create a complete, formatted user story document**

4. **Create the GitHub issue**:
   ```bash
   gh issue create --repo [REPO] --title "[User Story Title]" --body-file [temp-file-with-content] --label "user-story,bdd,v[X.Y.Z],[other-labels]"
   ```

5. **Add the created issue to the GitHub Project**:
   ```bash
   # Get the issue number from creation output
   gh project item-add [PROJECT_NUMBER] --owner [OWNER] --url [ISSUE_URL]
   ```

## Phase 10: Confirmation

Display to the user:
- Link to the created issue
- Version information (version number and change type)
- Confirmation that it was added to the project
- Summary of the user story with key scenarios
- Version badge for easy reference

## Important Notes:

- **Ask questions progressively** - don't overwhelm with all questions at once
- **Enforce semver validation** - strictly validate version format (X.Y.Z) before proceeding
- **Validate Gherkin syntax** - ensure Given/When/Then structure is correct
- **Be specific** - avoid vague placeholders; gather concrete details
- **Consider testability** - scenarios should be clear enough to write automated tests
- **Think edge cases** - push for error scenarios and boundary conditions
- **Use proper labels** - always include `user-story`, `bdd`, and `v[X.Y.Z]` labels
- **Verify project access** - confirm the user has access to the specified GitHub Project
- **Version consistency** - ensure version appears in template body, badge, and labels

## GitHub CLI Commands Reference:

```bash
# List available projects
gh project list --owner [OWNER]

# View project details
gh project view [NUMBER] --owner [OWNER]

# Create issue
gh issue create --repo [OWNER/REPO] --title "TITLE" --body "BODY" --label "label1,label2"

# Add issue to project
gh project item-add [PROJECT_NUMBER] --owner [OWNER] --url [ISSUE_URL]
```

Begin by loading the template and asking the first set of questions about the story overview.