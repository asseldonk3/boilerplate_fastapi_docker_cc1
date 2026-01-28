# Product Vision

**Last Updated:** {{TODAY}}

---

## Desired Outcome

_The measurable business/product goal this product aims to achieve._

**Example goals:**
- Increase user activation rate from 40% → 70% within 90 days
- Reduce customer support tickets by 50% in Q2
- Achieve 10,000 active users by year-end

**Your outcome:** [Define your target outcome here]

**Current Status:** Not yet defined

---

## Product Mission

_One sentence: What problem does this product solve and for whom?_

**Example:** "Enable developers to build AI-powered FastAPI applications in minutes, not days, with production-ready patterns and best practices built-in."

**Your mission:** [Define your product mission here]

---

## Core Principles

_3-5 guiding beliefs that inform all feature decisions._

1. **[Principle Name]** - [Brief description]
2. **[Principle Name]** - [Brief description]
3. **[Principle Name]** - [Brief description]

**Examples:**
- **User data ownership** - Users can export/delete their data anytime
- **Privacy by default** - Opt-in for all tracking
- **Accessibility first** - WCAG AA minimum

---

## User Archetypes

### Primary User: [Role/Type]
- **Goals:** [What they want to accomplish]
- **Pain Points:** [What frustrates them today]
- **Success Looks Like:** [How they'll know this product works]

### Secondary User: [Role/Type]
- **Goals:** [What they want to accomplish]
- **Pain Points:** [What frustrates them today]
- **Success Looks Like:** [How they'll know this product works]

---

## Success Metrics

**North Star Metric:** [The one metric that best captures value delivery]

**Supporting Metrics:**
- **Acquisition:** [How we measure growth]
- **Activation:** [How we measure first-value delivery]
- **Retention:** [How we measure ongoing value]
- **Revenue:** [How we measure business viability]

---

## Opportunity Solution Tree (OST)

_Framework by Teresa Torres: Desired outcomes → opportunities (problems) → solutions (specs)_

### Legend
- 🎯 **Opportunity** - A user problem or friction point (NOT a solution)
- 💡 **Solution** - A specific feature to address an opportunity
- ✅ **Validated** - Solution worked
- ❌ **Invalidated** - Solution didn't work, pivot needed
- 🔄 **In Progress** - Currently testing/building

---

### 🎯 Opportunity: [opportunity-slug]
**Problem:** [What user friction/pain exists? Be specific.]
**Impact:** [How many users? How severe?]
**Evidence:** [User feedback, metrics, observations]

**Solutions:**
- 💡 **[Solution Name]** 🔄
  - **Hypothesis:** If we build X, then Y outcome will improve by Z
  - **Spec:** `cc1/specs/solution-slug.md`
  - **Status:** Draft | Implementing | Done

**Results:**
- 📊 **[Date]** - ✅/❌ [What we learned]

---

## Example OST Entry

### 🎯 Opportunity: developer-environment-setup-friction
**Problem:** New developers spend 30+ minutes configuring environment
**Impact:** Affects 100% of new users, causes 40% to abandon
**Evidence:**
- Support tickets: 15 issues about "Docker won't start"
- User interviews: 4/5 developers said setup was confusing
- Analytics: Avg. time-to-first-run is 47 minutes

**Solutions:**
- 💡 **Automated Setup Script** ✅
  - **Hypothesis:** `./setup.sh` reduces time-to-first-run to <10 min
  - **Result:** Time dropped to 8 minutes avg.

---

## What We're Building Now

**Current Focus:** [Quarter/Sprint Goal]

**Active Opportunities:**
1. **#opportunity:opportunity-slug** - [Brief description]

---

## OST → Spec Workflow

```
VISION.md (problem space)
    ↓
  Define Opportunity + Evidence
    ↓
  Hypothesize Solutions
    ↓
cc1/specs/solution-slug.md (solution space)
    ↓
  Build & Test
    ↓
VISION.md (update with results)
```

---

**Related CC1 Files:**
- `specs/` - Detailed solution specifications
- `backlog.md` - Current work + recently completed
- `learnings.md` - What we've discovered

---

_This is a strategic document. Update manually during planning sessions._
_Created from boilerplate: {{CREATION_DATE}}_
