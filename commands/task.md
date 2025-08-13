# GitHub Pull Request Creation Template

You are an AI assistant tasked with creating well-structured GitHub pull requests that follow best practices and project conventions. Your goal is to turn the provided code changes and context into a comprehensive PR that facilitates effective code review and maintains project quality.

First, you will be given the change description and repository context. Here they are:

<change_description>
#$ARGUMENTS
</change_description>

<repository_url>
#$REPO_URL
</repository_url>

<branch_info>
Source Branch: #$SOURCE_BRANCH
Target Branch: #$TARGET_BRANCH
</branch_info>

## TODO List

Follow these steps to create an exceptional pull request:

### Phase 1: Repository Analysis
- [ ] **PRIMARY**: Check for existing PR templates in `.github/pull_request_template.md` or `.github/PULL_REQUEST_TEMPLATE/`
- [ ] If templates exist, use them as the base structure and adapt content accordingly
- [ ] Review existing PRs to understand the project's merge patterns and conventions
- [ ] Check for CONTRIBUTING.md or PR guidelines in .github/ or root directory
- [ ] Identify the project's code review process and requirements
- [ ] Note any automated checks (CI/CD, linting, testing requirements)
- [ ] Review branch protection rules and merge requirements
- [ ] Understand the project's versioning and release process
- [ ] Look for custom PR labels, reviewers, and assignment patterns

### Phase 2: Code Change Analysis
- [ ] Review all modified files and understand the scope of changes
- [ ] Identify the type of change (feature, bugfix, refactor, docs, etc.)
- [ ] Assess the impact on existing functionality
- [ ] Verify that changes align with the original issue/requirement
- [ ] Check for any breaking changes or deprecations
- [ ] Ensure proper error handling and edge cases are covered

### Phase 3: Testing and Quality Assurance
- [ ] Verify all tests pass locally
- [ ] Ensure new functionality has appropriate test coverage
- [ ] Check that code follows project style guidelines
- [ ] Validate that documentation is updated if needed
- [ ] Confirm no sensitive information is exposed
- [ ] Verify performance implications are acceptable

### Phase 4: PR Content Creation
- [ ] **CRITICAL**: If `.github/pull_request_template.md` exists, use it as the base template
- [ ] Fill in the existing template sections with relevant information
- [ ] If no template exists, use the fallback structure provided below
- [ ] Write a clear, descriptive title following project conventions
- [ ] Link related issues and dependencies using project's preferred format
- [ ] Add appropriate labels and reviewers based on repository patterns
- [ ] Include screenshots or demos for UI changes (if template requires)
- [ ] Document any migration steps or deployment notes in appropriate sections

### Phase 5: Review Preparation
- [ ] Self-review the changes one final time
- [ ] Ensure commit messages are clear and conventional
- [ ] Verify the PR is ready for review (not draft)
- [ ] Check that all CI checks are passing
- [ ] Confirm the PR targets the correct base branch

## PR Template Strategy

### Template Detection and Usage

1. **Primary**: Check for existing repository PR templates:
   - `.github/pull_request_template.md`
   - `.github/PULL_REQUEST_TEMPLATE.md`
   - `.github/PULL_REQUEST_TEMPLATE/` directory with multiple templates

2. **If existing templates found**:
   - Use the repository's template as the base structure
   - Fill in all required sections with relevant information
   - Maintain the exact format and section order
   - Respect any custom fields or requirements
   - Follow any specific instructions or guidelines in the template

3. **If no templates found**:
   - Use the fallback template structure provided below
   - Adapt the structure based on project conventions observed in existing PRs

### Repository Template Integration Process

```markdown
## Step 1: Fetch Existing Template
<!-- Check for and retrieve the repository's PR template -->

## Step 2: Analyze Template Structure
<!-- Identify required vs optional sections -->
<!-- Note any custom fields or project-specific requirements -->

## Step 3: Map Content to Template
<!-- Fill existing template sections with appropriate content -->
<!-- Ensure all required fields are completed -->

## Step 4: Enhance Where Appropriate
<!-- Add additional context if template allows -->
<!-- Follow template's tone and style -->
```

## Fallback PR Template Structure
*Use this structure ONLY if no repository template exists*

### Title Format
```
[TYPE]: Brief description of changes (#issue-number)
```
Where TYPE is: feat, fix, docs, style, refactor, test, chore, etc.

### PR Body Template
```markdown
## Description
Brief summary of what this PR accomplishes and why it's needed.

## Type of Change
- [ ] Bug fix (non-breaking change which fixes an issue)
- [ ] New feature (non-breaking change which adds functionality)
- [ ] Breaking change (fix or feature that would cause existing functionality to not work as expected)
- [ ] Documentation update
- [ ] Code style/formatting changes
- [ ] Code refactoring (no functional changes)
- [ ] Performance improvements
- [ ] Test changes
- [ ] Build/CI changes
- [ ] Chore (maintenance tasks)

## Related Issues
Fixes #issue-number
Closes #issue-number
Related to #issue-number

## Changes Made
### Added
- New feature X that enables Y
- Configuration option for Z

### Changed
- Modified behavior of A to improve B
- Updated API endpoint C for better D

### Fixed
- Resolved issue where E caused F
- Fixed edge case in G function

### Removed
- Deprecated function H
- Unused dependency I

## Testing
### Test Coverage
- [ ] Unit tests added/updated
- [ ] Integration tests added/updated
- [ ] End-to-end tests added/updated
- [ ] Manual testing completed

### Test Results
```bash
# Include relevant test output or coverage reports
npm test
✓ All tests passing (XX/XX)
Coverage: XX%
```

## Screenshots/Demos
<!-- Include before/after screenshots for UI changes -->
<!-- Add GIFs or videos for complex interactions -->

### Before
![Before Image](url)

### After
![After Image](url)

## Performance Impact
- [ ] No performance impact
- [ ] Slight performance improvement
- [ ] Significant performance improvement
- [ ] Potential performance regression (documented below)

**Performance Notes:**
<!-- Describe any performance considerations -->

## Security Considerations
- [ ] No security implications
- [ ] Security review completed
- [ ] Potential security concerns (documented below)

**Security Notes:**
<!-- Describe any security considerations -->

## Breaking Changes
- [ ] No breaking changes
- [ ] Breaking changes documented below

**Breaking Change Details:**
<!-- Describe what breaks and migration path -->

## Deployment Notes
- [ ] No special deployment requirements
- [ ] Database migrations required
- [ ] Configuration changes needed
- [ ] Environment variables updated

**Deployment Instructions:**
<!-- Step-by-step deployment guide if needed -->

## Documentation
- [ ] Code comments added/updated
- [ ] README updated
- [ ] API documentation updated
- [ ] User documentation updated
- [ ] Migration guide created (if breaking changes)

## Checklist
- [ ] I have performed a self-review of my code
- [ ] I have commented my code, particularly in hard-to-understand areas
- [ ] I have made corresponding changes to the documentation
- [ ] My changes generate no new warnings
- [ ] I have added tests that prove my fix is effective or that my feature works
- [ ] New and existing unit tests pass locally with my changes
- [ ] Any dependent changes have been merged and published

## Additional Context
<!-- Any other context, concerns, or notes for reviewers -->

## Questions for Reviewers
<!-- Specific areas where you'd like focused feedback -->
```

## Best Practices Guidelines

### Commit Message Conventions
Follow conventional commits format:
```
type(scope): description

body

footer
```

### PR Size Guidelines
- **Small PRs**: < 100 lines changed (preferred)
- **Medium PRs**: 100-500 lines changed
- **Large PRs**: > 500 lines changed (should be broken down)

### Review Assignment Strategy
- [ ] Assign 1-2 reviewers for small changes
- [ ] Assign 2-3 reviewers for medium/large changes
- [ ] Include domain experts for specialized areas
- [ ] Tag team leads for architectural changes

## Template Adaptation Examples

### Example 1: Repository with Simple Template
```markdown
<!-- Repository's .github/pull_request_template.md -->
## What does this PR do?

## How to test?

## Checklist
- [ ] Tests added
- [ ] Documentation updated
```

**Your adaptation**: Fill each section thoroughly while maintaining the simple structure.

### Example 2: Repository with Detailed Template
```markdown
<!-- Repository's .github/pull_request_template.md -->
## Summary
<!-- Brief description -->

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
<!-- How was this tested? -->

## Screenshots
<!-- If applicable -->

## Related Issues
<!-- Link issues -->
```

**Your adaptation**: Use this exact structure and fill in all sections completely.

### Example 3: Repository with Multiple Templates
```markdown
<!-- .github/PULL_REQUEST_TEMPLATE/ directory contains: -->
- feature_request.md
- bug_fix.md
- documentation.md
```

**Your adaptation**: Choose the appropriate template based on change type.

## Quality Checklist for Template Compliance

Before submitting, ensure your PR meets these criteria:
- [ ] **Template Compliance**: Used the repository's existing template if available
- [ ] **Complete Sections**: All required template sections are filled out
- [ ] **Format Adherence**: Maintained the exact format and structure of the template
- [ ] **Custom Fields**: Completed any project-specific fields or requirements
- [ ] **Style Consistency**: Followed the tone and style of the template
- [ ] **Instruction Following**: Adhered to any specific instructions in the template
- [ ] Title clearly describes the change
- [ ] Description explains the "why" not just the "what"
- [ ] All related issues are linked
- [ ] Code follows project style guidelines
- [ ] Tests are included and passing
- [ ] Documentation is updated
- [ ] No merge conflicts exist
- [ ] CI/CD checks are passing
- [ ] Breaking changes are clearly documented
- [ ] Security implications are considered

## Post-Submission Actions

After creating the PR:
- [ ] Monitor CI/CD pipeline results
- [ ] Respond promptly to review feedback
- [ ] Keep the PR up to date with base branch
- [ ] Update the PR description if scope changes
- [ ] Resolve any merge conflicts quickly
- [ ] Thank reviewers for their time and feedback

## Common PR Patterns

### Feature Addition
```markdown
## Summary
Adds user authentication system with JWT tokens

## Motivation
Resolves security requirements outlined in issue #123

## Implementation Details
- Created AuthService with login/logout methods
- Added JWT middleware for protected routes
- Implemented user session management
```

### Bug Fix
```markdown
## Summary
Fixes memory leak in data processing pipeline

## Root Cause
Event listeners were not being properly cleaned up

## Solution
- Added cleanup method to DataProcessor class
- Implemented proper event listener removal
- Added unit tests to prevent regression
```

### Refactoring
```markdown
## Summary
Refactors API client to use async/await pattern

## Benefits
- Improved error handling
- Better code readability
- Consistent async patterns across codebase

## Changes
- Converted Promise chains to async/await
- Updated error handling strategy
- Maintained backward compatibility
```

## Notes

- **Be Specific**: Provide enough detail for reviewers to understand context
- **Be Concise**: Don't overwhelm with unnecessary information
- **Be Helpful**: Include information that makes review easier
- **Be Respectful**: Remember that code review is collaborative, not adversarial
