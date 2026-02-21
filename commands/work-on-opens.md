# Work on Open Issues - Priority Board Epic Resolution

Iterate through a GitHub Projects priority board, resolve epics in priority order by working sub-issues in parallel, and create PRs for each.

## Input Parameters

<project_board>
$ARGUMENTS
</project_board>

## Instructions

You are an AI assistant that processes a GitHub Projects priority board end-to-end. You work through epics by priority, clarify third-party integration needs with the user, resolve sub-issues in parallel using git worktrees, and create PRs via the `/pr` command.

---

### Phase 1: Board Discovery & Epic Prioritization

1. **Fetch the project board** to get all epics ordered by priority:

   ```bash
   # List project items sorted by priority
   gh project item-list <PROJECT_NUMBER> --owner <OWNER> --format json
   ```

   If the user provided a board URL, parse the owner and project number from it.
   If the user provided an epic URL directly, treat it as a single-epic run.

2. **Build the priority queue** of epics:
   - Filter to only OPEN epics/issues
   - Respect the board's priority column ordering (P0 > P1 > P2, or Top > High > Medium > Low, etc.)
   - Present the ordered list to the user:

   ```
   Priority Board: <project_name>

   Epics to process (by priority):
     P0: #<num> - <title> (X open sub-issues)
     P0: #<num> - <title> (X open sub-issues)
     P1: #<num> - <title> (X open sub-issues)
     P2: #<num> - <title> (X open sub-issues)
     ...
   ```

3. **Confirm with the user** before starting:
   Use the `AskUserQuestion` tool:
   - "Ready to start working through X epics in priority order. Proceed with all, or select specific epics?"
   - Options: "Proceed with all", "Let me pick specific epics", "Start from epic #..."

---

### Phase 2: Epic Pre-Flight - Third-Party Clarification

**Before working on each epic**, analyze it for third-party integration needs.

1. **Scan the epic and its sub-issues** for third-party service references:
   - Payment processing (Stripe, PayPal, Square, etc.)
   - Notifications (Google Push, Firebase, APNs, SendGrid, Twilio, etc.)
   - Auth providers (Auth0, Okta, Firebase Auth, etc.)
   - Storage (AWS S3, Cloudinary, etc.)
   - Maps/Location (Google Maps, Mapbox, etc.)
   - Analytics (Segment, Mixpanel, etc.)
   - Any other external API or SDK

2. **If third-party integrations are detected**, use `AskUserQuestion` to clarify:

   Example questions:
   - "Epic #<num> involves payment processing. Which provider should we use?"
     - Options: "Stripe (Recommended)", "PayPal", "Square"
   - "Epic #<num> needs push notifications. Which service?"
     - Options: "Google FCM (Recommended)", "Apple APNs", "OneSignal"
   - "Epic #<num> references email sending. Which provider?"
     - Options: "SendGrid (Recommended)", "Resend", "AWS SES"

   Collect all answers before starting implementation. Store these decisions for use during `/task` execution.

3. **If no third-party needs are detected**, proceed directly to sub-issue resolution.

---

### Phase 3: Sub-Issue Analysis & Parallel Execution Plan

For the current epic:

1. **Extract all sub-issues** from the epic body:
   ```bash
   gh issue view <EPIC_NUMBER> --json body,title -q .body
   ```
   Parse task lists: `- [ ] #123`, `- [ ] https://github.com/.../issues/123`

2. **Fetch each sub-issue** and filter to OPEN only:
   ```bash
   gh issue view <SUB_ISSUE_NUMBER> --json state,title,body,labels,number
   ```

3. **Build a dependency graph**:
   - Parse each sub-issue for: "Depends on #X", "Blocked by #X", dependency sections
   - Use the epic's task breakdown table if it has dependency info
   - Group sub-issues into **parallelizable tiers**:

   ```
   Tier 0 (no deps, run in parallel):  #10, #11, #12
   Tier 1 (depends on Tier 0):         #13 (needs #10), #14 (needs #11)
   Tier 2 (depends on Tier 1):         #15 (needs #13, #14)
   ```

4. **Set up git worktrees** for parallel execution:
   ```bash
   # Create worktree directory
   mkdir -p .worktrees

   # For each parallel sub-issue, create a worktree
   git worktree add .worktrees/issue-<NUMBER> -b issue-<NUMBER> <BASE_BRANCH>
   ```

   This allows working on multiple features that may touch the same files simultaneously without conflicts.

---

### Phase 4: Parallel Sub-Issue Resolution

Process each tier of sub-issues:

#### For each tier (starting from Tier 0):

**4.1: Launch parallel work on all sub-issues in the current tier**

For each sub-issue in the tier, working from its dedicated worktree:

1. **Determine base branch**:
   - Tier 0 issues: base = `main` (or repo default branch)
   - Other tiers: base = the feature branch of the dependency issue

2. **Create the feature branch** in the worktree:
   ```bash
   cd .worktrees/issue-<NUMBER>
   git checkout -b issue-<NUMBER> <base_branch>
   ```

3. **Run `/task` to resolve the sub-issue**:
   Use the `/task` command with the sub-issue GitHub URL:
   ```
   /task <SUB_ISSUE_GH_URL>
   ```

   Pass along any third-party decisions collected in Phase 2 as context.

   The task command will:
   - Analyze the issue requirements
   - Implement the solution using appropriate specialist agents
   - Run tests and quality checks
   - Commit all changes to the feature branch

4. **Run tasks in parallel** using the Task tool with `run_in_background: true` for independent sub-issues within the same tier. Monitor progress and wait for all to complete before moving to the next tier.

**4.2: Wait for the entire tier to complete**

- Monitor all running background tasks
- Report progress as each sub-issue completes:
  ```
  Tier 0 progress: 2/3 complete
    [DONE] #10 - <title>
    [DONE] #11 - <title>
    [WORKING] #12 - <title>
  ```

**4.3: Create PRs for completed sub-issues**

Once a sub-issue's task is done, create its PR using the `/pr` command:

```
/pr --source-branch=issue-<NUMBER> --target-branch=<base_branch> --related-issues=<NUMBER>
```

The PR must:
- Target the dependency branch (or `main` for Tier 0)
- Reference the parent epic: "Part of #<EPIC_NUMBER>"
- Link the sub-issue: "Closes #<SUB_ISSUE_NUMBER>"
- Include labels from the sub-issue

**4.4: Move to the next tier**

- Ensure all dependency branches are pushed to remote
- Create worktrees for the next tier's sub-issues, branching from the appropriate dependency branches
- Repeat from 4.1

---

### Phase 5: Epic Completion & Cleanup

After all sub-issues in the epic are resolved:

1. **Clean up worktrees**:
   ```bash
   git worktree remove .worktrees/issue-<NUMBER>
   ```
   Remove the `.worktrees` directory when empty.

2. **Update the epic issue**:
   - Edit the epic body to check off completed sub-issues
   - Add a completion comment with the summary

3. **Present the epic summary**:
   ```
   Epic #<EPIC_NUMBER>: <title> - COMPLETE

   Sub-issues resolved: X/Y
   PRs created:

   Tier 0 (parallel):
     #10 → PR #<PR> (target: main)
     #11 → PR #<PR> (target: main)
     #12 → PR #<PR> (target: main)

   Tier 1 (after Tier 0):
     #13 → PR #<PR> (target: issue-10)
     #14 → PR #<PR> (target: issue-11)

   Tier 2 (after Tier 1):
     #15 → PR #<PR> (target: issue-13)

   Recommended merge order:
     1. Merge Tier 0 PRs into main
     2. Rebase Tier 1 branches onto main, then merge
     3. Rebase Tier 2 branches onto main, then merge
   ```

---

### Phase 6: Move to Next Epic

1. **Check if there are more epics** in the priority queue
2. **Report overall progress**:
   ```
   Board Progress: X/Y epics complete
   Completed: #<num> (P0), #<num> (P0)
   Next: #<num> - <title> (P1, X sub-issues)
   ```
3. **Use `AskUserQuestion`** to confirm continuing:
   - "Epic #<num> complete. Continue to next epic #<num> - <title>?"
   - Options: "Continue", "Skip to next priority", "Stop here"
4. **Loop back to Phase 2** for the next epic

---

### Phase 7: Board Completion Summary

After all epics are processed:

```
Priority Board Complete!

Board: <project_name>
Epics Processed: X/Y
Total Sub-Issues Resolved: N
Total PRs Created: M

By Priority:
  P0: X epics (N sub-issues, M PRs)
  P1: X epics (N sub-issues, M PRs)
  P2: X epics (N sub-issues, M PRs)

Third-Party Integrations Used:
  - Stripe (payment) in Epic #<num>
  - Google FCM (notifications) in Epic #<num>

All PRs are ready for review and merge.
```

---

## Error Handling

- **If `/task` fails on a sub-issue:** Log the error, use `AskUserQuestion` to ask "Sub-issue #X failed. Skip and continue, retry, or abort epic?"
- **If `/pr` creation fails:** Retry once. If it fails again, log and continue to the next sub-issue.
- **If a dependency sub-issue failed:** Skip dependent sub-issues in later tiers, notify the user.
- **If merge conflicts arise in a worktree:** Pause that sub-issue, alert the user with `AskUserQuestion` for manual resolution guidance.
- **If git worktree creation fails:** Fall back to sequential branch-switching mode for that sub-issue.
- **If the user interrupts:** Save progress state and present a resume summary so they can restart with `/work-on-opens` later.

## Important Notes

- Always respect the priority board ordering - P0 epics before P1, etc.
- Use `AskUserQuestion` proactively for ANY third-party/external service decisions before implementing.
- Git worktrees enable true parallel work on sub-issues touching the same files without conflicts.
- Each sub-issue gets its own feature branch and PR - never bundle multiple sub-issues into one PR.
- Dependency sub-issues must complete before their dependents can start (tier-based execution).
- After merging Tier 0 PRs to main, subsequent tier PRs should be rebased onto main before merge.
