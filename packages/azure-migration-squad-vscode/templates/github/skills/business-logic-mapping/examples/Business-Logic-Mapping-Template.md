# Business Logic Mapping Report Template

Use this template to track business logic during migration. Copy this file to `reports/Business-Logic-Mapping.md` and fill in the details.

---

# Business Logic Mapping Report

**Application:** [Application Name]
**Generated:** [Date/Time]
**Migration:** [Source Framework] → [Target Framework]
**Last Updated:** [Date/Time]

## Executive Summary

| Metric | Count | Percentage |
|--------|-------|------------|
| **Total Business Logic Items** | 0 | - |
| ✅ Migrated | 0 | 0% |
| ✅✅ Verified | 0 | 0% |
| 🔄 In Progress | 0 | 0% |
| ⬜ Pending | 0 | 0% |
| 🚫 Blocked | 0 | 0% |

## Migration Progress

```
[░░░░░░░░░░░░░░░░░░░░] 0% Complete
```

---

## Business Logic Inventory

### 📊 Calculations

Business rules involving mathematical computations, pricing, discounts, taxes, etc.

| ID | Name | Description | Source Location | Target Location | Status | Verified | Notes |
|----|------|-------------|-----------------|-----------------|--------|----------|-------|
| BL-CALC-001 | | | | | ⬜ Pending | ⬜ | |

### ✔️ Validations

Business rule validations, input validation, domain constraints.

| ID | Name | Description | Source Location | Target Location | Status | Verified | Notes |
|----|------|-------------|-----------------|-----------------|--------|----------|-------|
| BL-VAL-001 | | | | | ⬜ Pending | ⬜ | |

### 🔄 Workflows

Process flows, state machines, approval chains, multi-step operations.

| ID | Name | Description | Source Location | Target Location | Status | Verified | Notes |
|----|------|-------------|-----------------|-----------------|--------|----------|-------|
| BL-WF-001 | | | | | ⬜ Pending | ⬜ | |

### 🔀 Transformations

Data transformations, format conversions, aggregations, reporting logic.

| ID | Name | Description | Source Location | Target Location | Status | Verified | Notes |
|----|------|-------------|-----------------|-----------------|--------|----------|-------|
| BL-TRANS-001 | | | | | ⬜ Pending | ⬜ | |

### 🔌 Integrations

External system interactions, API calls, third-party services.

| ID | Name | Description | Source Location | Target Location | Status | Verified | Notes |
|----|------|-------------|-----------------|-----------------|--------|----------|-------|
| BL-INT-001 | | | | | ⬜ Pending | ⬜ | |

### 🔐 Authorization

Business-level permissions, role-based rules, ownership checks.

| ID | Name | Description | Source Location | Target Location | Status | Verified | Notes |
|----|------|-------------|-----------------|-----------------|--------|----------|-------|
| BL-AUTH-001 | | | | | ⬜ Pending | ⬜ | |

### 📧 Notifications

Event-driven communications, email triggers, alerts, messaging.

| ID | Name | Description | Source Location | Target Location | Status | Verified | Notes |
|----|------|-------------|-----------------|-----------------|--------|----------|-------|
| BL-NOTIF-001 | | | | | ⬜ Pending | ⬜ | |

### ⏰ Scheduling

Time-based business rules, batch jobs, scheduled tasks.

| ID | Name | Description | Source Location | Target Location | Status | Verified | Notes |
|----|------|-------------|-----------------|-----------------|--------|----------|-------|
| BL-SCHED-001 | | | | | ⬜ Pending | ⬜ | |

---

## Media and Static Assets

### Static Files

| Asset Type | Source Path | Target Path | Status | Notes |
|------------|-------------|-------------|--------|-------|
| Images | | | ⬜ Pending | |
| CSS | | | ⬜ Pending | |
| JavaScript | | | ⬜ Pending | |
| Fonts | | | ⬜ Pending | |
| Icons/Favicon | | | ⬜ Pending | |

### Dynamic Content

| Asset Type | Source Path | Target Path | Status | Notes |
|------------|-------------|-------------|--------|-------|
| User Uploads | | | ⬜ Pending | |
| Generated Files | | | ⬜ Pending | |
| Documents | | | ⬜ Pending | |

### Templates

| Template Type | Source Path | Target Path | Status | Notes |
|---------------|-------------|-------------|--------|-------|
| Email Templates | | | ⬜ Pending | |
| PDF Templates | | | ⬜ Pending | |
| Report Templates | | | ⬜ Pending | |

---

## Database Business Logic

Stored procedures, triggers, and views containing business logic.

| ID | Name | Type | Database | Status | Migration Approach | Notes |
|----|------|------|----------|--------|-------------------|-------|
| DB-001 | | Stored Proc | | ⬜ Pending | | |

---

## Modified Logic (Requires Documentation)

Items where business logic was intentionally changed during migration.

| ID | Original Logic | New Logic | Reason for Change | Approved By |
|----|----------------|-----------|-------------------|-------------|
| | | | | |

---

## Blocked Items

Items that cannot be migrated and require decisions.

| ID | Name | Blocker Description | Required Decision | Owner | Due Date |
|----|------|---------------------|-------------------|-------|----------|
| | | | | | |

---

## Verification Test Coverage

| Category | Total Items | With Tests | Coverage |
|----------|-------------|------------|----------|
| Calculations | 0 | 0 | 0% |
| Validations | 0 | 0 | 0% |
| Workflows | 0 | 0 | 0% |
| Transformations | 0 | 0 | 0% |
| Integrations | 0 | 0 | 0% |
| **Total** | 0 | 0 | 0% |

---

## Migration Notes

### Preserved As-Is
<!-- List items that required no changes -->

### Adapted for Modern Framework
<!-- List items that required adaptation with explanation -->

### Architectural Changes
<!-- List items that required redesign with justification -->

---

## Verification Checklist

### Calculations
- [ ] All calculations produce same results as legacy
- [ ] Edge cases tested (zero, negative, max values)
- [ ] Rounding behavior matches

### Validations
- [ ] All validations enforce same rules
- [ ] Error messages preserved or improved
- [ ] Validation order preserved where important

### Workflows
- [ ] All workflows follow same process flows
- [ ] State transitions match
- [ ] Error handling preserved

### Integrations
- [ ] All external APIs still called correctly
- [ ] Request/response formats compatible
- [ ] Error handling and retries preserved

### Media Assets
- [ ] All images accessible
- [ ] All CSS/JS loading correctly
- [ ] File paths updated throughout application
- [ ] Upload/download functionality working

---

## Status Legend

| Status | Icon | Description |
|--------|------|-------------|
| Pending | ⬜ | Not yet started |
| In Progress | 🔄 | Currently being migrated |
| Migrated | ✅ | Migration complete |
| Verified | ✅✅ | Verified with tests |
| Blocked | 🚫 | Cannot proceed, needs decision |
| Modified | ⚠️ | Logic intentionally changed |

---

## Revision History

| Date | Author | Changes |
|------|--------|---------|
| | | Initial mapping document created |
