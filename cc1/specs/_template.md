---
status: draft          # draft | approved | implementing | done | deprecated
opportunity: ""        # Slug from VISION.md OST (e.g., "user-onboarding-friction")
created: YYYY-MM-DD
updated: YYYY-MM-DD
estimate: X days
owner: ""             # team | engineering | product | design
---

# [Feature Name]

## Opportunity Context
**From OST:** [Opportunity name from VISION.md]
**Hypothesis:** [What we believe this solution will achieve]
**Success Metric:** [How we'll measure if this solution works]

## Problem & Value
**Who:** [User/stakeholder who benefits]
**Problem:** [What pain point does this solve? Why does it exist?]
**Value:** [Why does this matter? What's the impact of solving it?]

## Scope Boundaries
**In Scope:**
- Feature or capability A
- Feature or capability B
- Feature or capability C

**Out of Scope:**
- Feature X (reason: adds complexity, defer to v2)
- Feature Y (reason: not aligned with core goal)
- Feature Z (reason: edge case, handle if requested)

## System Context (Context-Injection)
**Existing Code to Reference:**
- `path/to/file.py` - Pattern/approach to follow
- `path/to/module/` - Similar implementation for reference
- See PROJECT_INDEX.md [D-XXX] for architectural decision
- See LEARNINGS.md [E-XXX] for related error solution

**Dependencies:**
- Requires ENV_VAR_NAME environment variable (see .env.example)
- Uses existing Model/Service (see schema/docs)
- Depends on Package v.X.X (already installed)

**Integration Points:**
- Connects to existing API/service at endpoint
- Shares data model with existing feature

## Constraints & Guardrails (What NOT to do)
**Security:**
- ❌ Never log sensitive data (passwords, tokens, PII)
- ✅ Must validate/sanitize all user inputs
- ✅ Must use parameterized queries (no string interpolation)
- ✅ Tokens/secrets must expire (max: Xh/Xd)

**Performance:**
- ❌ No N+1 queries (use eager loading/batching)
- ❌ No blocking operations in request handlers
- ✅ Response time must be <Xms for Y% of requests
- ✅ Must handle X concurrent users/requests

## Requirements
### Functional
- User can perform action A
- System responds with behavior B when condition C
- Data is processed/transformed according to rule D
- Integration with external service E works correctly

### Non-Functional
- Input validation: field constraints, formats, ranges
- Error handling: specific error codes/messages for failure cases
- Logging: what events/data to log at what level
- Monitoring: metrics/alerts to track

## Interfaces & Contracts
```python
# API Endpoints (or function signatures, CLI commands, etc.)
POST /api/v1/resource
  Headers: { "Authorization": "Bearer <token>" }
  Body: {
    "field1": "type (constraints)",
    "field2": number (min-max range)
  }
  Returns: 200 { "id": int, "status": str }
  Errors:
    400 - Invalid input (specific validation failure)
    401 - Unauthorized
    409 - Resource conflict

GET /api/v1/resource/{id}
  Returns: 200 { "id": int, "data": {...} }
  Errors: 404 - Not found
```

**Data Contracts:**
```python
# Database schema changes (if applicable)
Table: resource_name
  id: INTEGER PRIMARY KEY
  field1: VARCHAR(255) NOT NULL
  field2: INTEGER DEFAULT 0
  created_at: TIMESTAMP

  Indexes: field1_idx ON field1
  Foreign Keys: user_id REFERENCES users(id)
```

## Edge Cases & Risks
**Edge Cases to Handle:**
- **Empty/null inputs:** How should system respond?
- **Duplicate requests:** Idempotency handling
- **Concurrent modifications:** Race condition prevention
- **Resource limits:** Max file size, rate limits, quotas
- **Partial failures:** What happens if step 3 of 5 fails?

**Known Risks:**
- **Security risk:** Specific vulnerability and mitigation
- **Performance risk:** Bottleneck and solution approach
- **Data integrity risk:** Scenario and safeguard
- **Integration risk:** External dependency and fallback
