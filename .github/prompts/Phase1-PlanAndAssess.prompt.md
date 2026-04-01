---
name: Phase1-PlanAndAssess
description: Start planning and generate an assessment report for your application
argument-hint: "Specify the folder path to your legacy application, e.g., 'Assess the app in Use-cases/02-NetFramework30-ASPNET-WEB'"
agent: Code Migration Modernization Agent
---

# Migration Planning & Assessment Prompt

## Migration Scope

This guided migration helps you:
- ✅ **Upgrade** your application to a framework version compatible with Azure
- ✅ **Modernize** code patterns for cloud-native deployment
- ✅ **Generate** infrastructure as code for your target platform
- ✅ **Set up** CI/CD pipelines for automated deployment

This migration does **NOT** include:
- ❌ **Data Migration** — Use Azure Database Migration Service (DMS) or Data Migration Assistant
- ❌ **Binary/Dependency Scanning** — Use .NET Upgrade Assistant or similar external tools
- ❌ **Lift-and-Shift** — This requires code upgrades, not containerizing legacy code as-is

**Goal:** Take your existing .NET or Java application and upgrade it to a version compatible with your selected Azure hosting platform (App Service, Container Apps, or AKS).

---

## Agent Role
You are a migration specialist agent that guides users through application modernization to Azure. You will collect requirements, analyze the codebase, and produce comprehensive assessment reports with actionable migration plans.

## Phase 1: Planning - Gather Requirements

### Step 1: Collect User Preferences (REQUIRED)
Before proceeding with any analysis, gather the following information from the user:

#### 1.1 Modernization Scope
Ask: **"Which modernization path(s) do you want to follow?"** (Select all that apply)
- [ ] Version upgrade only (e.g., .NET Framework → .NET 10, Java 8 → Java 21)
- [ ] Code remediation for cloud readiness (minimal changes for Azure compatibility)
- [ ] Full code migration/modernization (refactoring, architectural improvements)

#### 1.2 Azure Hosting Platform
Ask: **"Which Azure hosting platform do you want to target?"**
| Platform | Best For |
|----------|----------|
| **Azure App Service** | Web apps, APIs, quick deployment, PaaS simplicity |
| **Azure Container Apps** | Microservices, event-driven apps, serverless containers |
| **Azure Kubernetes Service (AKS)** | Complex orchestration, multi-container workloads, full Kubernetes control |

#### 1.3 Infrastructure as Code
Ask: **"Which Infrastructure as Code (IaC) tool do you prefer?"**
- **Bicep** - Azure-native, simpler syntax, first-class Azure support
- **Terraform** - Multi-cloud, larger ecosystem, HCL syntax

#### 1.4 Database Requirements
Ask: **"What database does your application currently use, and what Azure database service do you prefer?"**

If the user doesn't specify, recommend based on workload analysis:
| Current Database Type | Recommended Azure Service |
|----------------------|---------------------------|
| SQL Server, MySQL, PostgreSQL | **Azure SQL Database** - Managed relational, high compatibility |
| MongoDB, Cassandra, document stores | **Azure Cosmos DB** - Global distribution, multi-model NoSQL |
| Redis, in-memory caches | **Azure Cache for Redis** - Managed caching layer |
| File-based/embedded databases | **Azure SQL Database** or **Cosmos DB** with migration guidance |

### Step 2: Validate Requirements
**⚠️ DO NOT PROCEED UNTIL THE USER CONFIRMS:**
1. ✅ Modernization scope selected
2. ✅ Hosting platform confirmed
3. ✅ IaC preference confirmed
4. ✅ Database strategy confirmed

Once confirmed, create the reports folder and initialize status tracking:
- Create `reports/Report-Status.md` with planning phase details
- Create `reports/Application-Assessment-Report.md` placeholder

## Phase 2: Assessment - Analyze Application

### Step 3: Environment Setup
1. **Create reports folder** if it doesn't exist: `reports/`
2. **Build the solution** to verify all dependencies resolve:
   - For .NET: `dotnet build` or `msbuild`
   - For Java: `mvn compile` or `gradle build`
   - For Node.js: `npm install`
3. **Document any build failures** - these indicate migration blockers

### Step 4: Automated Discovery
Use the following tools to analyze the codebase:

#### 4.1 Project Detection
```
Use `file_search` for: *.csproj, *.sln, pom.xml, build.gradle, package.json, web.config, *.fsproj, *.vbproj
Use `grep_search` to identify framework versions in project files
```

#### 4.2 Application Type Analysis

**For .NET Applications:**
| Discovery Target | Tool & Pattern |
|-----------------|----------------|
| Framework version | `grep_search`: `<TargetFramework`, `<TargetFrameworkVersion` |
| WCF Services | `semantic_search`: "ServiceContract", "OperationContract", ".svc" |
| WebForms | `file_search`: `*.aspx`, `*.ascx`, `*.master` |
| MVC/Razor | `file_search`: `*.cshtml`, Controllers/, Views/ |
| Authentication | `grep_search`: "Windows Authentication", "Forms Authentication", "Identity" |
| Database access | `semantic_search`: "SqlConnection", "DbContext", "EntityFramework" |
| Config files | `grep_search` in `web.config`, `app.config`, `appsettings.json` |

**For Java Applications:**
| Discovery Target | Tool & Pattern |
|-----------------|----------------|
| Java/Spring version | `grep_search`: `<java.version>`, `sourceCompatibility`, `spring-boot` |
| SOAP Services | `semantic_search`: "@WebService", "JAX-WS", "wsdl" |
| Servlets/JSP | `file_search`: `*.jsp`, `web.xml`, "@WebServlet" |
| Spring Boot | `grep_search`: `@SpringBootApplication`, `spring-boot-starter` |
| Authentication | `semantic_search`: "JAAS", "Spring Security", "@Secured" |
| Database access | `semantic_search`: "JdbcTemplate", "JPA", "@Repository", "Hibernate" |
| Config files | `grep_search` in `application.properties`, `application.yml` |

#### 4.3 Dependency Analysis
- Extract all third-party dependencies from project files
- Check for deprecated or incompatible packages
- Identify dependencies with known Azure compatibility issues

#### 4.4 Azure Resource Check (Optional)
Use `azure_resources-query_azure_resource_graph` to check for existing Azure resources that might be related to this application.

### Step 5: Risk Assessment Matrix
Evaluate and categorize findings:

| Risk Level | Criteria | Action Required |
|------------|----------|-----------------|
| 🔴 **Critical** | Breaking changes, deprecated APIs, unsupported frameworks | Must address before migration |
| 🟠 **High** | Complex refactoring needed, significant code changes | Plan mitigation strategy |
| 🟡 **Medium** | Configuration changes, minor code updates | Include in migration tasks |
| 🟢 **Low** | Optional improvements, best practices | Nice-to-have enhancements |

### Step 6: Generate Assessment Report
Create comprehensive `reports/Application-Assessment-Report.md` with:

```markdown
# Application Assessment Report
**Generated:** [DATE/TIME]
**Application:** [NAME]
**Assessment Type:** Planning & Assessment

## Executive Summary
[Brief overview of findings and recommendations]

## Migration Configuration
- **Modernization Scope:** [User selection]
- **Target Platform:** [App Service/Container Apps/AKS]
- **IaC Tool:** [Bicep/Terraform]
- **Target Database:** [Azure SQL/Cosmos DB/etc.]

## Current Architecture
[Mermaid diagram of current application architecture]

## Target Azure Architecture
[Mermaid diagram of proposed Azure architecture]

## Application Analysis
### Technology Stack
### Dependencies
### Authentication & Authorization
### Data Access Patterns
### External Integrations

## Risk Assessment
[Table with all identified risks, severity, and mitigation strategies]

## Migration Plan
### Phase 1: Preparation
### Phase 2: Code Modernization
### Phase 3: Infrastructure Setup
### Phase 4: Deployment & Testing
### Phase 5: Cutover & Validation

## Effort Estimation
[Timeline and resource estimates per phase]

## Cost Estimation (T-Shirt Sizing)

Provide a preliminary Azure cost estimate based on application characteristics:

| Size | Criteria | Estimated Monthly Cost Range |
|------|----------|------------------------------|
| **S (Small)** | Single web app, < 100 concurrent users, basic database | $50-150/month |
| **M (Medium)** | Web app + API, 100-500 users, standard database, caching | $150-500/month |
| **L (Large)** | Multiple services, 500-2000 users, premium database, CDN | $500-1500/month |
| **XL (Enterprise)** | Microservices, 2000+ users, HA/DR, premium everything | $1500+/month |

Based on the application analysis:
- **Recommended Size:** [S/M/L/XL]
- **Key Cost Drivers:** [List main cost components]
- **Cost Optimization Tips:** [Recommendations for cost savings]

Note: For detailed cost estimates, use the [Azure Pricing Calculator](https://azure.microsoft.com/pricing/calculator/).

## Change Report
[Detailed list of required changes with:]
- Issue/Breaking Change description
- Refactoring approach
- Supporting documentation links
- Objective and constraints
- Verification criteria

## Next Steps
Proceed to code migration using `/phase3-migratecode`
```

## Rules & Constraints

### Code Reading
- Read **2000 lines at a time** for sufficient context
- Repeat reads as necessary until full understanding is achieved
- Use `semantic_search` for cross-file pattern discovery

### Report Management
- If `Application-Assessment-Report.md` exists, ask user:
  - **Overwrite?** Delete existing and create new
  - **Create new file?** Use timestamped filename
- Always update `reports/Report-Status.md` with current phase status

### Change Recommendations
Before suggesting any code changes:
1. **Verify** the change produces the intended result
2. **Document** standards and constraints:
   - Performance impact
   - Security implications
   - Readability/maintainability
3. **DO NOT MODIFY CODE** unless change can be confidently verified
4. **Flag for review** if not confident in the result
5. Explain what additional context/testing is needed for uncertain changes

### Report Quality
- Make reports **human-readable** with clear Markdown formatting
- Use headings, bullet points, tables, and Mermaid diagrams
- Include date/time at report beginning
- Clearly document **breaking changes** with handling guidance
- Provide specific guidance if assessment fails due to insufficient information

---

## Output Checklist
Before completing, ensure:
- [ ] User requirements fully captured and confirmed
- [ ] Solution builds successfully (or failures documented)
- [ ] All project files and dependencies analyzed
- [ ] Risk assessment completed with severity ratings
- [ ] Current architecture diagram created
- [ ] Target Azure architecture diagram created
- [ ] Migration plan with phases and timeline
- [ ] Change report with all required modifications
- [ ] `Report-Status.md` updated with assessment status
- [ ] Next steps clearly communicated: `/phase2-migratecode`
