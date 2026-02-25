# GHCP-PromptMigration Project Review Findings

**Review Date:** February 4, 2026  
**Reviewers:** GPT-5.2-Codex, Gemini 3 Pro, Claude Sonnet 4.5  
**Document Status:** Draft for Review

---

## Executive Summary

This document presents a comprehensive analysis of the GitHub Copilot Migration & Modernization for Azure project. The review evaluated the project's approach to helping users migrate legacy .NET and Java applications to Azure through a structured 5-phase process using custom prompts, agents, and skills.

**Overall Assessment:** The project provides a solid foundation for Azure migration with strong security defaults and well-structured phases. The prompts, skills, and agent are well-aligned with VS Code's customization features. Several enhancement opportunities were identified, along with clarifications on project scope.

### Scope Clarifications

Based on stakeholder input, the following items are **out of scope** for this project:

| Topic | Reason |
|-------|--------|
| **Data Migration** | Handled by other patterns/tools (Azure DMS, DMA) |
| **Binary/Dependency Scanning** | Handled by external tools (e.g., .NET Upgrade Assistant) |
| **Lift & Shift** | This project focuses on **upgrading to compatible versions**, not containerizing legacy as-is |

**Key Clarification:** This is NOT a lift-and-shift project. The goal is to take existing .NET or Java applications, upgrade them to versions compatible with the user's selected Azure hosting platform, and provide a guided step-by-step migration experience.

---

## Project Overview

The GHCP-PromptMigration project offers:

| Component | Description |
|-----------|-------------|
| **5 Migration Phases** | Planning → Code Migration → Infrastructure → Deployment → CI/CD |
| **7 Skills** | dotnet-modernization, java-modernization, azure-infrastructure, azure-containerization, wcf-to-rest-migration, config-transformation, migration-unit-testing |
| **7 Use Cases** | ASP Classic, .NET Framework 3.0-4.8, WCF 3.5, Java 8 API, BookShop, ContosoUniversity, PartsUnlimited |
| **Hosting Targets** | Azure App Service, Container Apps, AKS |

---

## Strengths Identified

### ✅ Security-First Approach
- **Managed Identities by default** - Eliminates credential management issues
- **Key Vault with RBAC only** - No legacy access policies
- **User consent required** for Azure resource modifications
- **Private endpoints** recommended for databases

### ✅ Modern Framework Patterns
- Comprehensive .NET Framework → .NET 8 LTS mapping
- Java EE → Spring Boot 3.x with Java 21 patterns
- WCF → REST API conversion with OpenAPI documentation
- EF6 → EF Core migration patterns

### ✅ Infrastructure Best Practices
- **Azure Verified Modules (AVM)** for Bicep templates
- Terraform best practices with proper provider configuration
- Multi-stage Dockerfiles for containerization
- Application Insights + Log Analytics integration

### ✅ Structured Workflow
- Clear phase-based progression
- Status tracking in `reports/Report-Status.md`
- Assessment reports with risk matrices
- Guardrails preventing unsafe operations

---

## VS Code Documentation Alignment

Based on review of the [VS Code Copilot Customization Documentation](https://code.visualstudio.com/docs/copilot/copilot-customization), the project is well-aligned with current features. Below are opportunities to leverage additional VS Code capabilities:

### Current Alignment ✅

| VS Code Feature | Project Implementation |
|-----------------|------------------------|
| **Custom Agents** (`.agent.md`) | ✅ `Code-Migration-Modernization.agent.md` with handoffs |
| **Prompt Files** (`.prompt.md`) | ✅ 7 phase prompts with proper frontmatter |
| **Agent Skills** (`SKILL.md`) | ✅ 7 skills with templates and patterns |
| **Handoffs** | ✅ Phase-to-phase transitions defined |
| **Model specification** | ✅ Claude Sonnet 4.5 specified |

### Enhancement Opportunities 🔧

| VS Code Feature | Current State | Recommendation |
|-----------------|---------------|----------------|
| **`argument-hint`** | Missing from prompts | Add hints like "Specify folder path to assess" |
| **Input variables** (`${input:var}`) | Not used | Add for dynamic user input during prompts |
| **`applyTo` glob patterns** | Not used in skills | Could help auto-load skills based on file type |
| **`agents` property** | Not used | Define allowed subagents for orchestration |
| **`user-invokable: false`** | Not used | Consider for helper-only agents |
| **Always-on instructions** | Missing `.github/copilot-instructions.md` | Add for global guardrails |

---

## Recommendations for Prompts and Skills

### 1. Add Always-On Instructions File

**Recommendation:** Create `.github/copilot-instructions.md` for global guardrails that apply to ALL chat interactions.

**Suggested content:**
```markdown
# Azure Migration Project Guidelines

## Scope
This project helps upgrade .NET and Java applications to Azure-compatible versions.
- This is NOT a lift-and-shift migration
- Focus on version upgrades compatible with selected Azure hosting platform
- Data migration is handled by external tools (Azure DMS, DMA)
- Binary/dependency scanning is handled by external tools (.NET Upgrade Assistant)

## Out of Scope
- Do NOT suggest lift-and-shift approaches
- Do NOT attempt data migration - refer users to Azure Database Migration Service
- Do NOT scan for binary dependencies - refer users to .NET Upgrade Assistant or similar tools

## Always Apply
- Prefer managed identities over connection strings
- Store secrets in Azure Key Vault
- Use PowerShell (pwsh) for commands
- Track progress in reports/Report-Status.md
```

<!-- REVIEWER: This creates global context so users don't get confused about project scope -->

---

### 2. Improve Agent Definition

**File:** `.github/agents/Code-Migration-Modernization.agent.md`

**Current Issues:**
- Missing `argument-hint` for better UX
- Missing `agents` property for subagent control
- Handoff `send` property defaults may cause confusion

**Recommended Changes:**

```yaml
---
name: Code Migration Modernization Agent
description: Helps users migrate and modernize legacy .NET and Java applications to Azure-compatible versions
argument-hint: "Example: 'Migrate my .NET Framework 4.8 app to .NET 8 for Azure App Service'"
tools: ['edit/editFiles', 'search/codebase', 'read/problems', ...]
model: Claude Sonnet 4.6 (copilot)
agents: ['*']  # Allow all subagents for flexibility
handoffs:
  - label: "Phase 1: Plan & Assess"
    agent: Code Migration Modernization Agent
    prompt: Phase1-PlanAndAssess.prompt.md
    send: false
    model: Claude Sonnet 4.6 (copilot)
  # ... rest of handoffs with explicit send: false
---
```

<!-- REVIEWER: Adding argument-hint improves discoverability. The example helps new users. -->

---

### 3. Enhance Prompt Files with Input Variables

**Issue:** Prompts don't leverage VS Code's input variable feature for dynamic user input.

**Recommendation for Phase 1 prompt:**

```yaml
---
name: Phase 1 - Plan and Assess
description: Start planning and generate an assessment report for your application
argument-hint: "Specify the folder containing your legacy application"
agent: Code Migration Modernization Agent
model: Claude Sonnet 4.6 (copilot)
tools: ['edit/editFiles', 'search/codebase', ...]
---

# Migration Planning & Assessment Prompt

Target Application: ${input:applicationPath:Enter the path to your application folder}
```

**Benefits:**
- Users get prompted for application path automatically
- Reduces back-and-forth clarification
- More consistent input format

---

### 4. Add Scope Clarification to Phase 1 Prompt

**Issue:** Users may expect data migration or lift-and-shift capabilities.

**Recommendation:** Add explicit scope section at the top of `Phase1-PlanAndAssess.prompt.md`:

```markdown
## Migration Scope

This guided migration helps you:
✅ Upgrade your application to a framework version compatible with Azure
✅ Modernize code patterns for cloud-native deployment
✅ Generate infrastructure as code for your target platform
✅ Set up CI/CD pipelines for automated deployment

This migration does NOT include:
❌ Data migration (use Azure Database Migration Service)
❌ Binary dependency scanning (use .NET Upgrade Assistant)
❌ Lift-and-shift without code changes

**Goal:** Take your existing .NET or Java application and upgrade it to a version compatible with your selected Azure hosting platform (App Service, Container Apps, or AKS).
```

---

### 5. Improve Skill Descriptions for Better Auto-Loading

**Issue:** Skill descriptions could be more specific about when to load.

**Recommendation:** Update `SKILL.md` descriptions to be more explicit:

| Skill | Current Description | Improved Description |
|-------|---------------------|---------------------|
| `dotnet-modernization` | ".NET Framework to .NET 8+ modernization patterns..." | "Use when the user has a .NET Framework 4.x application and needs to upgrade to .NET 8 LTS. Triggers on: .csproj files with TargetFrameworkVersion, web.config files, System.Web references." |
| `java-modernization` | "Java EE and legacy Java to modern Spring Boot..." | "Use when the user has a Java EE, J2EE, or legacy Java 8/11 application and needs to upgrade to Spring Boot 3.x with Java 21. Triggers on: pom.xml with javax.* dependencies, web.xml files, EJB annotations." |

---

### 6. Add Handoff Confirmation Step

**Issue:** Current handoffs proceed directly without explicit confirmation.

**Recommendation:** Add a confirmation step pattern to prompts:

```markdown
## Phase Completion Checklist

Before proceeding to the next phase, confirm:
- [ ] All assessment items reviewed
- [ ] Risk matrix understood
- [ ] Target platform confirmed
- [ ] IaC preference confirmed

When ready, use the handoff button or type `/phase2-migratecode` to continue.
```

---

### 7. Standardize Report Generation

**Issue:** Different prompts have slightly different report structures.

**Recommendation:** Create a `reports-template` skill or instructions file:

```markdown
---
name: reports-template
description: Standard report templates for migration documentation. Use when generating assessment reports, status reports, or deployment summaries.
---

# Report Standards

All reports should include:
1. **Header**: Date, application name, phase
2. **Executive Summary**: 3-5 sentences max
3. **Mermaid Diagrams**: Architecture before/after
4. **Tables**: Use for structured data
5. **Checklists**: Use for actionable items
6. **Next Steps**: Clear command to proceed
```

---

## Prompt-Specific Recommendations

### Phase 0 (Multi-Repo Assessment)

**Issue:** Very long prompt (700+ lines) may hit context limits.

**Recommendations:**
1. Split into modular sections that can be loaded on-demand
2. Add explicit instruction about context limitations
3. Reference external template files instead of embedding all templates

---

### Phase 1 (Plan and Assess)

**Current Strength:** Well-structured with clear steps and validation gates.

**Recommendations:**
1. Add scope clarification (see #4 above)
2. Add `argument-hint` to frontmatter
3. Consider adding recommended model for complex assessments

---

### Phase 2 (Migrate Code)

**Current Strength:** Good skill integration with dotnet/java modernization.

**Recommendations:**
1. Add explicit "upgrade path" guidance vs. rewrite
2. Clarify that this upgrades to compatible version, not lift-and-shift
3. Add validation checkpoints between major changes

---

### Phase 3-5

**Generally well-structured.** Minor recommendations:
- Phase 3: Add cost estimation reminder
- Phase 4: Add rollback guidance
- Phase 5: Add branch protection recommendations

---

## Skill-Specific Recommendations

### All Skills

**Recommendation:** Add `applyTo` or enhanced description patterns for better auto-loading:

```markdown
---
name: dotnet-modernization
description: |
  .NET Framework to .NET 8+ modernization patterns.
  **Triggers when:** User mentions .NET Framework, upgrading .NET, or has .csproj files with legacy TargetFrameworkVersion.
  **Use for:** web.config migration, EF6 to EF Core, authentication modernization.
---
```

---

### wcf-to-rest-migration

**Recommendation:** Add explicit note about this being a rewrite, not a compatibility layer:

```markdown
**Important:** WCF to REST migration requires rewriting service contracts as REST controllers.
This is a breaking change for existing WCF clients. Consider:
- Parallel deployment during transition
- Client SDK generation for REST consumers
- API versioning strategy
```

---

## Additional Recommendations from Model Feedback

### Addressed by Clarifications

| Model Feedback | Status | Notes |
|----------------|--------|-------|
| Data migration gap | **Out of Scope** | Add note to prompts referring to Azure DMS |
| Binary scanning | **Out of Scope** | Add note referring to .NET Upgrade Assistant |
| Windows vs Linux confusion | **Clarified** | Not lift-and-shift; upgrade to compatible version |

### Still Valid Recommendations

| Feedback | Priority | Action |
|----------|----------|--------|
| Cost estimation in Phase 1 | Medium | Add T-shirt sizing guidance |
| Integration testing patterns | Medium | Expand migration-unit-testing skill |
| Strangler Fig pattern | Low | Document for large monoliths |
| Observability code changes | Medium | Add logging migration to skills |

---

## Priority Actions Summary

### High Priority (Immediate) ✅ COMPLETED

| # | Action | File(s) Updated | Status |
|---|--------|-----------------|--------|
| 1 | Create `.github/copilot-instructions.md` with global guardrails | New file created | ✅ Done |
| 2 | Add scope clarification to Phase 1 prompt | `Phase1-PlanAndAssess.prompt.md` | ✅ Done |
| 3 | Add `argument-hint` to all prompts | All 7 `.prompt.md` files | ✅ Done |
| 4 | Add out-of-scope notes to agent definition | `Code-Migration-Modernization.agent.md` | ✅ Done |

### Medium Priority (Next Sprint) ✅ COMPLETED

| # | Action | File(s) Updated | Status |
|---|--------|-----------------|--------|
| 5 | Improve skill descriptions for better auto-loading | All 7 `SKILL.md` files | ✅ Done |
| 6 | Add cost estimation guidance to Phase 1 | `Phase1-PlanAndAssess.prompt.md` | ✅ Done |

### Low Priority (Future)

| # | Action | File(s) to Update | Status |
|---|--------|-------------------|--------|
| 7 | Split Phase 0 into modular components | `Phase0-Multi-repo-assessment.prompt.md` | Pending |
| 8 | Add Strangler Fig pattern documentation | New optional skill | Pending |
| 9 | Add logging migration patterns | `dotnet-modernization`, `java-modernization` | Pending |

---

## Appendix A: Files Reviewed

| Path | Purpose |
|------|---------|
| `.github/agents/Code-Migration-Modernization.agent.md` | Main agent definition |
| `.github/prompts/Phase0-Multi-repo-assessment.prompt.md` | Multi-repo assessment |
| `.github/prompts/Phase1-PlanAndAssess.prompt.md` | Planning phase workflow |
| `.github/prompts/Phase2-MigrateCode.prompt.md` | Code migration workflow |
| `.github/prompts/Phase3-GenerateInfra.prompt.md` | Infrastructure generation |
| `.github/prompts/Phase4-DeployToAzure.prompt.md` | Deployment workflow |
| `.github/prompts/Phase5-SetupCICD.prompt.md` | CI/CD setup |
| `.github/prompts/GetStatus.prompt.md` | Status tracking |
| `.github/skills/dotnet-modernization/SKILL.md` | .NET patterns |
| `.github/skills/java-modernization/SKILL.md` | Java patterns |
| `.github/skills/azure-infrastructure/SKILL.md` | IaC patterns |
| `.github/skills/wcf-to-rest-migration/SKILL.md` | WCF migration patterns |
| `README.md` | Project documentation |

---

## Appendix B: VS Code Documentation References

| Topic | URL |
|-------|-----|
| Copilot Customization Overview | https://code.visualstudio.com/docs/copilot/copilot-customization |
| Custom Agents | https://code.visualstudio.com/docs/copilot/customization/custom-agents |
| Agent Skills | https://code.visualstudio.com/docs/copilot/customization/agent-skills |
| Prompt Files | https://code.visualstudio.com/docs/copilot/customization/prompt-files |
| Custom Instructions | https://code.visualstudio.com/docs/copilot/customization/custom-instructions |

---

## Appendix C: Model Feedback Summary

### GPT-5.2-Codex Feedback
- Add data migration/ETL patterns → **Out of scope**
- Add observability/telemetry migration → **Valid, medium priority**
- Well-architected review integration → **Good suggestion**
- Cost governance emphasis → **Added to recommendations**
- Decision trees for common app types → **Good UX suggestion**

### Gemini 3 Pro Feedback
- Database data migration gap → **Out of scope**
- Integration & background tasks → **Valid, but may need separate skill**
- Frontend modernization → **Valid observation**
- Secret scanning pre-migration → **Out of scope**
- Windows vs Linux path → **Clarified: not lift-and-shift**
- Cost estimation → **Added to recommendations**
- Strangler Fig pattern → **Added as low priority**

---

## Document Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2026-02-04 | AI Review Team | Initial findings document |
| 1.1 | 2026-02-04 | AI Review Team | Added VS Code alignment, scope clarifications, prompt recommendations |

---

<!-- 
REVIEWER COMMENTS SECTION
========================

@reviewer1: The scope clarifications are important - please confirm these align with
project goals before we update the prompts.

@reviewer2: The VS Code documentation shows we can use `agents` property to control
subagent access. Should we restrict this or keep it open?

@reviewer3: The always-on instructions file (.github/copilot-instructions.md) would
provide consistent guardrails. Recommend implementing this first.

@all: The argument-hint additions would significantly improve UX. These are quick wins.

TODO: 
- [ ] Review and approve scope clarifications
- [ ] Prioritize action items
- [ ] Assign owners for high-priority changes
-->
