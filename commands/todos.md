# Enhanced TODOs Command

## Command: `claude todos`

Comprehensive issue tracking with agent orchestration support.

## Core Commands

### Initialize

```bash
claude todos --init --project="PROJECT_NAME" --repo="REPO_URL"
```

Add Issue

```bash
claude todos --add \
  --issue="123" \
  --title="Implement User Authentication" \
  --branch="feature/auth" \
  --type="orchestration" \
  --priority="high"
```

Update Issue

```bash
claude todos --update \
  --issue="123" \
  --phase="integration" \
  --progress="75" \
  --agents="backend,frontend,test"
```

Add Subtask

```bash
claude todos --add-subtask \
  --parent="123" \
  --id="ST-001" \
  --agent="backend-specialist" \
  --task="Implement API endpoints"
```

Update Subtask

```bash
claude todos --update-subtask \
  --parent="123" \
  --id="ST-001" \
  --progress="100" \
  --status="complete"
```

Status

```bash
claude todos --status [--issue="123"] [--tree]
Complete
```

```bash
claude todos --complete --issue="123" --pr="456"
```

Output Format (todos.md)
markdown# TODOs

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

**Notes**: JWT implementation, integration testing in progress

---

### [#124] Fix Memory Leak

- **Branch**: `fix/memory-leak`
- **Progress**: 60% | **Assignee**: @dev1

#### Tasks

- [x] Identify source
- [x] Implement fix
- [ ] Test solution
- [ ] Create PR

---

## 🔄 In Review

### [#122] Update Documentation

- **PR**: #456 | **Status**: 1/2 approvals
- **Submitted**: 2024-01-14

---

## ⏸️ Blocked

### [#125] Payment Integration

- **Blocked**: Waiting for API credentials
- **Since**: 2024-01-12

---

## ✅ Completed This Week

- ✅ [#121] Database Optimization - PR #455
- ✅ [#120] Avatar Upload - PR #454
- ✅ [#119] Login Fix - PR #453

---

## 📋 Up Next

1. [#126] Search Feature - Priority: Medium
2. [#127] Email Notifications - Priority: Low
3. [#128] User Preferences - Priority: Medium
Tree View
bashclaude todos --status --tree
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
Quick Reference
Status Codes

🚀 In Progress
🔄 In Review
⏸️ Blocked
✅ Completed
📋 Planned

Priority Levels

🔴 Critical
🟠 High
🟡 Medium
🟢 Low

Agent Status

✅ Complete
🔄 Working
⏸️ Waiting
❌ Failed
