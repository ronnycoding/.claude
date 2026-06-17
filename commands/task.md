---
description: Resolve a GitHub issue end-to-end by decomposing it, dispatching specialist subagents in parallel dependency tiers, integrating, and opening a PR.
argument-hint: <issue-number | issue-url | short description>
---

# Task Resolution with Agent Orchestration

You are an AI assistant that resolves a GitHub issue from analysis through merged PR. You decompose the work, dispatch specialist **subagents** (via the Task tool) in parallel within dependency tiers, integrate their output, verify it, and hand off to `/pr`. All progress is tracked in your todo list and mirrored to the parent issue description.

## Input

<task_target>
$ARGUMENTS
</task_target>

`$ARGUMENTS` is normally a GitHub issue number or URL. If it is a free-text description instead, ask whether to create an issue first via `/issue`, or proceed without one (no issue tracking, PR only).

---

## Operating Rules

- **Use real tooling only:** `gh` CLI for GitHub, `git` (+ worktrees) for branches, the **Task tool** to spawn subagents, `TodoWrite` for tracking. There is no `claude task`/`claude agent`/`claude todos` CLI — never invent commands.
- **Progress tracking is single-source:** mirror status by **editing the parent issue description** (checkboxes in its task list), per `CLAUDE.md`. Do **not** post status updates as issue comments.
- **Parallelism:** dispatch independent subagents in a **single message with multiple Task calls** so they run concurrently. Only parallelize within a dependency tier.
- **File-conflict isolation:** when multiple agents in the same tier touch the same files, give each its own `git worktree` (see `/work-on-opens` for the pattern) and merge results back.
- **Agent selection:** match subtasks to specialists from `~/.claude/agents/` (e.g. `backend-architect`, `frontend-developer`, `test-automator`, `code-reviewer`, `security-auditor`, `database-optimizer`, `docs-architect`, `debugger`). Use `general-purpose` only when no specialist fits.
- **Skills:** check `~/.claude/skills/` for applicable domain skills and instruct subagents to use them.

---

## Phase 1 — Setup & Issue Registration

```bash
# Resolve the issue (accept number or URL)
gh issue view "$ISSUE_NUMBER" --json title,body,state,labels,assignees,milestone,comments

ISSUE_TITLE=$(gh issue view "$ISSUE_NUMBER" --json title -q .title)
BRANCH_NAME="issue-$ISSUE_NUMBER"

# Branch off the default branch (never commit straight to main)
git switch -c "$BRANCH_NAME"
```

Initialize your **todo list** (`TodoWrite`) with one orchestration item plus a placeholder per anticipated subtask. This is your live working tracker; the issue description is the durable mirror.

## Phase 2 — Analysis & Planning

Read the issue body, comments, and linked items. Then assess:

- **Scope & boundaries** — what is in and out of scope.
- **Acceptance criteria** — extract explicit and implied criteria; if missing, infer and state your assumptions.
- **Complexity** — `simple` (single agent), `medium`, `complex`, or `epic` (recommend splitting via `/issue`).
- **Dependencies & integration points** — what must exist before what.
- **Breaking changes / risks.**

Inspect the repo to ground the plan: `CONTRIBUTING.md`, existing patterns, test/lint/build commands (from `package.json`, `Makefile`, CI config), and recent related PRs (`gh pr list --search`).

For a **simple** issue, skip decomposition and resolve it directly (optionally with one specialist agent), then jump to Phase 5.

## Phase 3 — Decomposition & Dependency Tiers

Break the work into atomic, independently verifiable subtasks. For each, record: a clear description, the specialist agent, acceptance criteria, and its dependencies.

Group subtasks into **dependency tiers** — every subtask in a tier can run in parallel because none depends on another in the same tier:

```
Tier 0 (parallel): schema/migrations, shared types, auth scaffolding
Tier 1 (parallel): feature work depending on Tier 0
Tier 2 (parallel): integration flows, end-to-end wiring depending on Tier 1
```

Mirror this plan into the **parent issue description** as a checklist (one box per subtask). Keep these boxes updated as the source of truth for progress.

## Phase 4 — Parallel Execution by Tier

For each tier, in order, launch all its subagents **in one message** (multiple Task calls). Give each subagent a self-contained prompt:

- The specific subtask, its acceptance criteria, and relevant files/paths.
- Applicable skills to load and conventions to follow.
- A directive to **return a concise report**: what changed, files touched, how to verify, and any interface changes downstream tiers must know about.
- If files may collide with a sibling agent, instruct it to work in its assigned `git worktree`.

After a tier completes:
1. Integrate/merge each agent's output (resolve worktree merges, reconcile interface changes).
2. Run the project's **lint, type-check, and build** to confirm the tier is green before starting the next.
3. Check off the corresponding boxes in the parent issue description and update your todo list.
4. If an agent is blocked (missing credentials, contradictory requirements), log the blocker in the subtask, skip it, and continue; surface it in the final summary.

## Phase 5 — Integration, Testing & Quality

- Run the **full test suite**; add tests where coverage gaps map to acceptance criteria.
- Validate against every acceptance criterion explicitly.
- Run linting, type-checks, security/secret scans, and the build.
- For non-trivial changes, dispatch a `code-reviewer` (and `security-auditor` when relevant) subagent over the diff and address findings.
- Report results honestly — if tests fail or a step was skipped, say so with the output.

## Phase 6 — Commit & PR

```bash
git add -A
git commit -m "fix: #$ISSUE_NUMBER - $ISSUE_TITLE"   # use the repo's commit convention
git push -u origin "$BRANCH_NAME"
```

Then create the PR by invoking the **`/pr`** command (it detects PR templates and repo conventions). Ensure the PR body links the issue with a closing keyword (`Closes #$ISSUE_NUMBER`) so merge auto-closes it.

```bash
PR_NUMBER=$(gh pr view --json number -q .number)
```

Update the parent issue description: all subtask boxes checked, PR linked.

## Phase 7 — Review & Completion

- Monitor checks and review: `gh pr view "$PR_NUMBER" --json reviews,statusCheckRollup`.
- Address review feedback (re-dispatch the relevant specialist agent for substantive changes).
- After approval and green checks, merge per repo policy: `gh pr merge "$PR_NUMBER" --squash` (only if the user wants you to merge).
- Final summary to the user: what shipped, what was skipped/blocked and why, and verification status.

---

## Quick Reference (real commands)

```bash
# Issue context
gh issue view <n> --json title,body,labels,comments
gh issue list --label "<label>" --limit 10
gh pr list --search "<title>" --state all          # find prior art

# Branching / isolation
git switch -c issue-<n>
git worktree add ../wt-<subtask> -b issue-<n>-<subtask>   # parallel file-isolated work
git worktree remove ../wt-<subtask>

# Verify (use the project's actual scripts)
# e.g. npm test / pnpm lint / make check / pytest

# Handoff
/pr                                                  # create the pull request
gh pr view <pr> --json reviews,statusCheckRollup
```

## Tracking model

- **`TodoWrite`** — your live, in-session working list (orchestration item + one per subtask).
- **Parent issue description checkboxes** — the durable, single source of truth for progress. Edit the description to update; never use comments for status.
- **Subagents** — instruct significant ones to report structured results so you can integrate without re-reading everything.
