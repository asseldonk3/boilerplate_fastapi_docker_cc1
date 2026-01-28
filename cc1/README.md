# CC1 Documentation System

CC1 is a lightweight knowledge management system that maintains institutional memory across Claude Code sessions.

## File Structure

```
cc1/
├── learnings.md         # Errors, patterns, gotchas (auto-updated)
├── file-index.md        # Directory structure, key files (auto-updated)
├── architecture.md      # Tech decisions, constraints (auto-updated)
├── vision.md            # Product vision, OST (manual)
├── backlog.md           # Max 5 features: current + done (semi-auto)
├── specs/
│   ├── _template.md     # Spec template
│   └── archive/         # Completed specs archive
└── README.md            # This file
```

---

## File Purposes

### **learnings.md** - Knowledge Capture (Most Valuable!)
**What:** Errors solved, patterns discovered, gotchas found
**Auto-updated:** Yes - after each session via `/cc1-update`
**Format:** Entries with IDs ([E-001], [P-001], [C-001], [G-001])

```markdown
### [E-012] Database Connection Timeout
**Tags:** #database #postgresql
**Problem:** Connection pool exhausted under load
**Solution:** Increased pool size to 20
**File:** src/database.py:45
```

---

### **file-index.md** - Directory Structure
**What:** File tree, key entry points, recently changed files
**Auto-updated:** Yes - tracks file changes each session
**Format:** Tree structure + tables

---

### **architecture.md** - Technical Reference
**What:** Tech stack, dependencies, env vars, schema, decisions
**Auto-updated:** Yes - syncs with actual codebase
**Format:** Tables and decision records ([D-001], [D-002])

```markdown
### [D-005] Use Repository Pattern
**Date:** 2025-10-05
**Decision:** All DB access through repositories
**Rationale:** Decouples business logic from ORM
```

---

### **vision.md** - Product Vision
**What:** Desired outcomes, opportunities, success metrics
**Auto-updated:** No - this is a strategic document
**Format:** Opportunity Solution Tree (OST) framework

---

### **backlog.md** - Feature Sliding Window
**What:** Current work + recently completed (max 5 total)
**Auto-updated:** Semi - asks before moving features
**Rules:**
- Max 2-3 "Currently Building"
- Max 2-3 "Recently Completed"
- 6th item → archive oldest to `specs/archive/`

---

### **specs/** - Feature Specifications
**What:** Detailed specs for multi-day features
**Auto-updated:** Yes - progress updates on `implementing` specs
**When to create:** Features taking >1 day or security-critical

---

## Decision Guide: "Where Does This Go?"

```
┌─────────────────────────────────────────────┐
│ Is it an error you solved or pattern found? │
└─────────────────┬───────────────────────────┘
                  │ YES
                  ▼
         Add to learnings.md
         (with [E-XXX] or [P-XXX] ID)


┌─────────────────────────────────────────────┐
│ Is it about file structure or key files?    │
└─────────────────┬───────────────────────────┘
                  │ YES
                  ▼
         Add to file-index.md


┌─────────────────────────────────────────────┐
│ Is it a tech decision, dep, env var, or     │
│ database schema?                            │
└─────────────────┬───────────────────────────┘
                  │ YES
                  ▼
         Add to architecture.md
         (with [D-XXX] for decisions)


┌─────────────────────────────────────────────┐
│ Is it strategic vision or an opportunity?   │
└─────────────────┬───────────────────────────┘
                  │ YES
                  ▼
         Add to vision.md (manually)


┌─────────────────────────────────────────────┐
│ Is it a multi-day feature to build?         │
└─────────────────┬───────────────────────────┘
                  │ YES
                  ▼
         Create spec from _template.md
         Add to backlog.md
```

---

## Commands

### `/cc1-init`
**Initialize CC1 in a project**
- Creates cc1/ directory structure
- Analyzes existing code to pre-populate
- Migrates old CC1 format if present

**Use:** Starting CC1 on any project

### `/cc1-update`
**Capture session knowledge (after coding)**
- Auto-updates: learnings, file-index, architecture, active specs
- Asks about: backlog changes
- Enforces: max 5 backlog rule

**Use:** After every coding session

### `/cc1-audit-improve`
**Validate docs match code (weekly)**
- Auto-fixes: obvious mismatches
- Asks about: contradictions, stale specs
- Reports: orphan specs, broken references

**Use:** Weekly or when docs feel outdated

### `/cc1-boilerplatev2`
**Create new FastAPI + Docker + CC1 project**
- Clones template from GitHub
- Full stack: FastAPI, PostgreSQL, Docker
- CC1 pre-configured

**Use:** New Python/FastAPI projects only

---

## Auto-Update Behavior

| File | Auto-Update | Triggers |
|------|-------------|----------|
| `learnings.md` | ✅ Always | Errors, patterns, commands, gotchas |
| `file-index.md` | ✅ Always | File create/delete/move |
| `architecture.md` | ✅ Always | Dependencies, env vars, schema, decisions |
| `specs/*.md` | ✅ Active only | Progress on `implementing` specs |
| `backlog.md` | 🔄 Asks | Moving features between sections |
| `vision.md` | ❌ Never | Strategic document (manual only) |

---

## Backlog Rules

The backlog is a **sliding window** of max 5 features:

```
Currently Building (max 2-3)
├── Feature A (implementing)
└── Feature B (implementing)

Recently Completed (max 2-3)
├── Feature C (done: 2025-10-05)
└── Feature D (done: 2025-10-03)

Up Next (parking lot)
└── Ideas waiting to be picked up
```

**When 6th item would be added:**
1. `/cc1-update` prompts you
2. Choose which completed feature to archive
3. Archived to `specs/archive/`

---

## Spec Lifecycle

```
draft → approved → implementing → done → (archive)
```

| Status | Meaning |
|--------|---------|
| `draft` | Still being planned |
| `approved` | Ready to implement |
| `implementing` | Active development |
| `done` | Feature complete |
| (archive) | Moved to `specs/archive/` |

**When to create a spec:**
- ✅ Takes >1 day
- ✅ Security-critical
- ✅ Has complex constraints

**When to skip:**
- ❌ <2 hours work
- ❌ Simple bug fix
- ❌ Straightforward CRUD

---

## Best Practices

### Keep It Current
```
After coding → /cc1-update
Weekly → /cc1-audit-improve
```

### Be Selective
Document what helps future-you and future-Claude:
- **Good:** Error that took 30 min to solve
- **Skip:** Trivial typo fix

### Use Cross-References
```markdown
See learnings.md [E-012] for the solution
See architecture.md [D-005] for the decision
#spec:user-auth for the full specification
```

### Archive, Don't Delete
Old specs go to `specs/archive/`, not trash.

---

## CLAUDE.md vs CC1

| File | Purpose |
|------|---------|
| `CLAUDE.md` | Instructions for Claude (how to behave) |
| `cc1/` | Project knowledge (what exists, what we learned) |

**Examples:**
- "Always use async/await" → `CLAUDE.md`
- "We solved timeout by increasing pool" → `cc1/learnings.md`
- "Project uses FastAPI 0.100" → `cc1/architecture.md`

---

## Workflow Visualization

```
┌─────────────────────────────────────────┐
│         START CODING SESSION            │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│  Multi-day feature?  ──YES──▶ Create spec
│  from specs/_template.md                │
└────────────────┬────────────────────────┘
                 │ NO
                 ▼
┌─────────────────────────────────────────┐
│           CODE & BUILD                  │
│  (Claude generates, you guide)          │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│         RUN /cc1-update                 │
│  • Auto-updates learnings, files, arch  │
│  • Asks about backlog changes           │
└────────────────┬────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────┐
│    Knowledge captured for next session  │
└─────────────────────────────────────────┘

        ┌─────────────────┐
        │  WEEKLY AUDIT   │
        │ /cc1-audit-improve
        │  Validates docs │
        │  match code     │
        └─────────────────┘
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Start CC1 on a project | `/cc1-init` |
| After coding session | `/cc1-update` |
| Weekly maintenance | `/cc1-audit-improve` |
| New FastAPI project | `/cc1-boilerplatev2` |
| New multi-day feature | Copy `specs/_template.md` |

---

_Created from boilerplate: {{CREATION_DATE}}_
