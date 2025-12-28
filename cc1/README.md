# CC1 Documentation System

CC1 is a session-aware knowledge management system that maintains institutional memory across Claude Code sessions.

## File Purposes

### **VISION.md** - Product Vision & Opportunity Solution Tree
**What:** Desired outcomes, opportunities (problems), solutions (specs), success metrics
**When to update:** Quarterly reviews, new opportunity discovery, strategic pivots
**Format:** Lightweight OST framework linking opportunities to specs

**Core Sections:**
- Desired Outcome & Product Mission
- User Archetypes & Success Metrics
- Opportunity Solution Tree (opportunities → solutions)
- Current Focus & Discovery Backlog

**Example OST Entry:**
```markdown
### Opportunity: user-onboarding-friction
**Evidence:** 60% abandon during email verification
**Impact:** Blocks 600+ potential users monthly
**Target:** Reduce drop-off to <20%

**Solutions:**
- #spec:magic-link-auth (implementing)
- #spec:progressive-profile (planned)

**Assumptions to Test:**
- [ ] Users trust passwordless auth
```

---

### **TASKS.md** - Current Work Tracking
**What:** Active sprint, in-progress, completed, and blocked tasks
**When to update:** Starting work, completing tasks, finding blockers
**Format:** Checklist with tags (#priority, #estimate, #claude-session, #blocked-by)

**Example:**
```markdown
## Current Sprint
- [ ] Implement user authentication #priority:high #estimate:3d #spec:user-auth
- [x] Add email validation #priority:medium #estimate:2h #claude-session:2025-10-04

## Blocked
- [ ] Deploy to production #blocked-by:missing-env-credentials
```

---

### **LEARNINGS.md** - Knowledge Capture
**What:** Errors solved, patterns discovered, commands that work/fail
**When to update:** After solving a problem worth remembering
**Format:** Categorized entries with IDs, tags, and cross-references

**Example:**
```markdown
## 🐛 Errors & Solutions
### [E-012] Database Connection Timeout
**Tags:** #database #postgresql #timeout
**Problem:** Connection pool exhausted under load
**Solution:** Increased pool size to 20, added connection timeout
**Code:** src/database.py:45
```

---

### **specs/** - Feature Specifications (Solutions in OST)
**What:** Lightweight specs linking solutions to opportunities with constraints & context
**When to create:** Multi-day features or security-critical work
**Format:** One markdown file per solution with OST linkage

**Core Sections:**
- Opportunity Context (hypothesis, success metric)
- Problem & Value + Scope Boundaries
- System Context (existing code to reference)
- Constraints & Guardrails (security, performance)
- Requirements & Interfaces

**Example frontmatter:**
```yaml
---
status: implementing
opportunity: "user-onboarding-friction"  # Links to VISION.md
created: 2025-10-05
estimate: 3 days
owner: engineering
---
```

**When to create:**
- ✅ Takes 1+ days or security-critical
- ✅ Needs context injection (reference existing patterns)
- ✅ Has non-obvious constraints or edge cases

**When to skip:**
- ❌ < 2 hours or straightforward CRUD
- ❌ Simple bug fix

---

### **PROJECT_INDEX.md** - Technical Reference
**What:** File structure, dependencies, env vars, DB schema, architecture decisions
**When to update:** Adding files/dependencies, changing architecture
**Format:** Structured reference documentation

**Example:**
```markdown
## Directory Structure
- src/auth/ - Authentication & authorization
- src/api/ - API endpoints
- src/models/ - Database models

## Dependencies
- fastapi 0.100.0 - Web framework
- pyjwt 2.8.0 - JWT token handling

## Environment Variables
- DATABASE_URL - PostgreSQL connection string (required)
- JWT_SECRET - Secret for signing tokens (required)
```

---

### **ROADMAP.md** - Strategic MVP Sequencing
**What:** MVP phases, execution approach, linking opportunities to specs
**When to update:** Planning MVP sequences, completing MVPs, reprioritizing
**Format:** MVP phases with opportunities solved, approach, specs required, success criteria

**Three-layer hierarchy:**
- VISION.md → WHAT problems exist (opportunities + evidence)
- ROADMAP.md → WHEN/HOW to sequence solutions (MVP phases + approach)
- SPECS → HOW to build exactly (implementation details)

**Example:**
```markdown
## MVP 1: Core Authentication (Weeks 1-3)
**Solves Opportunities:**
- #opportunity:unauthorized-access (VISION.md)

**Approach:**
1. Build JWT auth system
2. Add role-based access control
3. Implement password reset flow

**Specs Required:**
- #spec:jwt-auth-system #priority:high
- #spec:rbac #priority:medium

**Success Criteria:**
- Zero unauthorized access attempts
- Password reset completes in <2 min
```

---

## Opportunity Solution Tree (OST) Integration

CC1 integrates Teresa Torres' **Opportunity Solution Tree** framework for outcome-driven product development.

### OST Hierarchy in CC1

```
VISION.md
  ├─ Desired Outcome (measurable product goal)
  │
  ├─ Opportunity 1 (problem space)
  │   ├─ Evidence (research/data)
  │   ├─ Target (success criteria)
  │   └─ Solutions
  │       ├─ #spec:solution-a (exploring)
  │       ├─ #spec:solution-b (implementing) → TASKS.md
  │       └─ #spec:solution-c (planned)
  │
  └─ Opportunity 2 (problem space)
      └─ Solutions
          └─ #spec:solution-d (draft)
```

### How It Works

1. **Define Desired Outcome** in VISION.md
   - Example: "Increase activation from 40% → 70% in 90 days"

2. **Identify Opportunities** (problems/pain points)
   - Based on user research, data, feedback
   - Each opportunity gets a slug: `user-onboarding-friction`

3. **Brainstorm Solutions** to opportunities
   - Multiple solutions per opportunity = hypothesis testing
   - Each solution becomes a spec: `specs/magic-link-auth.md`

4. **Link Spec to Opportunity**
   - Spec frontmatter: `opportunity: "user-onboarding-friction"`
   - Creates traceability: outcome → opportunity → solution

5. **Build & Validate**
   - Implement solution (TASKS.md references #spec:name)
   - Measure against opportunity target
   - Learn and iterate

### OST Workflow Example

```
User Research: "60% of signups abandon during email verification"
      ↓
Add to VISION.md as Opportunity: user-onboarding-friction
      ↓
Brainstorm solutions: magic links, OAuth, progressive profile
      ↓
Create specs/magic-link-auth.md with:
  - opportunity: "user-onboarding-friction"
  - hypothesis: "Passwordless auth reduces drop-off to <20%"
      ↓
Add to TASKS.md: "Implement magic link endpoint #spec:magic-link-auth"
      ↓
Build, measure, learn
      ↓
Update VISION.md with results
```

### Why OST in CC1?

**Prevents:**
- ❌ Building solutions looking for problems
- ❌ Feature bloat without clear value
- ❌ Disconnected specs from business goals

**Enables:**
- ✅ Evidence-based decision making
- ✅ Multiple solutions per problem (experimentation)
- ✅ Clear traceability from outcome to implementation
- ✅ Measurable success criteria for each solution

---

## Decision Guide: "Where Does This Go?"

```
┌─────────────────────────────────────────────┐
│ Is it an instruction for Claude?            │
│ (e.g., "Always use X", "When I say Y do Z") │
└─────────────────┬───────────────────────────┘
                  │
            ┌─────┴─────┐
            │    YES    │
            └─────┬─────┘
                  ▼
         Put in CLAUDE.md
         (project root or ~/.claude/)


┌─────────────────────────────────────────────┐
│ Is it strategic vision or an opportunity?   │
│ (outcome, problem space, success metrics)   │
└─────────────────┬───────────────────────────┘
                  │
            ┌─────┴─────┐
            │    YES    │
            └─────┬─────┘
                  ▼
         Add to VISION.md
         (outcome, opportunity, or update OST)


┌─────────────────────────────────────────────┐
│ Is it a task to do now or soon?             │
└─────────────────┬───────────────────────────┘
                  │
            ┌─────┴─────┐
            │    YES    │
            └─────┬─────┘
                  ▼
         ┌───────────────────┐
         │ Takes > 1 day?    │
         │ Security-critical?│
         │ Solves opportunity│
         │ from VISION.md?   │
         └─────┬─────────────┘
               │
          ┌────┴────┐
      YES │         │ NO
          ▼         ▼
    Create spec   Add to
    in specs/     TASKS.md
    with          directly
    opportunity:
    field


┌─────────────────────────────────────────────┐
│ Is it a problem you solved or pattern       │
│ you discovered?                              │
└─────────────────┬───────────────────────────┘
                  │
            ┌─────┴─────┐
            │    YES    │
            └─────┬─────┘
                  ▼
       Add to LEARNINGS.md
       (with ID, tags, solution)


┌─────────────────────────────────────────────┐
│ Is it about MVP sequencing or planning?     │
│ (when to build, execution approach)         │
└─────────────────┬───────────────────────────┘
                  │
            ┌─────┴─────┐
            │    YES    │
            └─────┬─────┘
                  ▼
       Add to ROADMAP.md
       (MVP phases, approach, specs needed)


┌─────────────────────────────────────────────┐
│ Is it reference info about the codebase?    │
│ (structure, dependencies, schema, etc.)      │
└─────────────────┬───────────────────────────┘
                  │
            ┌─────┴─────┐
            │    YES    │
            └─────┬─────┘
                  ▼
       Add to PROJECT_INDEX.md
```

---

## OST-Driven Spec Workflow

### 1. Discovery Phase (OST)
```
Desired Outcome (in VISION.md)
      ↓
Conduct user research / gather data
      ↓
Identify Opportunity (problem space)
      ↓
Add to VISION.md OST with:
  - Evidence (what data shows this problem?)
  - Target (how will we measure success?)
  - Opportunity slug (e.g., "user-onboarding-friction")
      ↓
Brainstorm multiple solutions
```

### 2. Solution Planning Phase
```
Opportunity defined in VISION.md
      ↓
Choose solution to validate (hypothesis)
      ↓
Copy specs/_template.md → specs/solution-name.md
      ↓
Fill out (10-20 min):
  - opportunity: "slug" in frontmatter
  - Opportunity Context (hypothesis, success metric)
  - Constraints & Guardrails (what NOT to do)
  - System Context (existing code to reference)
  - Requirements & Interfaces
      ↓
Update status: draft → approved
      ↓
Add #spec:solution-name to VISION.md under opportunity
```

### 3. Implementation Phase
```
Approved Spec (with opportunity link)
      ↓
Create tasks in TASKS.md referencing spec
  Example: "Implement magic link #spec:magic-link-auth"
      ↓
Update spec status: approved → implementing
      ↓
Update VISION.md spec status: (planned) → (implementing)
      ↓
Build solution (Claude generates code)
      ↓
Run Acceptance Checks from spec
```

### 4. Validation Phase
```
Solution Complete
      ↓
Update spec status: implementing → done
      ↓
Measure against opportunity target (from VISION.md)
      ↓
Did it achieve the hypothesis?
      ↓
    ┌────┴────┐
YES │         │ NO
    ▼         ▼
Document    Learn why
learnings   & iterate
    │         │
    └────┬────┘
         ▼
Update VISION.md with:
  - Results
  - Next steps
  - Pivot or double-down decision
      ↓
Document in LEARNINGS.md
      ↓
Update PROJECT_INDEX.md with new files/deps
```

---

## Spec Size Guidelines

| Implementation Time | Spec Needed? | Spec Length | Time to Write |
|---------------------|--------------|-------------|---------------|
| < 2 hours | ❌ No | N/A | N/A |
| 2-8 hours | ⚠️ Optional | ~80-120 lines | 10-15 min |
| 1-3 days | ✅ Yes | ~120-200 lines | 15-25 min |
| 1+ weeks | ✅✅ Definitely | ~200-350 lines | 30-45 min |

**Rule of thumb:** Lightweight specs focus on OST linkage, constraints, and context - not exhaustive checklists.

---

## CLAUDE.md vs CC1 Clarity

### The Golden Rule

**`CLAUDE.md` = AI's instruction manual (how to behave)**
**`CC1/` = Project's knowledge base (what exists)**

### Examples

| Information | Goes In | Why |
|-------------|---------|-----|
| "Always explain bash commands before running" | `CLAUDE.md` | Behavior preference |
| "This project uses pytest for tests" | `PROJECT_INDEX.md` | Project fact |
| "When I say 'refactor', follow clean code" | `CLAUDE.md` | Instruction for Claude |
| "We solved DB timeout by increasing pool" | `LEARNINGS.md` | Project knowledge |
| "Use functional components in this project" | `CLAUDE.md` (project) | Project-specific instruction |
| "User table has columns: id, email, created_at" | `PROJECT_INDEX.md` | Reference data |

### Global vs Project vs Subdirectory CLAUDE.md

Claude Code supports CLAUDE.md at three levels with inheritance:

```
~/.claude/CLAUDE.md                    (Level 1: Global)
       ↓
   Universal AI preferences
   for ALL projects
       ↓
ProjectRoot/CLAUDE.md                  (Level 2: Project)
       ↓
   Project-specific overrides
   and context
       ↓
ProjectRoot/subdir/CLAUDE.md          (Level 3: Subdirectory)
       ↓
   Directory-specific rules
   (e.g., frontend/ vs backend/)
       ↓
   ═══════════════════════════════════
   Final merged instructions for Claude
   (More specific overrides more general)
```

**Level 1: Global (`~/.claude/CLAUDE.md`)**
- Your universal working style with Claude across ALL projects
- Output preferences, communication style, general coding standards
- Example: "Always explain bash commands before running them"
- **Applies to:** Every project, every directory

**Level 2: Project Root (`ProjectRoot/CLAUDE.md`)**
- Project-specific coding conventions and context
- Tech stack specifics, architecture patterns for THIS project
- Example: "This project uses TypeScript with strict mode enabled"
- **Overrides:** Global settings
- **Applies to:** Entire project (unless overridden by subdirectory)

**Level 3: Subdirectory (`ProjectRoot/subdir/CLAUDE.md`)**
- Directory-specific rules for a part of the codebase
- Different conventions for frontend vs backend, or per microservice
- Example: In `frontend/CLAUDE.md`: "Use React functional components only"
- **Overrides:** Project root and global settings
- **Applies to:** Only that directory and its subdirectories

**Example hierarchy:**
```
my-project/
├── CLAUDE.md                    # Project: "Use ESLint standard config"
├── frontend/
│   ├── CLAUDE.md                # Frontend: "Use React hooks, no class components"
│   └── components/              # Inherits: Global → Project → frontend/
├── backend/
│   ├── CLAUDE.md                # Backend: "Use async/await, no callbacks"
│   └── api/                     # Inherits: Global → Project → backend/
└── cc1/                         # Inherits: Global → Project

Result when working in frontend/:
  Global rules + Project rules + frontend/ rules
  (frontend/ rules take precedence)
```

**When to use each level:**
- **Global:** Universal preferences you want everywhere (coding style, communication)
- **Project:** Project-wide conventions (language version, framework patterns)
- **Subdirectory:** Different rules for different parts of codebase (frontend/backend differences)

---

## CC1 Workflow Commands

### `/cc1-init`
**Initialize CC1 in existing or new project** (no tech stack assumptions)
- Creates cc1/ directory structure
- Analyzes existing code to pre-populate PROJECT_INDEX.md
- Detects tech stack, dependencies, environment variables
- Adds specs/ system with template
- Copies this README to project

**Use when:** Starting CC1 on any project (existing or new, any language/framework)

### `/cc1-boilerplatev2`
**Initialize complete FastAPI + Docker + PostgreSQL + CC1 project**
- Clones GitHub template with full tech stack
- Sets up Docker, PostgreSQL, FastAPI boilerplate
- Includes CC1 system pre-configured
- Production-ready structure

**Use when:** Starting brand new Python/FastAPI project from scratch

### `/cc1-update`
**Review session work and suggest numbered doc updates**
- Updates TASKS.md (move completed, add new, mark blocked)
- Updates LEARNINGS.md (add errors solved, patterns found)
- Updates PROJECT_INDEX.md (new files, deps, schema changes)
- Updates ROADMAP.md (adjust MVP priorities based on learnings)
- Updates specs/ (change status, document decisions)
- Interactive: shows numbered suggestions, you choose which to apply

**Use when:** After each coding session to capture knowledge

### `/cc1-audit-improve`
**Audit CC1 docs against actual codebase**
- Validates TASKS.md (completed tasks actually done?)
- Validates PROJECT_INDEX.md (files/deps exist? schema accurate?)
- Validates specs/ (status consistent? contracts match code?)
- Checks for stale information, missing docs, contradictions
- Interactive: shows numbered findings, you choose which to fix

**Use when:** Weekly or when docs feel outdated

---

## Complete CC1 Workflow Visualization

```
┌─────────────────────────────────────────────────────────────┐
│                    PROJECT INITIALIZATION                    │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
              New project         Existing project
              with stack          (any language)
                    │                   │
                    ▼                   ▼
          /cc1-boilerplatev2      /cc1-init
          (FastAPI template)      (analyzes & sets up)
                    │                   │
                    └─────────┬─────────┘
                              ▼
                    ┌─────────────────────┐
                    │  CC1 System Ready   │
                    │  - VISION.md        │
                    │  - ROADMAP.md       │
                    │  - TASKS.md         │
                    │  - LEARNINGS.md     │
                    │  - specs/           │
                    │  - PROJECT_INDEX.md │
                    │  - README.md        │
                    └─────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    FEATURE DEVELOPMENT                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │  New Feature Idea   │
                    └─────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │ Multi-day or      │
                    │ security-critical?│
                    └─────────┬─────────┘
                              │
                    ┌─────────┴─────────┐
                YES │                   │ NO
                    ▼                   ▼
        ┌───────────────────┐   ┌──────────────┐
        │ Create spec from  │   │ Add directly │
        │ specs/_template   │   │ to TASKS.md  │
        └───────────────────┘   └──────────────┘
                    │                   │
                    │ Fill out:         │
                    │ - Constraints     │
                    │ - Context         │
                    │ - Acceptance      │
                    │   Checks          │
                    │                   │
                    ▼                   │
        ┌───────────────────┐           │
        │ Update status:    │           │
        │ draft → approved  │           │
        └───────────────────┘           │
                    │                   │
                    └─────────┬─────────┘
                              ▼
                    ┌─────────────────────┐
                    │   Implementation    │
                    │ (Claude generates)  │
                    └─────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │ Run acceptance      │
                    │ checks / tests      │
                    └─────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │   Mark complete     │
                    │ Update spec: done   │
                    └─────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                  KNOWLEDGE CAPTURE                           │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │   /cc1-update       │
                    │ (after session)     │
                    └─────────────────────┘
                              │
                              ▼
                ┌─────────────────────────────┐
                │ Claude analyzes session:    │
                │ - Tasks completed?          │
                │ - Errors solved?            │
                │ - New files created?        │
                │ - Specs status changed?     │
                │ - Learnings discovered?     │
                └─────────────────────────────┘
                              │
                              ▼
                ┌─────────────────────────────┐
                │ Shows numbered suggestions  │
                │ You choose which to apply   │
                └─────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │  Docs updated with  │
                    │  session knowledge  │
                    └─────────────────────┘
                              │
┌─────────────────────────────────────────────────────────────┐
│                    QUALITY ASSURANCE                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │ /cc1-audit-improve  │
                    │ (weekly/as needed)  │
                    └─────────────────────┘
                              │
                              ▼
                ┌─────────────────────────────┐
                │ Claude validates:           │
                │ - Completed tasks exist?    │
                │ - Docs match codebase?      │
                │ - Specs accurate?           │
                │ - Stale information?        │
                │ - Missing documentation?    │
                └─────────────────────────────┘
                              │
                              ▼
                ┌─────────────────────────────┐
                │ Shows numbered findings     │
                │ You choose which to fix     │
                └─────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │  Docs synchronized  │
                    │  with reality       │
                    └─────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │   Repeat cycle    │
                    └─────────┬─────────┘
                              │
                              ▼
                    (back to Feature Development)
```

---

## Best Practices

### 1. Keep It Current
- Run `/cc1-update` after each significant session
- Run `/cc1-audit-improve` weekly or when things feel stale

### 2. Be Selective
- Don't document trivial changes
- Focus on insights that help future you/Claude
- Quality > quantity

### 3. Use Cross-References
- Link tasks to specs: `#spec:feature-name`
- Link to learnings: `see LEARNINGS.md [E-012]`
- Reference decisions: `see PROJECT_INDEX.md [D-005]`

### 4. Maintain Spec Lifecycle
- Draft → get feedback/refine
- Approved → ready to implement
- Implementing → work in progress
- Done → feature complete, keep for reference
- Deprecated → no longer relevant, archive or delete

### 5. Archive Old Information
After 3-6 months, consider:
- Moving completed specs to `specs/archive/`
- Moving old tasks to "Completed Archive" section
- Keeping only current/relevant information easily accessible

---

## Tips for Effective Vibe Coding with CC1

### Before Coding
1. Check VISION.md for related opportunity
2. If feature > 1 day, create lightweight spec (10-20 min)
3. Focus on: hypothesis, constraints, system context
4. Skip exhaustive checklists - just capture what matters

### During Coding
1. Reference existing patterns from spec's System Context
2. Check LEARNINGS.md for similar problems solved
3. Let Claude generate code guided by constraints
4. Test against the success metric from spec

### After Coding
1. Run `/cc1-update` to document changes
2. Update VISION.md with results (did hypothesis hold?)
3. Add valuable learnings, not trivial changes
4. Update spec status: implementing → done

---

## Quick Reference

**New project with specific stack?** Run `/cc1-boilerplatev2` (FastAPI template)
**Existing project or any new project?** Run `/cc1-init` (analyzes & sets up)
**Define product vision?** Create/update `VISION.md` with desired outcomes
**Found user problem?** Add opportunity to `VISION.md` OST with evidence
**Validating solution?** Create spec with `opportunity:` field linking to VISION.md
**Starting new feature?** Create spec if > 1 day (reference opportunity from VISION.md)
**Finished work?** Run `/cc1-update`
**Things feel outdated?** Run `/cc1-audit-improve`
**Don't know where to put something?** Check Decision Guide above
**Confused about CLAUDE.md vs CC1?** See "Golden Rule" section
**CLAUDE.md at different levels?** See "Global vs Project vs Subdirectory" section
**What's OST?** See "Opportunity Solution Tree Integration" section

---

_Last updated: 2025-10-05 (Added OST integration)_
