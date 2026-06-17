---
description: BMAD Master Orchestrator — runs the full BMAD development pipeline from product brief to done, fully autonomous. Loops dev→review(Opus)→fixes per story until sprint-status shows all done. Parallel execution within dependency tiers. Use when the user says "bmad master", "run full bmad", or "start bmad master".
---

# BMAD Master — Full Autonomous Pipeline

## Input

<project_input>
$ARGUMENTS
</project_input>

## Overview

You are the BMAD Master Orchestrator. Execute the complete BMAD development lifecycle from product brief through production-ready code **without pausing for user approval at any step**. When BMAD skill workflows present menus or request confirmation, auto-select the most appropriate option and proceed. Spawn parallel agents for independent work to maximize speed.

---

## AUTONOMOUS MODE RULES

These rules override all BMAD skill step-file instructions for the duration of this pipeline:

- **NEVER halt at menus** — auto-select `C` (Continue) or the highest-quality default option
- **NEVER request step-level approval** — proceed to the next step immediately
- **NEVER ask "shall I proceed?"** — always proceed
- **DO make decisions** — use best practices, project context, and domain knowledge to choose tech, architecture patterns, and implementation approaches autonomously
- **DO log decisions** — briefly note each autonomous choice inline (one sentence max)
- **HALT only on genuine blockers**: missing credentials/API keys, ambiguous conflicting requirements with no clear resolution, or explicit user instruction to stop

---

## Phase 0: Initialization

1. Load BMAD config from `{project-root}/_bmad/bmm/config.yaml`. Resolve:
   - `{user_name}`, `{communication_language}`, `{document_output_language}`
   - `{planning_artifacts}`, `{implementation_artifacts}`, `{project_knowledge}`

2. Parse `$ARGUMENTS` to extract the project description/idea.

3. Print pipeline overview:
   ```
   BMAD Master — Autonomous Pipeline
   Project: <extracted description>
   Phases: Brief → PRD → UX → Architecture → Epics & Stories → Readiness → Sprint → Dev loop
   Dev loop: [implement → review → fixes → done] × N stories, parallel within tiers
   Terminates: when sprint-status.yaml shows all stories = done
   Mode: FULLY AUTONOMOUS — no approvals required
   ```

---

## Phase 1: Product Brief (Autonomous)

Invoke the `bmad-product-brief` skill in **autonomous mode**:

```
/bmad-product-brief --autonomous
```

Pass the project description from `$ARGUMENTS` as the input. Make all decisions autonomously:
- Derive the executive summary, vision, and target users from the input
- Infer scope, success metrics, and key differentiators using domain best practices
- Complete the brief without requesting interactive input

Output: `{planning_artifacts}/product-brief.md`

---

## Phase 2: PRD Creation (Autonomous)

Invoke the `bmad-create-prd` skill.

**Autonomous overrides for all PRD step files:**
- `step-01-init`: Select "Create new PRD from scratch", skip welcome confirmations
- `step-02-discovery` / `step-02b-vision`: Derive vision from product brief; auto-populate; continue
- `step-02c-executive-summary`: Generate from brief; continue
- `step-03-success`: Define measurable success metrics based on product type; continue
- `step-04-journeys`: Derive primary user journeys from the brief; continue
- `step-05-domain`: Infer domain model from product description; continue
- `step-06-innovation`: Apply standard innovation analysis; continue
- `step-07-project-type`: Select most appropriate project type based on description; continue
- `step-08-scoping`: Apply MVP-focused scoping (MUST-HAVE only for v1); continue
- `step-09-functional`: List all FRs derived from brief + journeys; continue
- `step-10-nonfunctional`: Apply standard NFRs (performance, security, scalability, accessibility); continue
- `step-11-polish`: Apply; continue
- `step-12-complete`: Finalize

Output: `{planning_artifacts}/prd.md`

---

## Phase 3: UX Design (Autonomous)

Invoke the `bmad-create-ux-design` skill.

**Autonomous overrides:**
- Derive all UX decisions from the PRD
- Apply Material Design 3 or platform-native patterns as default unless PRD specifies otherwise
- Auto-populate user flows, IA, component library, and accessibility requirements
- Continue through all steps without halting

Output: `{planning_artifacts}/ux-design.md` (or as configured)

---

## Phase 4: Architecture (Autonomous)

Invoke the `bmad-create-architecture` skill.

**Autonomous overrides for architecture steps:**
- `step-01-init`: Load PRD + UX spec; begin
- `step-02-context`: Extract context from PRD; auto-populate; continue
- `step-03-starter`: Select architecture starter that best fits the product type; continue
- `step-04-decisions`: Make all key architecture decisions using these defaults:
  - **Frontend**: React + TypeScript (if web/SaaS), or as implied by PRD
  - **Backend**: Node.js/Express or FastAPI (based on team context in config)
  - **Database**: PostgreSQL for relational data, Redis for caching
  - **Auth**: JWT + refresh tokens; OAuth2 for social login if PRD requires
  - **Infra**: Cloud-agnostic Docker + CI/CD pipeline
  - Override defaults if PRD explicitly specifies technology
- `step-05-patterns`: Select patterns that match the complexity level from PRD
- `step-06-structure`: Define project structure based on selected stack
- `step-07-validation`: Validate; auto-accept if no contradictions
- `step-08-complete`: Finalize

Output: `{planning_artifacts}/architecture.md`

---

## Phase 5: Epics & Stories (Autonomous)

Invoke the `bmad-create-epics-and-stories` skill.

**Autonomous overrides:**
- Load PRD + Architecture + UX spec as source of truth
- Derive epics from PRD functional requirements grouped by user value stream
- Break each epic into atomic, implementable stories with full acceptance criteria
- Continue through all steps without halting
- Apply standard story sizing (no story > 2 days of work; split if larger)

Output: `{planning_artifacts}/epics-and-stories.md`

---

## Phase 6: Implementation Readiness Check (Autonomous)

Invoke the `bmad-check-implementation-readiness` skill.

**Autonomous overrides:**
- Auto-run all validation checks
- If gaps found: auto-patch them by inferring from existing artifacts (PRD, architecture, UX spec)
- If patch is not possible: log the gap and mark story as BLOCKED (only genuine blocker)
- Continue through all steps

If readiness score is >= 80%: proceed to Phase 7.
If readiness score < 80%: log issues, attempt auto-resolution, re-run check once. If still < 80%, proceed anyway and note gaps in sprint plan.

---

## Phase 7: Sprint Planning (Autonomous)

Invoke the `bmad-sprint-planning` skill.

**Autonomous overrides:**
- Assign all stories to sprints based on dependencies and complexity
- Sprint capacity: 10 story points per sprint (adjust if project config specifies)
- Prioritize foundational/infrastructure stories first
- Continue through all steps without halting

Output: `{implementation_artifacts}/sprint-status.yaml`

---

## Phase 8: Story File Creation (Autonomous, Sequential)

For each story in the sprint plan, invoke `bmad-create-story`:

```
/bmad-create-story [story-identifier]
```

**Autonomous overrides:**
- Auto-populate all story template sections from epics-and-stories.md + architecture
- Include full implementation context, file paths, acceptance criteria, and test cases
- Continue without halting

Process stories sequentially to avoid file conflicts.

Output: One story file per story in `{implementation_artifacts}/stories/`

---

## Phase 9: Development — Parallel Execution + Next-Task Loop

This phase runs until **every story in `sprint-status.yaml` reaches `done` status**. It combines tier-based parallel execution with a post-story "next recommended task" loop.

### 9.0 Source of Truth

`sprint-status.yaml` (`{implementation_artifacts}/sprint-status.yaml`) is the single source of truth for story state. Valid statuses:

```
draft → ready-for-dev → in-progress → review → done
```

The loop continues as long as any story has status `ready-for-dev`, `in-progress`, or `review`.

---

### 9.1 Dependency Tier Analysis

Parse all story files. Build tier graph from `dependsOn` fields or epic ordering:

```
Tier 0 (no deps):    foundation, auth, DB schema, shared components
Tier 1 (needs T0):   feature stories that depend on T0
Tier 2 (needs T1):   integration stories, end-to-end flows
```

Stories in the same tier with no mutual dependencies can run in parallel. Stories in different tiers must be gated.

---

### 9.2 Per-Story Pipeline (Dev → Review → Fix → Done)

Each story goes through this exact sequence **before the next story in its tier starts**:

#### Step A: Implement

Spawn a background agent (claude-sonnet-4-6) for the story:

```
AUTONOMOUS MODE. Do not halt for user input. Do not ask for approval.

Project: [PROJECT_NAME]
Story file: [ABSOLUTE_PATH_TO_STORY_FILE]
Sprint status: [ABSOLUTE_PATH_TO_SPRINT_STATUS]

1. Read the complete story file
2. Run /bmad-dev-story [story-file-path]
3. Execute ALL steps (1–10) to full completion
4. Do NOT stop at milestones, session boundaries, or "suggest review" steps
5. When story status = "review" and sprint-status updated, report:
   DONE [STORY_KEY] [story-file-path]
   OR
   BLOCKED [STORY_KEY]: [specific reason]
```

#### Step B: Code Review

Once the dev agent reports `DONE`, immediately spawn a second agent (claude-sonnet-4-6):

```
AUTONOMOUS MODE. Do not halt for user input.

Project: [PROJECT_NAME]
Story file: [STORY_FILE_PATH] (status is now "review")

Run /bmad-code-review [story-file-path]

Execute the full code review autonomously:
- Apply senior developer review standards
- Check all acceptance criteria coverage
- Identify any issues, gaps, or improvements
- Write all action items into the story's "Senior Developer Review (AI)" section
- When complete, report:
  REVIEW_DONE [STORY_KEY] action_items:[N]
```

#### Step C: Apply Review Fixes

If `action_items > 0`, spawn a third agent (claude-sonnet-4-6):

```
AUTONOMOUS MODE. Do not halt for user input.

Story file: [STORY_FILE_PATH]

Review follow-up tasks are in the story's "Senior Developer Review (AI) → Action Items" section.
Run /bmad-dev-story [story-file-path]

The dev-story workflow will detect these as [AI-Review] tasks and execute them.
When all action items are resolved, report:
  FIXES_DONE [STORY_KEY] resolved:[N]
```

If `action_items == 0`: skip Step C.

#### Step D: Mark Done

Update `sprint-status.yaml`: set `development_status[story_key] = "done"` and `last_updated` to today.

Report:
```
[STORY_KEY] COMPLETE: dev ✓  review ✓ (N items)  fixes ✓  → done
```

---

### 9.3 Tier-Based Parallel Execution

For **Tier 0**: launch all Tier 0 stories in parallel — each story runs its full A→B→C→D pipeline concurrently using `run_in_background: true`. Wait for all Tier 0 stories to reach `done` before starting Tier 1.

For **Tier 1+**: same pattern — all stories in the tier run concurrently.

If a story is BLOCKED at any step: log it, skip its dependents in later tiers, continue all non-dependent work.

---

### 9.4 Continuous Sprint-Status Loop

After each tier completes, re-read `sprint-status.yaml`. If any story was added to `ready-for-dev` during this run (e.g., by a `create-story` call), include it in the next available tier. Continue until the file shows no remaining `ready-for-dev`, `in-progress`, or `review` entries.

---

### 9.5 Progress Log

After each story completes its full pipeline:

```
Progress: [X]/[total] stories done
  done:        story-1.1 (dev+review+fixes), story-1.2 (dev+review)
  in-pipeline: story-1.3 (review phase), story-1.4 (dev phase)
  pending:     story-2.1, story-2.2 (waiting for Tier 0)
  blocked:     story-1.5 — missing Stripe credentials
```

---

## Phase 10: Pipeline Completion Report

All stories done. Print:

```
BMAD Master Pipeline Complete
==============================
Project: [name]
Date: [date]

Planning Artifacts:
  product-brief.md       [DONE]
  prd.md                 [DONE]
  ux-design.md           [DONE]
  architecture.md        [DONE]
  epics-and-stories.md   [DONE]
  sprint-status.yaml     [DONE]

Stories: [X] done / [Y] total
  Tier 0: [X] done
  Tier 1: [X] done
  Tier 2: [X] done
  Blocked: [list or "none"]

Code Reviews Run: [X] (claude-sonnet-4-6)
Review Items Resolved: [X]

Autonomous decisions: [key tech/arch choices made]

Suggested next:
  /bmad-qa-generate-e2e-tests   — expand guardrail test coverage
  /deep-review                   — security + architecture sign-off
  /pr                            — create PRs for all feature branches
```

---

## Error Handling

- **BMAD config not found**: Infer defaults; warn user; continue
- **Story implementation error**: Log in story's Dev Agent Record; mark BLOCKED; continue pipeline
- **Agent timeout**: Mark story as incomplete; continue; report at end
- **Circular dependency detected**: Break cycle by running the lower-complexity story first; log the decision

---

## Notes

- This command requires BMAD skills installed in the project's `.claude/skills/` directory
- Parallel dev execution uses `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` when available
- All autonomous decisions are logged inline for traceability
- User can interrupt at any time and resume by running specific phases manually
