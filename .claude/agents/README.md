# Project Agents

This directory contains AI agents that assist with architecture decisions and debugging during Claude Code sessions.

## Available Agents

### Architect Agent (`architect.md`)

**Purpose**: Evaluate design decisions against architectural principles

**When invoked**:
- Before implementing new features
- When multiple implementation approaches exist
- When a requirement seems to conflict with principles
- During refactoring decisions

**What it does**:
- Analyzes proposals against project principles
- Provides value-effort analysis with multiple options
- Suggests minimum viable solutions
- Identifies potential violations with severity ratings

### Debugger Agent (`debugger.md`)

**Purpose**: Break debugging cycles through systematic root cause analysis

**When invoked**:
- Same fix tried 2-3+ times without success
- Root cause unclear despite multiple attempts
- Bug "moves around" or reappears differently
- Debugging session is stuck in circles

**What it does**:
- Systematic hypothesis formation (ranked by likelihood)
- Log-first investigation methodology
- Root cause identification using 5 Whys
- Solution design with workaround options
- Knowledge capture for future debugging

## Customization

These agents are **generic templates**. Customize them for your project by running:

```bash
claude /setup-project-agents
```

This will:
1. Analyze your project structure (ARCHITECTURE.md, tech stack, logging)
2. Ask interactive questions about your project
3. Generate customized versions with project-specific knowledge

### Manual Customization

If you prefer to customize manually, update these sections:

**In `architect.md`**:
- `Project Context` - Team size, scope, scale, deployment
- `Architecture Principles` - Your project's specific principles
- `Key Documentation` - Links to your docs

**In `debugger.md`**:
- `Tech Stack` - Your actual technologies
- `Critical Components` - Your system's key parts
- `Log Locations` - Where your logs live
- `Historical Failure Patterns` - Known issues from LEARNINGS.md

## How Agents Work

Agents are specialized subprocesses that Claude Code spawns for specific tasks. They have:

- **Limited tools** - Architect is read-only, Debugger can run bash
- **Focused context** - They receive the relevant context for their task
- **Specific expertise** - Prompts tuned for their purpose

When Claude detects a situation matching an agent's purpose, it automatically consults or invokes the appropriate agent.

## Adding New Agents

To create additional project-specific agents:

1. Create a new `.md` file in this directory
2. Add the frontmatter header:
   ```yaml
   ---
   name: agent-name
   description: What this agent does
   tools: Read, Grep, Glob  # Available tools
   model: sonnet  # or opus, haiku
   ---
   ```
3. Write the agent's instructions and methodology

## Best Practices

1. **Keep agents focused** - One clear purpose per agent
2. **Update after incidents** - Add failure patterns to debugger after solving bugs
3. **Evolve principles** - Update architect when architecture decisions change
4. **Document learnings** - Both agents should reference LEARNINGS.md
