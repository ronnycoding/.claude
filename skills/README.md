# Claude Code Skills Reference

Comprehensive documentation for custom Claude Code skills - specialized domain expertise and workflow automations.

## Table of Contents

- [Overview](#overview)
- [Skill Categories](#skill-categories)
  - [Claude Code Customization](#claude-code-customization)
  - [Domain Expertise](#domain-expertise)
- [Available Skills](#available-skills)
- [Usage](#usage)
- [Creating Custom Skills](#creating-custom-skills)
- [Best Practices](#best-practices)

---

## Overview

Skills are specialized prompt templates that provide Claude Code with deep domain expertise or workflow-specific knowledge. They extend Claude's capabilities beyond general programming assistance.

**What Skills Provide:**
- Domain-specific expertise (WebGL, bioinformatics, finance)
- Workflow automation (deployment, testing, research)
- Platform-specific knowledge (Argus, NotebookLM)
- Specialized tool guidance (hooks, subagents, plugins)
- Best practices and patterns for specific technologies

**How Skills Work:**
1. Skills are invoked using the Skill tool: `Skill(skill: "skill-name")`
2. Claude loads the skill's prompt template
3. The skill provides specialized instructions and context
4. Claude follows the skill's guidance for the task

**Skills vs Agents:**
- **Skills**: Provide specialized knowledge to the main Claude instance
- **Agents**: Spawn separate specialized AI instances for complex tasks
- **Combined**: Skills can be used with agents for high-quality domain-specific work

---

## Skill Categories

### Claude Code Customization

Skills for extending and customizing Claude Code itself:

1. **[create-hooks](#create-hooks)** - Create lifecycle hooks for automation
2. **[create-subagent](#create-subagent)** - Build specialized AI agents
3. **[create-skill](#create-skill)** - Design new domain skills
4. **[create-command](#create-command)** - Build slash commands
5. **[create-claude-plugin](#create-claude-plugin)** - Package and distribute extensions
6. **[connect-mcp-server](#connect-mcp-server)** - Integrate MCP servers

### Domain Expertise

Skills providing specialized domain knowledge:

7. **[webgl-expert](#webgl-expert)** - WebGL 3D graphics development
8. **[nightingale-expert](#nightingale-expert)** - Protein sequence visualization
9. **[argus-deployment](#argus-deployment)** - CZI Argus platform deployment
10. **[notebooklm](#notebooklm)** - Google NotebookLM automation
11. **[secure-web-search](#secure-web-search)** - Privacy-focused research
12. **[analyzing-financial-statements](#analyzing-financial-statements)** - Financial analysis
13. **[creating-financial-models](#creating-financial-models)** - Financial modeling

---

## Available Skills

### Claude Code Customization Skills

#### create-hooks

**Description:** Guide for creating Claude Code hooks - shell commands that execute at specific lifecycle events.

**File:** `create-hooks/SKILL.md`

**Use When:**
- Creating lifecycle automation
- Adding event handlers
- Formatting code automatically
- Protecting sensitive files
- Logging operations
- Validating tool inputs

**Capabilities:**
- Hook event reference (9 events)
- PreToolUse, PostToolUse, UserPromptSubmit, etc.
- Blocking and non-blocking hooks
- Environment variable access
- Security best practices
- Example implementations

**Hook Events:**
1. **PreToolUse**: Before tool execution (can block)
2. **PostToolUse**: After tool execution
3. **UserPromptSubmit**: Before user prompt processing (can block)
4. **PostUserPromptSubmit**: After prompt processing
5. **SessionStart**: When session begins
6. **SessionEnd**: When session ends
7. **PreWriteFile**: Before file writes (can block)
8. **PostWriteFile**: After file writes
9. **PreExecuteCommand**: Before command execution (can block)

**Example Usage:**
```bash
# Invoke the skill
Skill(skill: "create-hooks")

# Then describe your hook needs
"Create a hook that prevents writing to .env files"
"Add a hook that runs prettier on modified TypeScript files"
"Set up logging for all GitHub CLI commands"
```

**Key Features:**
- Blocking capabilities (exit code 2)
- Context access via environment variables
- Security validation patterns
- Testing workflows

---

#### create-subagent

**Description:** Guide for creating specialized Claude Code subagents with focused expertise.

**File:** `create-subagent/SKILL.md`

**Use When:**
- Building domain specialists
- Creating workflow orchestrators
- Designing custom AI assistants
- Packaging reusable expertise

**Capabilities:**
- YAML frontmatter configuration
- System prompt engineering
- Tool access control
- Model selection (Haiku/Sonnet/Opus)
- Description optimization

**Agent Structure:**
```yaml
---
name: agent-name
description: Clear, action-oriented description for invocation detection
model: sonnet|opus|haiku
tools:
  - Read
  - Write
  - Bash
---

# System Prompt

Expert instructions for the agent...
```

**Best Practices:**
- Action-oriented descriptions
- Specific tool requirements
- Clear success criteria
- Domain-specific examples
- Model tier optimization

**Example Usage:**
```bash
Skill(skill: "create-subagent")

"Create a security auditor agent that reviews code for vulnerabilities"
"Build a database optimizer agent for PostgreSQL performance"
```

---

#### create-skill

**Description:** Guide for creating well-structured Claude Code skills with proper YAML frontmatter.

**File:** `create-skill/SKILL.md`

**Use When:**
- Packaging domain expertise
- Creating reusable knowledge templates
- Building educational guides
- Documenting specialized workflows

**Capabilities:**
- Skill file structure
- YAML frontmatter format
- Description optimization
- Supporting file organization
- Best practices

**Skill Structure:**
```markdown
---
name: skill-name
description: When to use this skill and what it provides
---

# Skill Content

Specialized instructions and knowledge...
```

**Example Usage:**
```bash
Skill(skill: "create-skill")

"Create a skill for GraphQL schema design best practices"
"Build a skill for Kubernetes YAML configuration"
```

---

#### create-command

**Description:** Guide for creating custom Claude Code slash commands.

**File:** `create-command/SKILL.md`

**Use When:**
- Building reusable workflows
- Creating prompt templates
- Designing CLI shortcuts
- Packaging common operations

**Capabilities:**
- Command file structure
- Argument handling
- Frontmatter configuration
- Prompt template design
- Best practices

**Command Structure:**
```markdown
---
description: Command description
args:
  - name: arg1
    description: Argument description
    required: true
---

# Command Prompt Template

Instructions that expand when command is invoked...
```

**Example Usage:**
```bash
Skill(skill: "create-command")

"Create a command for database schema migration"
"Build a command for API documentation generation"
```

---

#### create-claude-plugin

**Description:** Guide for creating Claude Code plugins that bundle skills, agents, commands, hooks, and MCP servers.

**File:** `create-claude-plugin/SKILL.md`

**Use When:**
- Packaging related functionality
- Creating distributable extensions
- Building marketplaces
- Sharing custom tools

**Capabilities:**
- Plugin structure and organization
- marketplace.json format
- Installation workflows
- Testing strategies
- Publishing guidelines

**Plugin Structure:**
```
my-plugin/
├── marketplace.json
├── skills/
│   └── my-skill/
├── agents/
│   └── my-agent.md
├── commands/
│   └── my-command.md
├── hooks/
│   └── my-hook.sh
└── mcp-servers/
    └── my-server/
```

**Example Usage:**
```bash
Skill(skill: "create-claude-plugin")

"Create a plugin for React development workflows"
"Build a plugin for AWS infrastructure management"
```

---

#### connect-mcp-server

**Description:** Guide for connecting MCP (Model Context Protocol) servers to Claude Code.

**File:** `connect-mcp-server/SKILL.md`

**Use When:**
- Integrating external services
- Adding API integrations
- Connecting databases
- Setting up authentication

**Capabilities:**
- HTTP transport configuration
- stdio transport setup
- SSE (Server-Sent Events)
- Environment variables
- Authentication patterns
- Security best practices

**Transport Types:**
1. **HTTP**: REST APIs and web services
2. **stdio**: Local processes and scripts
3. **SSE**: Real-time streaming data

**Example Usage:**
```bash
Skill(skill: "connect-mcp-server")

"Connect a Postgres database via MCP"
"Set up GitHub API integration"
"Configure Slack notifications"
```

---

### Domain Expertise Skills

#### webgl-expert

**Description:** Expert guide for WebGL API development including 3D graphics, shaders (GLSL), and rendering pipelines.

**File:** `webgl-expert/SKILL.md`

**Use When:**
- Building 3D visualizations
- Creating WebGL applications
- Writing GLSL shaders
- Optimizing GPU performance
- Implementing texture mapping
- Canvas rendering

**Capabilities:**
- WebGL 1.0 and 2.0 APIs
- GLSL shader programming (vertex/fragment)
- Rendering pipeline architecture
- Buffer management
- Texture operations
- Performance optimization
- Cross-browser compatibility

**Topics Covered:**
- WebGLRenderingContext interface
- Shader compilation and linking
- Vertex and index buffers
- Texture mapping and samplers
- Transformation matrices
- Lighting calculations
- Frame buffer operations
- Extension APIs

**Supporting Files:**
- `reference.md` - Complete API reference
- Examples and patterns

**Example Usage:**
```bash
Skill(skill: "webgl-expert")

"Create a 3D rotating cube with texture mapping"
"Implement phong lighting in a fragment shader"
"Optimize draw calls for particle system"
```

---

#### nightingale-expert

**Description:** Expert guide for Nightingale web components - protein sequence and biological data visualization library.

**File:** `nightingale-expert/skill.md`

**Use When:**
- Visualizing protein sequences
- Building bioinformatics tools
- Integrating UniProt data
- Creating sequence viewers
- Displaying protein features
- Biological data visualization

**Capabilities:**
- Nightingale component library
- UniProt API integration
- Sequence track rendering
- Feature annotation display
- Protein structure visualization
- Data binding patterns
- Customization options

**Components:**
- Sequence viewers
- Feature tracks
- Structure viewers
- Navigation controls
- Data loaders
- Color schemes

**Supporting Files:**
- `README.md` - Overview and quick start
- `components-reference.md` - Component API
- `examples.md` - Usage examples

**Example Usage:**
```bash
Skill(skill: "nightingale-expert")

"Create a protein sequence viewer with domain annotations"
"Display UniProt features for protein P12345"
"Build an interactive sequence alignment tool"
```

---

#### argus-deployment

**Description:** Expert guide for deploying applications on the CZI Argus platform using GitOps and Kubernetes.

**File:** `argus-deployment/SKILL.md`

**Use When:**
- Deploying to CZI Argus platform
- Configuring Kubernetes stacks
- Setting up GitOps workflows
- Managing Helm values
- Working with ArgoCD
- Biohub application deployment

**Capabilities:**
- `.infra/` directory structure
- Helm values configuration
- Environment management (dev/staging/prod)
- ArgoCD Application resources
- GitHub Actions workflows
- Stack troubleshooting
- Secret management

**Key Concepts:**
- GitOps-based deployment (file changes only)
- Helm charts and Kustomize
- ArgoCD sync operations
- Environment-specific values
- Stack configuration

**Deployment Flow:**
1. Configure `.infra/` files
2. Push to GitHub
3. ArgoCD detects changes
4. Kubernetes resources updated
5. Application deployed

**Example Usage:**
```bash
Skill(skill: "argus-deployment")

"Set up a new web service on Argus"
"Configure staging environment with custom values"
"Debug ArgoCD sync failure"
"Add environment variables to production stack"
```

---

#### notebooklm

**Description:** Guide for managing Google NotebookLM from the command line using nlm CLI.

**File:** `notebooklm/skill.md`

**Use When:**
- Creating research notebooks
- Managing document sources
- Generating audio overviews
- Organizing research materials
- Automating NotebookLM workflows

**Capabilities:**
- Notebook creation and management
- Source upload (PDFs, URLs, text)
- Audio generation with transcripts
- Outline and guide creation
- Export and organization
- Rate limiting and error handling

**nlm CLI Commands:**
- `nlm create` - Create notebooks
- `nlm add-source` - Upload documents
- `nlm generate-audio` - Create audio overviews
- `nlm export` - Download content
- `nlm list` - View notebooks

**Example Usage:**
```bash
Skill(skill: "notebooklm")

"Create a research notebook from PDFs"
"Generate audio overview of multiple articles"
"Export notebook content to markdown"
```

---

#### secure-web-search

**Description:** Guide for performing secure web searches with privacy protection and source verification.

**File:** `secure-web-search/SKILL.md`

**Use When:**
- Conducting privacy-focused research
- Verifying sources and facts
- Checking information validity
- Avoiding tracking and profiling
- Researching sensitive topics

**Capabilities:**
- Privacy-preserving search strategies
- Source verification techniques
- Fact-checking workflows
- Information validation
- Secure search operators
- Result filtering

**Privacy Techniques:**
- Using privacy-focused search engines
- Avoiding tracking cookies
- Verifying SSL certificates
- Checking source credibility
- Cross-referencing information

**Example Usage:**
```bash
Skill(skill: "secure-web-search")

"Research medical information with source verification"
"Find academic papers without tracking"
"Verify news article authenticity"
```

---

#### analyzing-financial-statements

**Description:** Calculate key financial ratios and metrics from financial statement data.

**File:** `analyzing-financial-statements/SKILL.md`

**Use When:**
- Analyzing company financials
- Calculating financial ratios
- Evaluating investment opportunities
- Performing due diligence
- Comparing company performance

**Capabilities:**
- Liquidity ratios (current, quick, cash)
- Profitability ratios (ROE, ROA, margins)
- Leverage ratios (D/E, interest coverage)
- Efficiency ratios (turnover, days sales)
- Market ratios (P/E, P/B, dividend yield)
- Trend analysis

**Financial Ratios:**
- **Liquidity**: Current ratio, quick ratio, cash ratio
- **Profitability**: ROE, ROA, profit margins, EBITDA
- **Leverage**: Debt/equity, interest coverage
- **Efficiency**: Asset turnover, inventory turnover
- **Market**: P/E ratio, EPS, dividend yield

**Example Usage:**
```bash
Skill(skill: "analyzing-financial-statements")

"Analyze Apple's latest 10-K filing"
"Compare profitability ratios for tech companies"
"Calculate liquidity metrics from balance sheet"
```

---

#### creating-financial-models

**Description:** Advanced financial modeling suite with DCF analysis, sensitivity testing, and Monte Carlo simulations.

**File:** `creating-financial-models/SKILL.md`

**Use When:**
- Building financial models
- Performing DCF valuations
- Running scenario analysis
- Testing sensitivity
- Monte Carlo simulations
- Investment decision support

**Capabilities:**
- Discounted Cash Flow (DCF) analysis
- Comparable company analysis
- Sensitivity tables and charts
- Scenario planning (best/base/worst)
- Monte Carlo simulations
- Risk analysis
- Valuation ranges

**Modeling Techniques:**
- Revenue forecasting
- Cost structure modeling
- Working capital projections
- Free cash flow calculations
- WACC determination
- Terminal value estimation
- Risk-adjusted returns

**Example Usage:**
```bash
Skill(skill: "creating-financial-models")

"Build a DCF model for a SaaS company"
"Run Monte Carlo simulation for project ROI"
"Create sensitivity analysis for acquisition"
"Model best/base/worst case scenarios"
```

---

## Usage

### Invoking Skills

**In Conversation:**
Skills are invoked automatically by Claude when relevant, or you can explicitly request them:

```bash
# Automatic invocation
"I need to create a hook that runs tests before commits"
# Claude detects need and invokes create-hooks skill

# Explicit invocation
"Use the webgl-expert skill to help me build a 3D scene"
```

**Via Skill Tool:**
```bash
Skill(skill: "skill-name")
```

**Listing Available Skills:**
```bash
# View all installed skills
ls ~/.claude/skills/

# View skill description
cat ~/.claude/skills/skill-name/SKILL.md
```

### Skill Selection

**Claude automatically selects skills based on:**
1. **Description matching**: Keywords in skill description
2. **User mentions**: Direct references to technologies
3. **Context analysis**: Understanding of task requirements
4. **Previous usage**: Learning from conversation flow

**Example Detection:**
- User: "Create a WebGL shader" → Invokes `webgl-expert`
- User: "Deploy to Argus" → Invokes `argus-deployment`
- User: "Build a custom hook" → Invokes `create-hooks`

### Combining Skills and Agents

Skills can be used standalone or with specialized agents:

**Skill Standalone:**
```bash
# Skill provides knowledge to main Claude instance
Skill(skill: "webgl-expert")
"Create a fragment shader for water effects"
```

**Skill + Agent:**
```bash
# Skill provides domain knowledge
# Agent provides specialized processing
Task(
  subagent_type: "frontend-developer",
  prompt: "Use webgl-expert skill to build 3D visualization"
)
```

**Workflow:**
1. Agent spawned with task
2. Agent loads relevant skill
3. Agent applies skill knowledge
4. High-quality domain-specific output

---

## Creating Custom Skills

### When to Create a Skill

Create a new skill when:
- You have specialized domain knowledge to package
- A workflow is repeated frequently
- Existing skills don't cover your needs
- You want to share expertise with others
- Complex domain requires deep understanding

**Good Skill Candidates:**
- Medical data processing
- Legal compliance checking
- Financial derivatives pricing
- Domain-specific testing strategies
- Platform-specific deployment patterns

### Skill Creation Process

1. **Invoke create-skill:**
   ```bash
   Skill(skill: "create-skill")
   ```

2. **Define your skill:**
   - Name and description
   - When to use it
   - What knowledge it provides
   - Examples and patterns

3. **Structure the content:**
   - Clear section headers
   - Step-by-step workflows
   - Code examples
   - Best practices
   - Common pitfalls

4. **Add supporting files:**
   - Reference documentation
   - API specifications
   - Example implementations
   - Testing strategies

5. **Test the skill:**
   - Invoke with various scenarios
   - Verify knowledge accuracy
   - Check invocation detection
   - Validate examples

### Skill File Structure

```
skill-name/
├── SKILL.md           # Main skill prompt
├── README.md          # User documentation (optional)
├── reference.md       # API/technical reference (optional)
├── examples.md        # Usage examples (optional)
└── assets/            # Supporting files (optional)
```

**SKILL.md Template:**
```markdown
---
name: skill-name
description: Clear description of when to use this skill
---

# Skill Title

Brief overview of what this skill provides.

## When to Use

- Scenario 1
- Scenario 2
- Scenario 3

## Capabilities

What the skill can help with:
1. Capability 1
2. Capability 2
3. Capability 3

## Knowledge Areas

### Topic 1
Detailed information...

### Topic 2
Detailed information...

## Examples

### Example 1
```code
example code
```

### Example 2
```code
example code
```

## Best Practices

- Practice 1
- Practice 2
- Practice 3

## Common Pitfalls

- Pitfall 1 and how to avoid it
- Pitfall 2 and how to avoid it

## References

- [Documentation](url)
- [API Reference](url)
```

---

## Best Practices

### Skill Design

**Write Clear Descriptions:**
- Use action-oriented language
- Include specific keywords
- Mention technologies explicitly
- Describe exact use cases

**Good:**
```yaml
description: Expert guide for WebGL API development including 3D graphics, shaders (GLSL), rendering pipeline, textures, buffers, and performance optimization. Use when working with WebGL, 3D graphics, or when user mentions OpenGL ES, GLSL, vertex shaders, fragment shaders.
```

**Bad:**
```yaml
description: Helps with graphics stuff
```

**Organize Content Logically:**
1. Overview and capabilities
2. When to use the skill
3. Core concepts and knowledge
4. Step-by-step workflows
5. Examples and patterns
6. Best practices
7. Common pitfalls
8. References

**Provide Complete Examples:**
- Include working code samples
- Show before/after comparisons
- Demonstrate common patterns
- Cover edge cases
- Explain the reasoning

### Usage Guidelines

**Be Specific in Requests:**
```bash
# Good - Specific technology and context
"Use the webgl-expert skill to create a phong lighting shader"

# Bad - Vague and generic
"Help me with graphics"
```

**Combine Skills Appropriately:**
```bash
# Financial modeling + analysis
Skill(skill: "creating-financial-models")
Skill(skill: "analyzing-financial-statements")
"Build and analyze DCF model for acquisition target"
```

**Reference Supporting Files:**
```bash
# When skill has reference documentation
"Check the webgl-expert reference.md for texture parameters"
"Review nightingale-expert examples.md for sequence viewer"
```

### Maintenance

**Keep Skills Updated:**
- Review for accuracy regularly
- Update examples with new APIs
- Add newly discovered patterns
- Remove deprecated information
- Incorporate user feedback

**Document Changes:**
- Version skill content
- Note breaking changes
- Explain rationale for updates
- Maintain changelog

**Test Regularly:**
- Verify examples still work
- Check invocation detection
- Validate knowledge accuracy
- Test with real scenarios

---

## Related Documentation

- **Commands:** `~/.claude/commands/README.md`
- **Templates:** `~/.claude/templates/README.md`
- **Agents:** `~/.claude/agents/README.md`
- **Creating Skills:** Use `create-skill` skill
- **Creating Agents:** Use `create-subagent` skill

---

## Quick Reference

### Skill Categories

**Claude Code Customization:**
1. `create-hooks` - Lifecycle automation
2. `create-subagent` - Specialized agents
3. `create-skill` - Domain expertise packaging
4. `create-command` - Slash commands
5. `create-claude-plugin` - Plugin bundling
6. `connect-mcp-server` - Service integration

**Domain Expertise:**
7. `webgl-expert` - 3D graphics development
8. `nightingale-expert` - Protein visualization
9. `argus-deployment` - CZI platform deployment
10. `notebooklm` - Research automation
11. `secure-web-search` - Privacy research
12. `analyzing-financial-statements` - Financial analysis
13. `creating-financial-models` - Financial modeling

### Skill Invocation

```bash
# Automatic (recommended)
"Create a WebGL particle system"

# Explicit
Skill(skill: "webgl-expert")

# Combined with agent
Task(
  subagent_type: "frontend-developer",
  prompt: "Use webgl-expert skill for 3D scene"
)
```

### File Locations

```
~/.claude/skills/
├── create-hooks/SKILL.md
├── create-subagent/SKILL.md
├── create-skill/SKILL.md
├── create-command/SKILL.md
├── create-claude-plugin/SKILL.md
├── connect-mcp-server/SKILL.md
├── webgl-expert/SKILL.md
├── nightingale-expert/skill.md
├── argus-deployment/SKILL.md
├── notebooklm/skill.md
├── secure-web-search/SKILL.md
├── analyzing-financial-statements/SKILL.md
└── creating-financial-models/SKILL.md
```
