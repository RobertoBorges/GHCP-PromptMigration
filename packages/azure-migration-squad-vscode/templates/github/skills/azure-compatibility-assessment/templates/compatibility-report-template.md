# Azure Compatibility Assessment Report

**Application:** [APPLICATION_NAME]
**Date:** [DATE]
**Assessed By:** AWS to Azure Migration Agent

---

## Compatibility Score: [SCORE] / [MAX] — [RATING]

## Executive Summary

[Brief overview: Is this workload ready for Azure migration? What are the key findings?]

## Assessment Details

### 1. Runtime & Framework
- **Language:** [Language and version]
- **Framework:** [Framework and version]
- **Target Azure Platform:** [App Service / Container Apps / AKS / Functions]
- **Supported:** [Yes/No]
- **Action Required:** [None / Upgrade to version X]

### 2. OS & Architecture
- **Current OS:** [Linux/Windows]
- **Architecture:** [x86_64/ARM64]
- **Native Dependencies:** [List any]
- **Compatible:** [Yes/No/With changes]

### 3. Container Image (if applicable)
- **Base Image:** [Image name and tag]
- **Source Registry:** [ECR/DockerHub/Other]
- **Action Required:** [None / Push to ACR / Change base image]

### 4. Database Compatibility
- **Current Database:** [DynamoDB/RDS/Aurora/ElastiCache/etc.]
- **Target Database:** [Cosmos DB/Azure SQL/Azure Cache for Redis/etc.]
- **Feature Parity Issues:** [List any]
- **Data Model Changes Required:** [Yes/No — details]

### 5. AWS-Proprietary Features
| Feature Used | Azure Equivalent | Complexity | Action |
|-------------|-----------------|------------|--------|
| [Feature] | [Equivalent] | [🟢/🟡/🟠/🔴] | [Action] |

### 6. Third-Party Library Compatibility
| Library | Issue | Action |
|---------|-------|--------|
| [Library] | [Issue or "Compatible"] | [Action] |

### 7. Networking
- **Current Topology:** [VPC layout summary]
- **Azure Mapping:** [VNet plan summary]
- **Changes Required:** [List]

### 8. Authentication & Authorization
- **Current Auth:** [IAM/Cognito/etc.]
- **Target Auth:** [Entra ID/Managed Identity/etc.]
- **Migration Complexity:** [🟢/🟡/🟠/🔴]

## Remediation List

### 🔴 Critical (Must fix before migration)
- [ ] [Item 1]

### 🟠 High (Address during Phase 2)
- [ ] [Item 1]

### 🟡 Medium (Address during migration)
- [ ] [Item 1]

### 🟢 Low (Nice-to-have)
- [ ] [Item 1]

## Migration Readiness

- [ ] Runtime version supported on Azure
- [ ] Container image compatible (if applicable)
- [ ] Database migration path identified
- [ ] All AWS-proprietary features have Azure equivalents
- [ ] Third-party libraries are Azure-compatible
- [ ] Networking topology mapped
- [ ] Authentication migration path defined
- [ ] Remediation plan created

## Next Steps

1. Address all 🔴 Critical items
2. Proceed to Phase 2: Code Migration (`/phase2-migratecode`)
