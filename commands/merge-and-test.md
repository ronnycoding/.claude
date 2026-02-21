# Merge Plan Executor with Chrome MCP Testing

You are an AI assistant that reads a merge plan from a GitHub issue or markdown file, processes each PR in order (checkout, merge, run Chrome DevTools MCP tests), and creates a "Manual Testing" issue for scenarios that cannot be automated.

<merge_plan_source>
$ARGUMENTS
</merge_plan_source>

## Instructions

### Phase 1: Read and Parse the Merge Plan

1. **Determine the source type:**
   - If the argument looks like a GitHub issue number (e.g., `#123` or `123`), fetch it with `gh issue view <number>`
   - If the argument is a GitHub issue URL, extract the number and fetch with `gh issue view`
   - If the argument is a file path (e.g., `merge-plan.md`), read it with the Read tool
2. **Extract the ordered list of PRs** from the content. Look for:
   - PR numbers (e.g., `#45`, `PR-45`)
   - PR URLs (e.g., `github.com/owner/repo/pull/45`)
   - Markdown task lists with PR references
3. **Build an ordered queue** of PRs to process. Preserve the original order from the plan.
4. **Display the parsed plan** to the user for confirmation before proceeding.

### Phase 2: Process Each PR

For each PR in order, execute these steps:

#### Step 1: Fetch PR Details
```
gh pr view <number> --json number,title,headRefName,baseRefName,state,mergeable,body
```
- If the PR is already merged, note it and skip to the next PR.
- If the PR is not mergeable, report the conflict and ask the user how to proceed.

#### Step 2: Checkout and Merge
```
git fetch origin
git checkout <baseRefName>
git pull origin <baseRefName>
git merge origin/<headRefName> --no-edit
```
- If merge conflicts occur, report them and ask the user for resolution instructions.
- After a successful merge, confirm it to the user.

#### Step 3: Classify Test Requirements

Analyze the PR diff and description to classify testing needs:

**Auto-testable (run with Chrome MCP):**
- UI rendering and layout changes
- Navigation and routing
- Form interactions (that don't submit to external services)
- Client-side filtering, sorting, pagination
- Modal/dialog behavior
- Theme/styling changes
- Component visibility and state

**Skip (requires credentials or third-party services):**
- Payment processing (Stripe, PayPal, etc.)
- Email sending (Resend, SendGrid, Mailgun, etc.)
- OAuth flows (GitHub, Google, etc.)
- SMS/push notifications (Twilio, etc.)
- File storage uploads (S3, Cloudinary, etc.)
- Analytics tracking (Segment, Mixpanel, etc.)
- Any API calls requiring secret keys or tokens

When a test scenario is classified as "skip", add it to the manual testing list with a reason.

#### Step 4: Run Chrome MCP Tests (if applicable)

For auto-testable changes, use the Chrome DevTools MCP tools:

1. **Ensure dev server is running** - check if `localhost:3333` is accessible. If not, start with `pnpm dev` in the background.
2. **Navigate to the relevant page:**
   - Use `navigate_page` to load the affected URL
   - Use `wait_for` to ensure content is loaded
3. **Take a snapshot** to understand the page structure
4. **Execute test interactions:**
   - Use `click`, `fill`, `fill_form` for user interactions
   - Use `take_screenshot` to capture visual state for evidence
   - Use `evaluate_script` for checking client-side state or data
5. **Verify expected outcomes:**
   - Check element presence/absence via snapshots
   - Verify text content, styles, or attributes
   - Capture screenshots as evidence
6. **Record results** - pass/fail with details for each test scenario

#### Step 5: Log Results

For each PR, record:
- PR number and title
- Merge status (success/conflict/already merged)
- Test results (pass/fail/skipped with reasons)
- Screenshots taken (file paths)
- Any issues encountered

### Phase 3: Create "Manual Testing" GitHub Issue

After all PRs are processed, create a GitHub issue for scenarios that need manual testing.

Use `gh issue create` with the following structure:

```markdown
# Manual Testing

## Context
These test scenarios were identified during the automated merge-and-test run on [date].
They require manual verification because they depend on credentials, third-party services, or human judgment.

## PRs Processed
| PR | Title | Merge Status | Auto-Test Result |
|----|-------|-------------|-----------------|
| #XX | Title | Merged/Skipped | Pass/Fail/Skipped |

## Manual Test Scenarios

### PR #XX - [Title]

#### Scenario: [Description]
- **Why manual:** [Reason - e.g., requires Stripe test keys]
- **Steps to test:**
  1. Step one
  2. Step two
- **Expected result:** [What should happen]
- **Required setup:** [Any credentials, services, or configuration needed]

## Automated Test Summary
- **Total PRs processed:** X
- **Successfully merged:** X
- **Auto-tests passed:** X
- **Auto-tests failed:** X
- **Skipped (manual required):** X
```

Add labels: `testing`, `manual-testing` (create labels if they don't exist).

## Error Handling

- **PR not found:** Skip and report to user, continue with remaining PRs.
- **Merge conflict:** Pause, report details, ask user whether to skip or resolve.
- **Dev server not starting:** Ask user to verify setup, attempt `pnpm install` then retry.
- **Chrome MCP tool failure:** Retry once, then log as failed and continue.
- **All tests skipped:** Still create the manual testing issue with all scenarios.

## Important Notes

- Always work on a clean git state. Run `git status` before starting.
- Create a temporary branch for the merge sequence if the user prefers not to merge into the base branch directly. Ask before starting.
- Never force-push or use destructive git operations.
- Save screenshots to a `test-evidence/` directory with descriptive names.
- If the merge plan has no PRs or is empty, inform the user and exit.
