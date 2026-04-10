---
allowed-tools: Bash(gh pr view:*), Bash(gh pr diff:*), Bash(git log:*), Bash(git diff:*), Bash(git fetch:*), Bash(git status:*), Bash(mkdir:*), Bash(awk:*), Read, Write, Glob, Grep, Task, TaskOutput
argument-hint: <PR_NUMBER_or_URL>
description: Run parallel specialized PR reviews (Opus 4.6 for security/architecture, Sonnet 4.6 for the rest)
model: opus
---

# Deep Review (Hybrid) - Parallel PR Analysis

Launch specialized review agents based on the PR's tech stack, then aggregate and deduplicate all findings.

Uses Opus 4.6 for reasoning-heavy agents (security, architecture, bug-finding) and Sonnet 4.6 for the rest. All models have 1M context windows.

## Arguments

- PR Reference: $ARGUMENTS

---

## Phase 1: Gather PR Context

### Step 1.1: Get PR Metadata

```bash
gh pr view $ARGUMENTS --json number,url,title,body,baseRefName,headRefName,additions,deletions,changedFiles
```

Extract and store:
- `PR_NUMBER`: The PR number
- `PR_TITLE`: The PR title
- `PR_URL`: The PR URL
- `PR_BODY`: The PR description/body text
- `FILES_CHANGED`: Number of files changed
- `ADDITIONS`: Lines added
- `DELETIONS`: Lines deleted
- `TOTAL_CHANGED`: ADDITIONS + DELETIONS

### Step 1.2: Get Full PR Diff with Line Numbers

**Step 1.2a: Fetch raw diff (standalone)**
```bash
gh pr diff $ARGUMENTS
```

**Step 1.2b: Save raw diff to temp file**
Use the Write tool to save the raw diff output to `/tmp/claude/pr_raw_diff.txt`.

**Step 1.2c: Add line numbers (standalone)**
```bash
awk '
/^diff --git/ { file_header = $0; printed_header = 0; next }
/^index |^--- |^\+\+\+ / { next }
/^@@/ {
  plus_pos = index($0, "+")
  rest = substr($0, plus_pos + 1)
  gsub(/[^0-9].*/, "", rest)
  new_line = rest - 1
  if (printed_header == 0) { print file_header; printed_header = 1 }
  print $0
  next
}
/^-/ { printf "     - %s\n", substr($0, 2); next }
/^\+/ { new_line++; printf "%4d + %s\n", new_line, substr($0, 2); next }
{ new_line++; printf "%4d   %s\n", new_line, $0 }
' /tmp/claude/pr_raw_diff.txt
```

Store the entire numbered diff as `DIFF_FULL`.

### Step 1.3: Get List of Changed Files

```bash
gh pr view $ARGUMENTS --json files --jq '.files[].path'
```

Store as `CHANGED_FILES` list.

### Step 1.4: Write Diff Files to Disk

**CRITICAL**: Instead of embedding diffs in agent prompts, write them to files that agents will read.

**Step 1.4a: Create output directory**
```bash
mkdir -p PR_${PR_NUMBER}/reviews PR_${PR_NUMBER}/issues
```

**Step 1.4b: Write full diff to file**
Use the Write tool to save `DIFF_FULL` to `PR_${PR_NUMBER}/diff.txt`.

**Step 1.4c: Write filtered diffs**
Based on detected file types in `CHANGED_FILES`, write filtered diffs to separate files.
Only create a filtered diff file if relevant files exist in the PR.

Each filtered diff runs a standalone `awk` command on `/tmp/claude/pr_raw_diff.txt` and the output is saved via the Write tool to `PR_${PR_NUMBER}/diff_<type>.txt`.

Use exactly these awk scripts — copy them verbatim, do NOT modify or generate alternatives:

**TypeScript/JS** → `diff_typescript.txt`
```bash
awk '
/^diff --git/ { p=0 }
/^diff --git.*\.(ts|tsx|js|jsx)$/ { p=1 }
p==0 { next }
/^diff --git/ { file_header = $0; printed_header = 0; next }
/^index |^--- |^\+\+\+ / { next }
/^@@/ { plus_pos = index($0, "+"); rest = substr($0, plus_pos + 1); gsub(/[^0-9].*/, "", rest); new_line = rest - 1; if (printed_header == 0) { print file_header; printed_header = 1 }; print $0; next }
/^-/ { printf "     - %s\n", substr($0, 2); next }
/^\+/ { new_line++; printf "%4d + %s\n", new_line, substr($0, 2); next }
{ new_line++; printf "%4d   %s\n", new_line, $0 }
' /tmp/claude/pr_raw_diff.txt
```

**Python** → `diff_python.txt`
```bash
awk '
/^diff --git/ { p=0 }
/^diff --git.*\.py$/ { p=1 }
p==0 { next }
/^diff --git/ { file_header = $0; printed_header = 0; next }
/^index |^--- |^\+\+\+ / { next }
/^@@/ { plus_pos = index($0, "+"); rest = substr($0, plus_pos + 1); gsub(/[^0-9].*/, "", rest); new_line = rest - 1; if (printed_header == 0) { print file_header; printed_header = 1 }; print $0; next }
/^-/ { printf "     - %s\n", substr($0, 2); next }
/^\+/ { new_line++; printf "%4d + %s\n", new_line, substr($0, 2); next }
{ new_line++; printf "%4d   %s\n", new_line, $0 }
' /tmp/claude/pr_raw_diff.txt
```

**CSS** → `diff_css.txt`
```bash
awk '
/^diff --git/ { p=0 }
/^diff --git.*\.(css|scss|sass|less)$/ { p=1 }
p==0 { next }
/^diff --git/ { file_header = $0; printed_header = 0; next }
/^index |^--- |^\+\+\+ / { next }
/^@@/ { plus_pos = index($0, "+"); rest = substr($0, plus_pos + 1); gsub(/[^0-9].*/, "", rest); new_line = rest - 1; if (printed_header == 0) { print file_header; printed_header = 1 }; print $0; next }
/^-/ { printf "     - %s\n", substr($0, 2); next }
/^\+/ { new_line++; printf "%4d + %s\n", new_line, substr($0, 2); next }
{ new_line++; printf "%4d   %s\n", new_line, $0 }
' /tmp/claude/pr_raw_diff.txt
```

**Frontend** → `diff_frontend.txt`
```bash
awk '
/^diff --git/ { p=0 }
/^diff --git.*\.(tsx|jsx|html)$/ { p=1 }
p==0 { next }
/^diff --git/ { file_header = $0; printed_header = 0; next }
/^index |^--- |^\+\+\+ / { next }
/^@@/ { plus_pos = index($0, "+"); rest = substr($0, plus_pos + 1); gsub(/[^0-9].*/, "", rest); new_line = rest - 1; if (printed_header == 0) { print file_header; printed_header = 1 }; print $0; next }
/^-/ { printf "     - %s\n", substr($0, 2); next }
/^\+/ { new_line++; printf "%4d + %s\n", new_line, substr($0, 2); next }
{ new_line++; printf "%4d   %s\n", new_line, $0 }
' /tmp/claude/pr_raw_diff.txt
```

**Database** → `diff_database.txt`
```bash
awk '
/^diff --git/ { p=0 }
/^diff --git.*\.(sql|prisma)$/ { p=1 }
p==0 { next }
/^diff --git/ { file_header = $0; printed_header = 0; next }
/^index |^--- |^\+\+\+ / { next }
/^@@/ { plus_pos = index($0, "+"); rest = substr($0, plus_pos + 1); gsub(/[^0-9].*/, "", rest); new_line = rest - 1; if (printed_header == 0) { print file_header; printed_header = 1 }; print $0; next }
/^-/ { printf "     - %s\n", substr($0, 2); next }
/^\+/ { new_line++; printf "%4d + %s\n", new_line, substr($0, 2); next }
{ new_line++; printf "%4d   %s\n", new_line, $0 }
' /tmp/claude/pr_raw_diff.txt
```

**DevOps** → `diff_devops.txt`
```bash
awk '
/^diff --git/ { p=0 }
/^diff --git.*(Dockerfile|docker-compose|\.github)/ { p=1 }
p==0 { next }
/^diff --git/ { file_header = $0; printed_header = 0; next }
/^index |^--- |^\+\+\+ / { next }
/^@@/ { plus_pos = index($0, "+"); rest = substr($0, plus_pos + 1); gsub(/[^0-9].*/, "", rest); new_line = rest - 1; if (printed_header == 0) { print file_header; printed_header = 1 }; print $0; next }
/^-/ { printf "     - %s\n", substr($0, 2); next }
/^\+/ { new_line++; printf "%4d + %s\n", new_line, substr($0, 2); next }
{ new_line++; printf "%4d   %s\n", new_line, $0 }
' /tmp/claude/pr_raw_diff.txt
```

**Backend (everything except frontend/CSS)** → `diff_backend.txt`
```bash
awk '
/^diff --git/ { p=1 }
/^diff --git.*\.(tsx|jsx|html|css|scss|sass|less)$/ { p=0 }
p==0 { next }
/^diff --git/ { file_header = $0; printed_header = 0; next }
/^index |^--- |^\+\+\+ / { next }
/^@@/ { plus_pos = index($0, "+"); rest = substr($0, plus_pos + 1); gsub(/[^0-9].*/, "", rest); new_line = rest - 1; if (printed_header == 0) { print file_header; printed_header = 1 }; print $0; next }
/^-/ { printf "     - %s\n", substr($0, 2); next }
/^\+/ { new_line++; printf "%4d + %s\n", new_line, substr($0, 2); next }
{ new_line++; printf "%4d   %s\n", new_line, $0 }
' /tmp/claude/pr_raw_diff.txt
```

**Diff-to-file mapping for agent prompts:**

| Agent Type | Diff File |
|------------|-----------|
| code-reviewer, silent-failure-hunter, security-auditor, code-architect | `PR_${PR_NUMBER}/context.txt` (falls back to `diff.txt` if Step 1.5 was skipped) |
| Other core agents (code-simplifier, type-design-analyzer, comment-analyzer, pr-test-analyzer, cross-cutting-concerns) | `PR_${PR_NUMBER}/diff.txt` |
| typescript-pro, nodejs-expert | `PR_${PR_NUMBER}/diff_typescript.txt` |
| react-expert, nextjs-developer, tailwind-expert | `PR_${PR_NUMBER}/diff_frontend.txt` |
| python-expert, fastapi-expert, django-developer, flask-expert | `PR_${PR_NUMBER}/diff_python.txt` |
| css-expert | `PR_${PR_NUMBER}/diff_css.txt` |
| postgres-expert, prisma-expert | `PR_${PR_NUMBER}/diff_database.txt` |
| docker-expert, github-actions-expert | `PR_${PR_NUMBER}/diff_devops.txt` |
| rest-expert | `PR_${PR_NUMBER}/diff_backend.txt` |

### Step 1.5: Generate Function-Context Diff

Generates a second diff with full function bodies (`git diff -W`) for agents that need surrounding logic.

**Step 1.5a: Fetch PR head (standalone)**
```bash
git fetch origin pull/${PR_NUMBER}/head
```

If `git fetch` fails (deleted fork, network issue, permissions), skip Step 1.5 entirely. The 4 context agents (code-reviewer, silent-failure-hunter, security-auditor, code-architect) will use `diff.txt` instead of `context.txt`.

**Step 1.5b: Generate function-context diff (standalone)**
```bash
git diff -W origin/${BASE_REF}...FETCH_HEAD
```

`BASE_REF` is the `baseRefName` from Step 1.1. Store raw output as `FUNCCTX_RAW`.

**Step 1.5c: Save raw function-context diff to temp file**
Use the Write tool to save `FUNCCTX_RAW` to `/tmp/claude/pr_funcctx_diff.txt`.

**Step 1.5d: Add line numbers (standalone)**
```bash
awk '
/^diff --git/ { file_header = $0; printed_header = 0; next }
/^index |^--- |^\+\+\+ / { next }
/^@@/ {
  plus_pos = index($0, "+")
  rest = substr($0, plus_pos + 1)
  gsub(/[^0-9].*/, "", rest)
  new_line = rest - 1
  if (printed_header == 0) { print file_header; printed_header = 1 }
  print $0
  next
}
/^-/ { printf "     - %s\n", substr($0, 2); next }
/^\+/ { new_line++; printf "%4d + %s\n", new_line, substr($0, 2); next }
{ new_line++; printf "%4d   %s\n", new_line, $0 }
' /tmp/claude/pr_funcctx_diff.txt
```

Store the entire numbered output as `FUNCCTX_FULL`.

**Step 1.5e: Write function-context diff to file**
Use the Write tool to save `FUNCCTX_FULL` to `PR_${PR_NUMBER}/context.txt`.

---

## Phase 2: Detect Tech Stack

### 2.1: Detect Technologies

Analyze the diff and changed files. Set flags to `true`/`false`:

**Languages**: HAS_TYPESCRIPT, HAS_JAVASCRIPT, HAS_PYTHON, HAS_GO, HAS_RUST, HAS_JAVA, HAS_SQL
**Frontend**: HAS_REACT, HAS_NEXTJS, HAS_VUE, HAS_SVELTE, HAS_CSS, HAS_TAILWIND, HAS_HTML
**Backend**: HAS_NODEJS, HAS_EXPRESS, HAS_FASTAPI, HAS_DJANGO, HAS_FLASK, HAS_GRAPHQL, HAS_REST_API, HAS_OPENAPI
**Database**: HAS_POSTGRES, HAS_PRISMA, HAS_SQLITE, HAS_DATABASE
**Auth**: HAS_AUTH, HAS_JWT, HAS_OAUTH
**Testing**: HAS_TESTS, HAS_PLAYWRIGHT, HAS_CYPRESS, HAS_PYTEST, HAS_JEST
**DevOps**: HAS_DOCKER, HAS_GITHUB_ACTIONS, HAS_CI_CD
**AI/ML**: HAS_LANGCHAIN, HAS_OPENAI, HAS_PANDAS, HAS_NUMPY

### 2.2: Identify Unsupported Tech

Check `CHANGED_FILES` for extensions with NO specialized agent:
`.cu`, `.go`, `.rs`, `.java`, `.kt`, `.swift`, `.c`, `.cpp`, `.h`, `.rb`, `.php`, `.scala`, `.ex`, `.lua`, `.r`, `.R`, `.dart`, `.tf`, etc.

Store: `UNSUPPORTED_TECH_LIST`, `UNSUPPORTED_FILE_COUNT`, `UNSUPPORTED_SUMMARY`

---

## Phase 3: Launch Review Agents

### Step 3.1: Launch ALL Agents in a SINGLE Message

**CRITICAL**: Launch ALL agents (core + tech-specific) in ONE message for maximum parallelism using the Task tool with `run_in_background: true`.

Every agent uses these settings:
- `subagent_type: general-purpose`
- `model`: **per-agent** (see Model column in tables below; all models are 1M context — Opus 4.6 / Sonnet 4.6)
- `max_turns: 20`
- `run_in_background: true`

Every agent prompt follows this template (fill in AGENT_NAME, FOCUS, DIFF_FILE, CATEGORIES, and optionally EXTRA_RULES):

```
You are reviewing PR #${PR_NUMBER}: "${PR_TITLE}"
PR URL: ${PR_URL}
Changed files: ${CHANGED_FILES}

## PR DESCRIPTION
${PR_BODY}

FOCUS: ${FOCUS_DESCRIPTION}

## DIFF
Read the diff from: ${DIFF_FILE}
Use the Read tool to read this file. Do NOT ask for it to be provided inline.

## OUTPUT
Write findings to: PR_${PR_NUMBER}/reviews/${AGENT_NAME}.json

JSON format:
{
  "agent": "${AGENT_NAME}",
  "pr_number": ${PR_NUMBER},
  "issues": [
    {
      "file_path": "path/to/file",
      "line_numbers": "42-45",
      "severity": "critical|high|medium|low",
      "category": "${CATEGORIES}",
      "title": "Short title (max 80 chars)",
      "impact": "What happens if not fixed (max 120 chars)",
      "description": "Detailed explanation",
      "suggested_fix": "Specific code fix",
      "confidence": 95,
      "auto_fixable": false
    }
  ]
}

## RULES

### Severity Definitions
- **critical**: Data loss, security vulnerability, crash in production, or silent corruption. Would block merge.
- **high**: Incorrect behavior under realistic conditions, or a pattern that reliably causes bugs. Would block merge.
- **medium**: Code smell, maintainability issue, or edge case unlikely in normal use. Recommended fix.
- **low**: Style, naming, minor improvement, or nitpick. Optional.

### Confidence Calibration
- **90-100**: You can point to the exact code path that causes the problem.
- **70-89**: Strong signal but depends on runtime conditions or code you cannot see.
- **50-69**: Suspicious pattern that MIGHT be a problem. Needs human verification.
- **Below 50**: Do not report.

### Reporting Rules
- Only report issues within YOUR focus area. If another specialist would catch it, skip it.
- Use Read/Grep/Glob to examine source files beyond the diff for context.
- The "impact" field must describe the CONSEQUENCE, not restate the problem.
  Bad: "There is a null pointer dereference"
  Good: "Server crashes when processing orders with no shipping address"
- Set "auto_fixable" to true ONLY for mechanical fixes requiring no human judgment (unused imports, missing type annotations, formatting). If the fix requires understanding business logic, set to false.
- If you find zero issues in your focus area, write an empty issues array. Do not invent findings.
${EXTRA_RULES}

After writing the JSON file, your work is complete.
```

### Agent Definitions Table

Below are all agents. Always spawn all 9 core agents. Spawn tech-specific agents based on detected tech.

#### Core Agents (always run)

| Name | Model | Focus | Diff File | Categories |
|------|-------|-------|-----------|------------|
| code-reviewer | opus | Bugs, logic errors, race conditions, null pointers, off-by-one, resource leaks, edge cases, code smells, performance issues, maintainability, naming clarity, error handling, logging adequacy | context.txt | bug\|logic\|resource\|edge-case\|smell\|performance\|maintainability\|naming\|error-handling |
| code-simplifier | sonnet | Over-engineering, unnecessary complexity, premature abstractions, redundant/dead code | diff.txt | over-engineering\|complexity\|abstraction\|dead-code |
| silent-failure-hunter | sonnet | Swallowed exceptions, empty catch blocks, ignored error returns, dangerous fallbacks, silent data corruption | context.txt | swallowed-exception\|empty-catch\|ignored-return\|missing-handler\|dangerous-fallback |
| type-design-analyzer | sonnet | Type safety, any/unknown abuse, unsafe casts, missing types, overly permissive types, union handling | diff.txt | type-safety\|any-abuse\|unsafe-cast\|missing-type\|permissive-type |
| comment-analyzer | sonnet | Outdated comments, misleading docs, missing docs for complex logic, TODO comments | diff.txt | outdated-comment\|misleading-doc\|missing-doc\|todo-ticket |
| pr-test-analyzer | sonnet | Missing test coverage, untested edge cases, brittle tests, missing integration tests | diff.txt | missing-coverage\|untested-edge-case\|brittle-test\|missing-integration |
| security-auditor | opus | Security vulnerabilities across OWASP Top 10 2021 (A01-A10): injection (SQL, XSS, command, SSRF), broken access control, cryptographic failures, insecure design, security misconfiguration, vulnerable components, authentication failures, data integrity issues, logging gaps, hardcoded secrets, path traversal. Extra JSON fields: `owasp_category`, `attack_scenario` | context.txt | injection\|xss\|csrf\|auth-bypass\|secrets\|crypto\|A01\|A02\|A03\|A04\|A05\|A06\|A07\|A08\|A09\|A10 |
| code-architect | opus | Architectural violations, coupling, layering violations, circular deps, god classes, SOLID violations | context.txt | coupling\|layering\|circular-dep\|god-class\|solid-violation |
| cross-cutting-concerns | opus | Cross-file inconsistencies: API/interface shape changes without updating all consumers, new routes/endpoints missing middleware or auth that sibling routes have, error handling or logging patterns applied inconsistently across sibling files, type definitions changed without updating all usage sites, config/env var changes without corresponding code updates | diff.txt | cross-file-inconsistency\|missing-update\|pattern-drift\|api-contract\|incomplete-change |

#### Tech-Specific Agents (conditional on detected tech)

| Condition | Name | Model | Focus | Diff File | Categories |
|-----------|------|-------|-------|-----------|------------|
| HAS_TYPESCRIPT | typescript-pro | sonnet | Advanced types, generics, conditional types, discriminated unions, type narrowing, strict null checks | diff_typescript.txt | type-safety\|generic\|narrowing\|utility-type |
| HAS_PYTHON | python-expert | sonnet | Pythonic idioms, type hints, async/await, context managers, mutable default args, import cycles | diff_python.txt | pythonic\|type-hints\|async\|context-manager |
| HAS_NODEJS | nodejs-expert | sonnet | Event loop blocking, promise handling, async/await, stream handling, memory leaks, unhandled rejections | diff_typescript.txt | event-loop\|promise\|async\|memory-leak |
| HAS_REACT | react-expert | sonnet | Hook rules, dependency arrays, stale closures, unnecessary rerenders, key props, memo/callback misuse | diff_frontend.txt | hooks\|dependency-array\|stale-closure\|rerender |
| HAS_NEXTJS | nextjs-developer | sonnet | Server/client boundaries, data fetching, caching, route handlers, middleware, ISR/SSG/SSR | diff_frontend.txt | server-client\|data-fetching\|caching\|routing |
| HAS_FASTAPI | fastapi-expert | sonnet | Dependency injection, Pydantic models, async endpoints, background tasks, security deps | diff_python.txt | dependency-injection\|pydantic\|async\|security |
| HAS_DJANGO | django-developer | sonnet | ORM usage, N+1 queries, model design, migrations, permissions, caching | diff_python.txt | orm\|n-plus-one\|migration\|permission |
| HAS_FLASK | flask-expert | sonnet | App factory, blueprints, request/app context, extensions, error handlers | diff_python.txt | blueprint\|context\|extension\|error-handler |
| HAS_EXPRESS | express-expert | sonnet | Middleware ordering, error handling middleware, async handler wrapping, security middleware | diff_typescript.txt | middleware\|error-handling\|async\|security |
| HAS_GRAPHQL | graphql-expert | sonnet | Schema design, N+1 problems, dataloader, authorization in resolvers, query complexity | diff.txt | schema\|n-plus-one\|dataloader\|authorization |
| HAS_REST_API | rest-expert | sonnet | HTTP semantics, status codes, resource naming, pagination, idempotency, error format | diff_backend.txt | http-method\|status-code\|resource-naming\|pagination |
| HAS_OPENAPI | openapi-expert | sonnet | Schema correctness, component reuse, security definitions, operation IDs | diff.txt | schema\|component\|security-def\|operation-id |
| HAS_POSTGRES | postgres-expert | sonnet | Query performance, indexes, N+1, transactions, connection pooling, SQL injection | diff_database.txt | query-perf\|index\|transaction\|sql-injection |
| HAS_PRISMA | prisma-expert | sonnet | Schema design, relations, transactions, migrations, N+1 prevention | diff_database.txt | schema\|relation\|transaction\|migration |
| HAS_JWT | jwt-expert | sonnet | Algorithm confusion, key management, token validation, expiration, refresh rotation | diff.txt | algorithm\|key-mgmt\|validation\|expiration |
| HAS_OAUTH | oauth-oidc-expert | sonnet | Auth code flow, PKCE, state parameter, redirect URI validation, token exchange | diff.txt | auth-flow\|pkce\|state\|redirect-uri |
| HAS_PLAYWRIGHT | playwright-expert | sonnet | Test isolation, selector stability, wait strategies, fixtures, flaky test prevention | diff_typescript.txt | isolation\|selector\|wait\|fixture |
| HAS_CYPRESS | cypress-expert | sonnet | Command chaining, intercepts, custom commands, retry-ability, cy.wait anti-patterns | diff_typescript.txt | chaining\|intercept\|custom-command\|retry |
| HAS_DOCKER | docker-expert | sonnet | Image size, layer caching, multi-stage builds, security (non-root), health checks | diff_devops.txt | image-size\|layer-cache\|security\|health-check |
| HAS_GITHUB_ACTIONS | github-actions-expert | sonnet | Workflow triggers, caching, secrets, matrix builds, security permissions, concurrency | diff_devops.txt | trigger\|cache\|secret\|permission |
| HAS_CSS or HAS_TAILWIND | css-expert | sonnet | Specificity, !important abuse, responsive design, accessibility, layout shifts | diff_css.txt | specificity\|responsive\|accessibility\|layout |
| HAS_TAILWIND | tailwind-expert | sonnet | Class ordering, responsive patterns, theme usage, arbitrary values, dark mode | diff_frontend.txt | class-order\|responsive\|theme\|dark-mode |
| HAS_LANGCHAIN | langchain-expert | sonnet | Chain composition, prompt templates, memory, callbacks, agent design, vector stores | diff_python.txt | chain\|prompt\|memory\|callback |
| HAS_PANDAS or HAS_NUMPY | pandas-expert | sonnet | Vectorization, chained indexing, copy vs view, memory, dtype optimization | diff_python.txt | vectorization\|indexing\|memory\|dtype |

### Agent EXTRA_RULES Definitions

When launching an agent, look up its name below. If an entry exists, substitute its content into the `${EXTRA_RULES}` placeholder in the prompt. If no entry exists (e.g., express-expert), substitute an empty string.

#### Core Agent EXTRA_RULES

**code-reviewer:**
```
### Scope
- You are the generalist. Report bugs, logic errors, and correctness issues.
- Severity HIGH only for: provable bugs (null deref, off-by-one, resource leak, race condition). MEDIUM for code smells with measurable impact. LOW for style/readability.
- Do NOT report: type system issues (type-design-analyzer), security vulnerabilities (security-auditor), test gaps (pr-test-analyzer), documentation issues (comment-analyzer), complexity (code-simplifier), architectural concerns (code-architect).
- Do NOT flag performance issues without identifying the hot path or data size that makes it matter.
```

**code-simplifier:**
```
### Scope
- Severity HIGH only for: code demonstrably harder to modify due to unnecessary abstraction (single-implementation interfaces, wrapper classes adding no behavior, strategy patterns with one strategy). MEDIUM for redundant code paths. LOW for verbose-but-clear code.
- Do NOT flag: code following an established pattern in the codebase (consistency beats local optimality), error handling/logging/observability code (operational needs invisible in the diff).
- Do NOT suggest refactors that would change public API surface or require modifications outside the files in the diff.
```

**silent-failure-hunter:**
```
### Scope
- Severity CRITICAL for: silently swallowed errors in data mutation paths (writes, deletes, state changes) where the caller assumes success. HIGH for ignored error returns on I/O. MEDIUM for empty catch blocks in read paths. LOW for best-effort/fire-and-forget patterns.
- Do NOT flag: catch blocks that log and continue, cleanup/finally paths, optional feature guards (analytics, telemetry), .catch(() => {}) on non-critical fire-and-forget promises, fallback values in config/feature-flag loading.
- When flagging an empty catch or ignored return, you MUST state what failure mode the caller experiences (e.g., "caller receives stale data", "write silently dropped").
```

**type-design-analyzer:**
```
### Scope
- Only produce findings for TypeScript, Flow, or files with JSDoc type annotations. Skip untyped JS, Python, Go, and other languages.
- Severity HIGH for: `as any` on values from external sources (API, DB, user input), non-null assertions (!) on external data, type predicates without runtime validation. MEDIUM for overly broad types (Record<string, any> where shape is known). LOW for missing return types on private functions.
- Do NOT flag: `any` in test files/fixtures, third-party library type workarounds, `as const`, `unknown` used correctly for narrowing.
```

**comment-analyzer:**
```
### Scope
- Severity HIGH only for: comments factually wrong given current code (e.g., "returns null" when it throws, stale param names in JSDoc). MEDIUM for TODO/FIXME introduced in this PR without a tracking issue. LOW for missing documentation.
- Do NOT flag: missing docstrings on self-documenting code (clear function names), missing docs on private/internal functions or test helpers, comment style (// vs /** */, casing, punctuation).
```

**pr-test-analyzer:**
```
### Scope
- Severity HIGH for: new public API endpoints, exported functions handling user input, or data mutation logic with zero test coverage. MEDIUM for missing edge-case tests on covered code. LOW for missing tests on internal helpers, config, or glue code.
- Do NOT flag: simple delegation methods, data classes/DTOs with no logic, framework boilerplate, generated code, test implementation details (mock strategy, assertion library, naming).
- When suggesting a missing test, name the specific scenario (e.g., "when input array is empty") not generic "add more tests."
```

**security-auditor:**
```
### Security-Specific
- Add extra JSON fields: "owasp_category" (A01-A10 ID), "attack_scenario" (1-2 sentences on how an attacker exploits this).
- Severity CRITICAL only if you can describe a concrete attack with a realistic attacker model. "An attacker could..." must specify how they reach the vulnerable code path. If you cannot describe the attack path, downgrade to MEDIUM.
- Do NOT flag: hardcoded non-secret strings (config keys, error messages, public URLs), hash algorithms for non-security purposes (cache keys, ETags), endpoints behind auth middleware visible in the codebase, theoretical SSRF in internal-only services with no user-facing input path.
- Skip code style, complexity, architecture, test coverage — your scope is strictly: can an attacker exploit this?
```

**code-architect:**
```
### Scope
- Severity HIGH only for: circular dependencies, bypassing existing abstraction layers (e.g., direct DB calls from controller when repository pattern exists), god classes (>500 lines of mixed responsibilities). MEDIUM for coupling increases. LOW for SOLID nitpicks on small focused code.
- Do NOT suggest architectural refactors for PRs touching fewer than 3 files or adding fewer than 100 lines of new code.
- Do NOT flag coupling that follows an established pattern in the codebase.
- Skip code correctness, security, test coverage — focus only on: dependency direction, module boundaries, layering, responsibility allocation.
```

**cross-cutting-concerns:**
```
### Scope
- Only produce findings that span 2+ files. If a finding applies to a single file, skip it — another agent handles it.
- Severity HIGH for: interface/contract changes (API schemas, shared types, DB migrations) where not all consumers in the diff are updated. MEDIUM for pattern drift (new code uses different approach than existing code for same concern). LOW for inconsistent naming across files.
- If the diff touches only 1 file, produce zero findings and write an empty issues array.
```

#### Tech-Specific Agent EXTRA_RULES

**typescript-pro:**
```
### TypeScript-Specific
- `any` cast silencing a real type error is HIGH. `any` in test fixtures or third-party type gaps is LOW.
- Missing discriminant check before narrowing a union is HIGH (runtime crash). `as` assertion that widens (as unknown as T) is HIGH.
- Non-null assertion (!) on external input (API, DB, user) is HIGH. On values just checked by a guard clause is LOW.
- Do NOT flag explicit generic params when inference works, or single-level conditional types.
```

**nodejs-expert:**
```
### Node.js-Specific
- Sync I/O in request handlers is HIGH (blocks event loop). Sync calls in CLI scripts or startup is LOW.
- Missing .catch() on a floating promise (not awaited, not returned) is CRITICAL — unhandled rejection crashes process.
- Unbounded Promise.all on user-controlled array without batching is HIGH. stream.pipe() without error handling is HIGH — prefer pipeline().
- Do NOT flag normal object allocation or EventEmitter usage patterns.
```

**python-expert:**
```
### Python-Specific
- Mutable default args (def f(x=[])) are HIGH. Bare except or except Exception: pass is HIGH. Missing async with for async context managers is HIGH (resource leak).
- Import cycle causing runtime ImportError is CRITICAL. Cycles guarded by if TYPE_CHECKING are fine.
- type: ignore without specific error code is MEDIUM. Do NOT flag type: ignore[specific-code].
- Do NOT flag: missing type hints on private helpers/tests, stylistic preferences (f-strings vs .format), code following the project's existing conventions.
```

**fastapi-expert:**
```
### FastAPI-Specific
- Dependency creating DB session without yield + cleanup is HIGH (connection leak). Pydantic model accepting Any/dict for user input is HIGH (bypasses validation).
- Sync def endpoint doing I/O is HIGH (blocks threadpool). Missing Depends() auth on mutation endpoints is CRITICAL.
- Background task accessing request-scoped dependencies (Depends session) is HIGH — session is closed.
- Do NOT flag model_config vs class Config style, or response_model when return type annotation is used.
```

**django-developer:**
```
### Django-Specific
- QuerySet in a loop without select_related/prefetch_related is HIGH (N+1). Raw SQL with string formatting is CRITICAL (injection).
- Missing migration for model field changes is HIGH. Model.objects.all() without pagination on large tables is MEDIUM.
- save() calling external services is HIGH (side effects in ORM). Overriding save() for local logic is LOW.
- Do NOT flag: Meta ordering, __str__ formatting, CharField vs TextField decisions, migration file contents.
```

**flask-expert:**
```
### Flask-Specific
- Accessing request/g outside request context (background threads, module-level) is CRITICAL. Missing teardown_appcontext for resources on g is HIGH (leak).
- Mutable module-level state shared across requests is HIGH (race condition in multi-worker). Broad exception handler returning 200 is HIGH.
- Not using app factory is LOW unless test isolation is broken. Do NOT flag flask.jsonify() vs dict returns.
```

**react-expert:**
```
### React-Specific
- Missing useEffect dependency causing stale state in user-visible behavior is HIGH. Intentional [] for run-once with stable values is fine.
- Hooks called conditionally or in loops is CRITICAL (Rules of Hooks violation). Missing key on reorderable lists is HIGH; index key on static lists is LOW.
- Creating new objects/functions in render passed to memoized children is HIGH (defeats React.memo). useMemo/useCallback on primitives is LOW.
- Do NOT flag state management library choices or component file structure.
```

**nextjs-developer:**
```
### Next.js-Specific
- useState/useEffect/browser APIs in Server Component (no 'use client') is CRITICAL. Importing large client lib in Server Component that passes to client is HIGH (bundle bloat).
- Data fetching in client component when Server Component would work is MEDIUM. Missing revalidate/cache on dynamic routes serving stale data is HIGH.
- Middleware with heavy computation or DB queries is HIGH (runs on every matching request).
- Do NOT flag Pages Router vs App Router choice, or use server unless there is a security issue.
```

**tailwind-expert:**
```
### Tailwind-Specific
- Conflicting utilities on same element (p-4 p-8) is HIGH — wins unpredictably by CSS source order. Hardcoded colors instead of theme tokens is MEDIUM (breaks theme/dark mode).
- Arbitrary values when a token exists is LOW. Responsive breakpoint class order is LOW (Tailwind handles it correctly).
- @apply with 10+ utilities is LOW. Do NOT flag hover:/focus: absence on non-interactive elements.
```

**css-expert:**
```
### CSS-Specific
- !important to win specificity war with own styles is HIGH. !important to override third-party inline styles is acceptable (LOW).
- Missing width/height on images (CLS/layout shift) is HIGH. display: none for accessibility hiding is HIGH (hidden from screen readers — use sr-only). Fixed px font sizes is MEDIUM (breaks zoom).
- Do NOT flag vendor prefix absence (autoprefixer), CSS methodology choice, or z-index on modals/overlays.
```

**postgres-expert:**
```
### Postgres-Specific
- String concatenation in SQL is CRITICAL (injection). Missing index on WHERE/JOIN columns on large tables is HIGH. SELECT * in app code is MEDIUM.
- Long-running transactions holding locks (wrapping HTTP calls) is CRITICAL (pool exhaustion). Missing LIMIT on user-facing queries is HIGH.
- Do NOT flag parameterized query builders (Knex, SQLAlchemy), BIGINT vs INT choice, or TEXT vs VARCHAR unless there is a correctness bug.
```

**prisma-expert:**
```
### Prisma-Specific
- findMany accessing relations in a loop without include is HIGH (N+1). Missing @unique on fields used in findUnique/upsert is CRITICAL.
- Interactive $transaction holding open for external API calls is HIGH. $queryRaw with template literal not using Prisma.sql is CRITICAL (injection).
- Do NOT flag schema formatting, model naming, enum vs string decisions, or Json type usage.
```

**rest-expert:**
```
### REST-Specific
- GET that mutates state is HIGH. Returning 200 for errors is HIGH (clients/monitoring treat as success). Missing pagination on unbounded list endpoints is HIGH.
- Exposing stack traces or DB details in error responses is HIGH (security). Non-idempotent PUT/DELETE is MEDIUM.
- Do NOT flag resource naming style (plural vs singular), API versioning strategy, or POST for complex queries exceeding URL limits.
```

**graphql-expert:**
```
### GraphQL-Specific
- Resolver querying DB without DataLoader for batch-eligible fields is HIGH (N+1). Missing auth checks on mutation resolvers is CRITICAL.
- Unbounded list fields without pagination args is HIGH. Missing query depth/complexity limiting on public APIs is HIGH.
- Exposing sensitive data in schema (passwords, tokens) is HIGH — any client can query any exposed field.
- Do NOT flag schema-first vs code-first, naming conventions, or ID scalar vs Int.
```

**openapi-expert:**
```
### OpenAPI-Specific
- Missing security requirement on auth-protected endpoints is HIGH. additionalProperties: true on request bodies is MEDIUM (allows unexpected fields).
- Missing error status codes (400, 401) is MEDIUM. Inline schemas duplicated 3+ times instead of $ref is MEDIUM.
- Do NOT flag OpenAPI version choice, YAML vs JSON, description wording, or operationId naming style.
```

**jwt-expert:**
```
### JWT-Specific
- Accepting alg: "none" or not validating alg against allowlist is CRITICAL (signature bypass). Symmetric signing with weak/short secret is HIGH.
- Not validating exp, iss, or aud claims is HIGH. Storing JWT in localStorage is MEDIUM (XSS-accessible). Non-rotated refresh tokens is HIGH.
- Do NOT flag RS256 vs ES256 vs EdDSA choice, or JWT vs opaque token architecture decision.
```

**oauth-oidc-expert:**
```
### OAuth/OIDC-Specific
- Missing state parameter in authorization requests is CRITICAL (CSRF). Implicit flow for server/native apps is HIGH. Missing PKCE on public clients is HIGH.
- Not validating redirect_uri against strict allowlist is CRITICAL (token theft). Access tokens in URL query params is HIGH.
- Do NOT flag auth code vs device code flow choice, or ID token payload structure.
```

**playwright-expert:**
```
### Playwright-Specific
- Selectors based on CSS classes/DOM position are HIGH (fragile). page.waitForTimeout(N) instead of condition-based waits is HIGH (flaky).
- Tests sharing state without isolation are HIGH (order-dependent flakes). Missing await on actions/assertions is CRITICAL (test passes without checking).
- Do NOT flag test description wording, file organization, or describe nesting depth.
```

**cypress-expert:**
```
### Cypress-Specific
- cy.wait(N) with fixed ms instead of cy.wait('@alias') is HIGH (flaky). Assigning command return to variable is HIGH (commands are async Chainables).
- this.* aliases in arrow functions is HIGH (no this binding). Tests depending on external API state is HIGH.
- Do NOT flag cy.contains() usage, custom command organization, or Cypress vs Playwright choice.
```

**docker-expert:**
```
### Docker-Specific
- Running as root in production images (no USER instruction) is HIGH. Copying secrets/.env into image is CRITICAL. Using latest tag for base image is MEDIUM (non-reproducible).
- Missing .dockerignore with COPY . . is MEDIUM (bloated image). Separate RUN for apt-get update/install is MEDIUM (stale layer).
- Not using multi-stage is LOW unless image exceeds 500MB. Do NOT flag base image choice (alpine vs slim) or EXPOSE documentation.
```

**github-actions-expert:**
```
### GitHub Actions-Specific
- pull_request_target with checkout of PR head is CRITICAL (executes untrusted code with secrets). Secrets in run: via interpolation is HIGH (may be logged).
- Missing permissions: block on public repos is HIGH. Third-party actions pinned to mutable tag is MEDIUM for public repos, LOW for private.
- Missing concurrency control on deployment workflows is MEDIUM. Do NOT flag workflow naming, job naming, or ubuntu-latest usage.
```

**langchain-expert:**
```
### LangChain-Specific
- User input directly in prompt templates without sanitization is HIGH (prompt injection). Unbounded memory (no k/token limit) is HIGH (context overflow, cost explosion).
- Chains swallowing LLM errors silently is MEDIUM. Sequential chain with 4+ LLM calls when fewer would suffice is MEDIUM.
- Do NOT flag vector store choice, LangChain vs alternatives, or prompt wording quality.
```

**pandas-expert:**
```
### Pandas-Specific
- iterrows() for vectorizable operations is HIGH (100-1000x slower). Chained indexing (df['a']['b'] = val) is HIGH (silently fails to modify original).
- Loading full dataset without dtype/usecols/chunksize on potentially large files is HIGH. Silent dtype coercion (int to float from NaN) is MEDIUM.
- inplace=True is LOW (deprecated but not a bug). Do NOT flag apply() with lambda as HIGH — flag as MEDIUM with suggestion.
```

**Store task IDs**: After launching all agents, store each agent's returned `task_id` along with its name and model in an `AGENT_TASK_MAP`. This is used in Phase 7 for cost reporting.

**IMPORTANT**: After launching all review agents, DO NOT perform any reviews yourself.
Wait for all agents to complete by polling for their JSON output files, then aggregate results.

### Line Number Format in Diffs

The diff files include actual file line numbers:
```
diff --git a/src/file.tsx b/src/file.tsx
@@ -48,7 +50,10 @@
  50   function Component() {    <- Context line at line 50
     - const old = value;        <- Deleted line (no line number)
  51 + const new = value;        <- Added line at line 51
  52   return null;              <- Context line at line 52
```

Report the line numbers shown in the diff (e.g., "Lines 50-52"), NOT positions in the diff text.

---

## Phase 4: Aggregate Results from JSON Files

### 4.1 Wait for Agent Completion (with auto-retry on failure)

Poll every ~30 seconds until all agents are accounted for (produced JSON, retried, or timed out):

1. Use Glob `PR_${PR_NUMBER}/reviews/*.json` to find agents that wrote output
2. For each agent whose JSON file does NOT exist yet, call `TaskOutput(task_id, block: false, timeout: 5000)`:
   - If TaskOutput returns a result → agent finished without writing JSON → **agent failed**
   - If TaskOutput times out → agent is still running → check again next poll
3. For each agent detected as failed (finished without writing JSON, and NOT already retried):
   - Display: `⚠ "${AGENT_NAME}" failed (no JSON output). Retrying with Sonnet 4.6...`
   - Relaunch with the SAME prompt from Step 3.1 but `model: sonnet`, `max_turns: 20`, `run_in_background: true`
   - Add retry task_id to AGENT_TASK_MAP with `model: sonnet` (keep original entry for cost tracking)
   - Add agent name to a RETRIED set so it's not retried again
4. Continue polling until ALL agents (including retries) have produced JSON or 15-minute overall timeout
5. After timeout, identify agents that are in the RETRIED set but still have no JSON output. For each:
   - Call `TaskOutput(task_id, block: false, timeout: 5000)` to capture the error
   - If the result contains "Prompt is too long", add to `CONTEXT_OVERFLOW_AGENTS` map (agent name → original diff file path)
   - Otherwise, note as permanently failed
6. If `CONTEXT_OVERFLOW_AGENTS` is non-empty, proceed to Phase 4.2. Otherwise, skip to 4.3.

### 4.2 Focused-Diff Retry for Context Overflow (fallback)

**This phase ONLY runs when agents fail with "Prompt is too long" after both initial run AND Sonnet retry.**

#### Step 1: Create focused diffs for each failed agent type

Only create the filtered diffs that are actually needed by the agents in `CONTEXT_OVERFLOW_AGENTS`.

**diff_error_handling.txt** — views, forms, models, notification (no tests/migrations/commands):
```bash
awk '
/^diff --git/ { p=0 }
/^diff --git.*(views|forms|models|notification_service|admin).*\.py$/ { p=1 }
/^diff --git.*tests\/.*\.py$/ { p=0 }
p==0 { next }
/^diff --git/ { file_header = $0; printed_header = 0; next }
/^index |^--- |^\+\+\+ / { next }
/^@@/ { plus_pos = index($0, "+"); rest = substr($0, plus_pos + 1); gsub(/[^0-9].*/, "", rest); new_line = rest - 1; if (printed_header == 0) { print file_header; printed_header = 1 }; print $0; next }
/^-/ { printf "     - %s\n", substr($0, 2); next }
/^\+/ { new_line++; printf "%4d + %s\n", new_line, substr($0, 2); next }
{ new_line++; printf "%4d   %s\n", new_line, $0 }
' /tmp/claude/pr_raw_diff.txt > PR_${PR_NUMBER}/diff_error_handling.txt
```

**diff_tests.txt** — test files only:
```bash
awk '
/^diff --git/ { p=0 }
/^diff --git.*tests\/.*\.py$/ { p=1 }
p==0 { next }
/^diff --git/ { file_header = $0; printed_header = 0; next }
/^index |^--- |^\+\+\+ / { next }
/^@@/ { plus_pos = index($0, "+"); rest = substr($0, plus_pos + 1); gsub(/[^0-9].*/, "", rest); new_line = rest - 1; if (printed_header == 0) { print file_header; printed_header = 1 }; print $0; next }
/^-/ { printf "     - %s\n", substr($0, 2); next }
/^\+/ { new_line++; printf "%4d + %s\n", new_line, substr($0, 2); next }
{ new_line++; printf "%4d   %s\n", new_line, $0 }
' /tmp/claude/pr_raw_diff.txt > PR_${PR_NUMBER}/diff_tests.txt
```

**diff_core_python.txt** — production Python only (no tests, migrations, management commands):
```bash
awk '
/^diff --git/ { p=0 }
/^diff --git.*\.py$/ { p=1 }
/^diff --git.*tests\/.*\.py$/ { p=0 }
/^diff --git.*migrations\/.*\.py$/ { p=0 }
/^diff --git.*management\/commands\/.*\.py$/ { p=0 }
p==0 { next }
/^diff --git/ { file_header = $0; printed_header = 0; next }
/^index |^--- |^\+\+\+ / { next }
/^@@/ { plus_pos = index($0, "+"); rest = substr($0, plus_pos + 1); gsub(/[^0-9].*/, "", rest); new_line = rest - 1; if (printed_header == 0) { print file_header; printed_header = 1 }; print $0; next }
/^-/ { printf "     - %s\n", substr($0, 2); next }
/^\+/ { new_line++; printf "%4d + %s\n", new_line, substr($0, 2); next }
{ new_line++; printf "%4d   %s\n", new_line, $0 }
' /tmp/claude/pr_raw_diff.txt > PR_${PR_NUMBER}/diff_core_python.txt
```

For any other agent type not in the table below, create a focused diff by filtering to files relevant to that agent's domain (e.g., TypeScript agent → `.ts`/`.tsx` only, CSS agent → `.css`/`.scss` only).

#### Step 2: Map failed agents to their focused diff files

| Failed Agent | Diff File(s) |
|---|---|
| silent-failure-hunter | `diff_error_handling.txt` |
| pr-test-analyzer | `diff_tests.txt` + `diff_core_python.txt` |
| python-expert | `diff_core_python.txt` |
| code-reviewer | `diff_core_python.txt` |
| code-simplifier | `diff_core_python.txt` |
| comment-analyzer | `diff_core_python.txt` |
| type-design-analyzer | `diff_typescript.txt` |
| security-auditor | `diff_error_handling.txt` |
| code-architect | `diff_core_python.txt` |
| cross-cutting-concerns | `diff.txt` (already exists; if still fails, split into 2 halves) |
| django-developer | `diff_core_python.txt` |
| rest-expert | `diff_core_python.txt` |

#### Step 3: Relaunch with modified prompt

For each agent in `CONTEXT_OVERFLOW_AGENTS`, apply these 3 changes to the retry prompt:

1. **Replace the diff file** with the focused version from the table above
2. **Add this warning** at the top of the FOCUS section:
   ```
   IMPORTANT: Read ONLY the diff file(s) specified below. Do NOT use Read/Grep/Glob
   to explore additional source files. Previous attempts failed because agents read
   too many files and exceeded context limits.
   ```
3. **Shorten the prompt**: Remove the full `PR_BODY`. Replace with a 2-3 sentence summary of the PR.

Launch all focused-diff retries with `model: sonnet`, `max_turns: 20`, `run_in_background: true`.
Add retry task_ids to AGENT_TASK_MAP with `model: sonnet`.

Poll for completion using the same Glob-based approach as Phase 4.1 (check for JSON files every ~30 seconds, 10-minute timeout).

#### Step 4: Output to separate directories

For each retried agent, write issue files to a separate directory instead of the main output directory. This keeps the original agent findings separate from the focused-diff retry findings.
- `pr-test-analyzer` retries → `PR_${PR_NUMBER}/autofixable/test_gaps_pr-test-analyzer/`
- `comment-analyzer` retries → `PR_${PR_NUMBER}/autofixable/docs_comment-analyzer/`
- Other agent retries with `auto_fixable` true → `PR_${PR_NUMBER}/autofixable/general_${AGENT_NAME}/`
- Other agent retries with `auto_fixable` false → `PR_${PR_NUMBER}/issues_${AGENT_NAME}/`

#### Step 5: Display focused-diff retry stats

```
FOCUSED-DIFF RETRIES: ${COUNT}
   ${AGENT_NAME}: ${ORIGINAL_DIFF} (${ORIGINAL_LINES} lines) → ${FOCUSED_DIFF} (${FOCUSED_LINES} lines)
```

### 4.3 Read JSON Files Directly

**CRITICAL**: Do NOT use TaskOutput. Read the JSON files directly from disk.

```
Glob: PR_${PR_NUMBER}/reviews/*.json
```

For each JSON file found:
1. Read the file with the Read tool
2. Parse the JSON
3. Extract the `issues` array
4. Add to combined issues list

### 4.4 Deduplicate Issues

For issues with same file + overlapping lines + similar title:
- Keep the one with highest confidence
- Merge severity (take the highest)
- Note all sources that identified it
- Combine descriptions if different insights

### 4.5 Categorize and Sort

Group by severity: CRITICAL > HIGH > MEDIUM > LOW
Sort within groups by confidence (highest first), then file path.

### 4.6 Quality Check

If total unique issues < 5 for a PR with 100+ lines changed, verify agents examined the diff carefully.
Typical ratio: ~1 issue per 50-100 lines of changed code.

---

## Phase 5: Generate Output Files

### 5.1 Summary File: `PR_${PR_NUMBER}/reviews/SUMMARY.md`

```markdown
# Deep Review Summary - PR #${PR_NUMBER}

**Title**: ${PR_TITLE}
**URL**: ${PR_URL}
**Files Changed**: ${FILES_CHANGED}
**Review Date**: ${DATE}
**Agents Run**: ${AGENT_COUNT}

---

## Quick Stats

| Severity | Count | Must Fix Before Merge |
|----------|-------|----------------------|
| Critical | X | YES |
| High | X | YES |
| Medium | X | Recommended |
| Low | X | Optional |
| **Total** | **X** | |

---

## Triage Table

| # | Sev | Conf | Impact | File | Title | Fix |
|---|-----|------|--------|------|-------|-----|
${FOR_EACH_ISSUE_BY_SEVERITY}
| ${INDEX} | ${SEV_SHORT} | ${CONFIDENCE}% (${SOURCE_COUNT}) | ${IMPACT} | `${FILE_PATH}:${LINE}` | ${TITLE} | ${IF_AUTO_FIXABLE}auto${ENDIF} |
${END_FOR_EACH}

---

## Tech Stack Detected
${LIST_OF_DETECTED_TECHNOLOGIES}

## Agents Run

### Core Agents (${CORE_COUNT})
${LIST_CORE_AGENTS}

### Tech-Specific Agents (${TECH_COUNT})
${LIST_TECH_AGENTS}

${IF_UNSUPPORTED_FILES}
## Unsupported Tech Warning
${UNSUPPORTED_TECH_TABLE}
${ENDIF}

---

## Critical Issues (${COUNT})
${FOR_EACH_CRITICAL_ISSUE}
### ${INDEX}. ${TITLE}
- **File**: `${FILE_PATH}:${LINE}`
- **Category**: ${CATEGORY}
- **Sources**: ${AGENTS}
- **Confidence**: ${CONFIDENCE}%

${DESCRIPTION}

**Fix**:
```
${SUGGESTED_FIX}
```
${END_FOR_EACH}

---

## High Priority Issues (${COUNT})
${SIMILAR_FORMAT}

## Medium Priority Issues (${COUNT})
${SIMILAR_FORMAT}

## Low Priority / Suggestions (${COUNT})
${SIMILAR_FORMAT}

---

## Files Most Affected

| File | Critical | High | Medium | Low | Total |
|------|----------|------|--------|-----|-------|
${TABLE}

---

## Next Steps

1. Fix all Critical issues before merge
2. Fix all High issues before merge
3. Consider Medium issues for code quality
4. Low issues can be addressed in future PRs

${IF_AUTO_FIXABLE_ISSUES}
## Auto-Fixable Issues

${AUTO_FIX_COUNT} issues can be fixed automatically without human review:
${LIST_AUTO_FIXABLE_ISSUES}

To batch-fix all auto-fixable issues (see `PR_${PR_NUMBER}/autofixable/README.md` for details):
\`\`\`
claude "For each .md file in PR_${PR_NUMBER}/autofixable/**/*.md (excluding README.md), spawn a separate Opus agent to fix that issue. Each agent should: 1) Read the issue file, 2) Apply the suggested fix, 3) Stage only the changed files, 4) Commit with message: fix: <issue title> (from deep-review PR #${PR_NUMBER}). Run agents sequentially so commits are clean."
\`\`\`
${ENDIF}
```

### 5.2 Individual Issue Files (REQUIRED FOR ALL ISSUES)

Route issues by source agent and auto_fixable flag:
- If agent is `pr-test-analyzer` → write to `PR_${PR_NUMBER}/autofixable/test_gaps/${PADDED_NUM}_${SEVERITY}_${SLUG}.md`
- If agent is `comment-analyzer` → write to `PR_${PR_NUMBER}/autofixable/docs/${PADDED_NUM}_${SEVERITY}_${SLUG}.md`
- If `auto_fixable` is true (any other agent) → write to `PR_${PR_NUMBER}/autofixable/general/${PADDED_NUM}_${SEVERITY}_${SLUG}.md`
- All other issues → write to `PR_${PR_NUMBER}/issues/${PADDED_NUM}_${SEVERITY}_${SLUG}.md`

Number sequences are independent per directory (each starts at 01).

For EVERY unique issue, create the file in the appropriate directory:

```markdown
# Issue #${NUM}: ${TITLE}

${IMPACT}

**Severity**: ${SEVERITY}
**Confidence**: ${CONFIDENCE}%
**Category**: ${CATEGORY}
**Sources**: ${AGENTS}

## Why This Matters
${IMPACT}

> **Impact**: ${IMPACT}
${IF_AUTO_FIXABLE}> **Auto-fixable**: Yes _(mechanical fix, no human judgment needed)_${ENDIF}
> ${SEVERITY} | ${CONFIDENCE}% confidence | ${SOURCE_COUNT} agent(s) flagged

---

## Location
- **File**: `${FILE_PATH}`
- **Lines**: ${START}-${END}
- **GitHub**: ${GITHUB_LINK_TO_LINES}

## Code
```${LANGUAGE}
${CODE_SNIPPET}
```

## Suggested Fix
```${LANGUAGE}
${FIX_CODE}
```

## Problem
${DETAILED_DESCRIPTION}

## For Autonomous Fix
```
claude "Fix the issue in PR_${PR_NUMBER}/${DIR}/${FILENAME}"
```
```

Where `${DIR}` is `autofixable/test_gaps` for pr-test-analyzer issues, `autofixable/docs` for comment-analyzer issues, `autofixable/general` for auto-fixable issues from other agents, `issues` for all others.

### 5.2.1 Unsupported Tech Issue File (Conditional)

If unsupported tech detected, create `PR_${PR_NUMBER}/issues/000_critical_unsupported-tech-stack.md` with details about limited coverage.

### 5.3 Verify Issue Completeness (REQUIRED — issues are often silently dropped)

After creating all issue files, reconcile against the raw agent JSON files. The deduplication step in 5.2 frequently drops valid issues — this step catches that.

1. **Count raw agent findings by severity**: Read each `PR_${PR_NUMBER}/reviews/*.json`, count issues grouped by severity:
   ```
   Raw findings: X critical, Y high, Z medium, W low (T total from N agents)
   ```

2. **Count issue files by severity**: Glob `PR_${PR_NUMBER}/issues/*_{critical,high,medium}_*.md` and `PR_${PR_NUMBER}/autofixable/**/*_{critical,high,medium}_*.md`, count per severity (combine all directories):
   ```
   Issue files: A critical, B high, C medium (issues: X, autofixable: Y)
   ```

3. **Check for gaps**: Normal deduplication reduces raw count by 40-60% (multiple agents flag the same issue). If issue files for any severity are **fewer than 30%** of the raw count at that severity, issues were dropped — not just deduplicated.
   - Example: 19 raw high-severity findings → expect 8-12 unique issue files. If only 3 exist, issues were dropped.

4. **Fix gaps**: If a gap is detected at any severity:
   - Re-read ALL agent JSONs for that severity
   - For each agent issue, check if an issue file exists covering the same file_path + overlapping line range
   - Create issue files for any uncovered issues (following the 5.2 format)
   - Group truly duplicate uncovered issues (same file + overlapping lines) into single files

5. **Display final counts**:
   ```
   VERIFIED: A critical, B high, C medium issue files | from T raw findings (N agents)
   ```
   If files were added: `Added X missing issue files (were dropped during deduplication)`

### 5.4 Create Autofixable README (REQUIRED if autofixable/ has any .md files)

If `PR_${PR_NUMBER}/autofixable/` contains any issue files, create `PR_${PR_NUMBER}/autofixable/README.md`:

```markdown
Fix all issues (one Opus agent per issue, one commit per fix) in "${REPO_ABSOLUTE_PATH}/PR_${PR_NUMBER}/autofixable". Read "${REPO_ABSOLUTE_PATH}/PR_${PR_NUMBER}/autofixable/README.md" before applying your fixes.

# Auto-Fixable Issues

This directory contains issues that can be fixed mechanically without human judgment.

## How to Fix

### Fix all issues (one Opus agent per issue, one commit per fix)

\`\`\`
claude "For each .md file in PR_${PR_NUMBER}/autofixable/**/*.md (excluding this README), spawn a separate Opus agent to fix that issue. Each agent should: 1) Read the issue file, 2) Apply the suggested fix, 3) Stage only the changed files, 4) Commit with message: fix: <issue title> (from deep-review PR #${PR_NUMBER}). Run agents sequentially so commits are clean."
\`\`\`

### Fix a single issue

\`\`\`
claude "Fix the issue in PR_${PR_NUMBER}/autofixable/<subdir>/<filename>.md"
\`\`\`

### Fix issues by category

\`\`\`
claude "Fix all issues in PR_${PR_NUMBER}/autofixable/test_gaps/"
claude "Fix all issues in PR_${PR_NUMBER}/autofixable/docs/"
claude "Fix all issues in PR_${PR_NUMBER}/autofixable/general/"
\`\`\`

## Directory Structure

- `test_gaps/` — Missing test coverage (from pr-test-analyzer)
- `docs/` — Comment and documentation issues (from comment-analyzer)
- `general/` — Mechanical fixes from other review agents (unused imports, missing types, formatting, etc.)
```

---

## Phase 6: Display Final Summary

```
═══════════════════════════════════════════════════════════════
                    DEEP REVIEW COMPLETE
═══════════════════════════════════════════════════════════════

PR #${PR_NUMBER}: ${PR_TITLE}

AGENTS RUN: ${TOTAL}
   Core: ${CORE_COUNT}
   Tech-specific: ${TECH_COUNT}
${IF_RETRIED_AGENTS}
   Retried: ${RETRY_COUNT} (auto-retried with Sonnet 4.6 after failure)
${ENDIF}

OUTPUT: PR_${PR_NUMBER}/
   reviews/SUMMARY.md        <- Start here
   reviews/*.json             <- Raw agent findings
   issues/*.md               <- Individual issue files (${ISSUE_COUNT})
   autofixable/README.md     <- How to auto-fix issues
   autofixable/test_gaps/*.md <- Missing test coverage (${TEST_GAP_COUNT})
   autofixable/docs/*.md     <- Comment/doc issues (${DOCS_COUNT})
   autofixable/general/*.md  <- Auto-fixable issues from other agents (${GENERAL_AUTOFIX_COUNT})

CRITICAL:  ${COUNT} (must fix)
HIGH:      ${COUNT} (must fix)
MEDIUM:    ${COUNT} (recommended)
LOW:       ${COUNT} (optional)
   TOTAL:     ${TOTAL}

${IF_CRITICAL_OR_HIGH}
This PR has blocking issues that should be fixed before merge.
${ENDIF}

${IF_NO_CRITICAL_AND_NO_HIGH}
No blocking issues found. Review medium/low for quality improvements.
${ENDIF}

═══════════════════════════════════════════════════════════════

To fix an issue automatically:
  claude "Fix the issue in PR_${PR_NUMBER}/issues/001_critical_xxx.md"

To auto-fix all mechanical issues (see PR_${PR_NUMBER}/autofixable/README.md):
  claude "Fix all issues in PR_${PR_NUMBER}/autofixable/"
```

---

## Error Handling

- If an agent fails (finishes without writing JSON), it is auto-retried once with `model: sonnet` (all models have 1M context, so context limits are rare — failures are usually due to max_turns or other issues)
- If retry also fails, continue with available results
- If GitHub CLI fails, check `gh auth status`
- Minimum viable output: produce summary from whatever JSON files exist

---

## Phase 7: Cost Report

After Phase 6, retrieve usage data from each agent and display a cost estimate.

### 7.1 Retrieve Usage

For each agent in `AGENT_TASK_MAP`, call `TaskOutput(task_id, block: false, timeout: 5000)`.
Extract `total_tokens` from the `<usage>` tag in each result.
If TaskOutput fails for an agent, record 0 tokens for that agent and continue.

### 7.2 Calculate Cost

CRITICAL: Use EXACTLY these blended rates. Current pricing: Opus 4.6 is $5/$25 per MTok, Sonnet 4.6 is $3/$15 per MTok. (NOT $15/$75 — that was Claude 3 Opus, which is deprecated). Do NOT substitute different pricing.

Using blended rates (assumes ~80% input / 20% output tokens):
- **Opus**: `total_tokens / 1_000_000 * 9.00` (blended: 0.80 × $5 + 0.20 × $25 = $9/MTok)
- **Sonnet**: `total_tokens / 1_000_000 * 5.40` (blended: 0.80 × $3 + 0.20 × $15 = $5.40/MTok)

### 7.3 Display Cost Summary

```
═══════════════════════════════════════════════════════════════
                        COST ESTIMATE
═══════════════════════════════════════════════════════════════

Model      Agents    Tokens        Est. Cost
───────────────────────────────────────────────────────────────
Opus       ${N}      ${TOKENS}     ~$${COST}
Sonnet     ${N}      ${TOKENS}     ~$${COST}
───────────────────────────────────────────────────────────────
TOTAL      ${N}      ${TOKENS}     ~$${COST}

Estimates assume 80/20 input/output token ratio.
Leader agent cost not included.

Print the following footer line VERBATIM (do not modify the dollar amounts):
Pricing: Opus $5/$25, Sonnet $3/$15 per MTok.

═══════════════════════════════════════════════════════════════
```

---

## Performance Notes

- **Hybrid model**: Opus 4.6 for 4 high-impact agents (code-reviewer, security-auditor, code-architect, cross-cutting-concerns), Sonnet 4.6 for the rest. All agents have 1M context.
- Cost is ~2-3x of `/deep-review-cheap`, ~0.3-0.5x of `/deep-review-expensive-are-you-sure`
- For full Sonnet (cheapest), use `/deep-review-cheap`
- For full Opus (most thorough), use `/deep-review-expensive-are-you-sure`
