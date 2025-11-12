# [SUB-ISSUE] Component/Module Name

## 🔗 Parent Issue
Part of #[parent_issue_number] - [Parent Issue Title]

## 👤 Assignment
**Assigned Agent/Team Member**: @agent_name
**Specialization**: [e.g., backend-architect, frontend-developer, database-optimizer]
**Story Points**: [Fibonacci: 1, 2, 3, 5, 8, 13, 21]

## 🛠️ Skills & Tooling
**Claude Code Skills**: [List applicable skills from `~/.claude/skills/` or "standalone" if agent-only]
**Custom Skill Needed**: [Yes/No - If yes, describe domain-specific skill requirements]
**Skill Usage**: [Standalone, With Agent, or Both]

## 📋 Summary
Specific description of this sub-task.

## 🎯 Scope
### In Scope
- Specific functionality to implement
- Components to modify
- Tests to write

### Out of Scope
- What this sub-issue does NOT cover
- Handled by other sub-issues

## 🔧 Technical Details
### Implementation Approach
Detailed technical approach for this component.

### Dependencies
- **Blocks**: #issue_numbers
- **Blocked by**: #issue_numbers
- **External dependencies**: libraries, services

### Interface Definition
```yaml
inputs:
  - parameter1: type, description
  - parameter2: type, description
outputs:
  - result1: type, description
  - result2: type, description
```

### Integration Points
- **Receives from**: [Component/Issue] - [Data/Interface description]
- **Provides to**: [Component/Issue] - [Data/Interface description]

## ✅ Acceptance Criteria
- [ ] Core functionality implemented
- [ ] Unit tests written and passing
- [ ] Integration tests with dependent components
- [ ] Code review completed
- [ ] Documentation updated
- [ ] Interface contract validated

## 🧪 Testing Strategy
### Unit Tests
- Test cases for core functionality
- Edge cases and error handling

### Integration Tests
- Interface compatibility with upstream components
- Data flow validation with downstream components

## 📎 Additional Context
### Related Issues
- Depends on: #[issue_number]
- Related to: #[issue_number]

### References
- [Design doc](link)
- [API spec](link)
- [Architecture diagram](link)

### Technical Notes
_Add any implementation-specific notes, gotchas, or considerations_

## 🏷️ Labels
`sub-issue`, `[component-name]`, `[priority]`, `story-points:[X]`

## 📅 Timeline
- **Start**: [Date]
- **Target Completion**: [Date]
- **Estimated**: [X story points]

## 🤝 Handoff Checklist
- [ ] Interface contract documented
- [ ] API endpoints/methods documented
- [ ] Data models/schemas defined
- [ ] Error handling patterns established
- [ ] Integration points validated
- [ ] Handoff notes for dependent teams/agents
