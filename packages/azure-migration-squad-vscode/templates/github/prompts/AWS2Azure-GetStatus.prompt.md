---
name: Get Migration Status
description: Check the current AWS-to-Azure migration status and progress
argument-hint: "Just run this command to see current status"
agent: AWS to Azure Migration Agent
---

Retrieve status of the AWS-to-Azure migration process

# Rules for Status Tracking
- When this prompt is called, summarize the current migration status and direct the user to the status file for details. The status file is located at `reports/Report-Status.md`.
- If this prompt is called at the start of the migration process, create `reports/Report-Status.md` with content indicating the migration has not started yet.
- If the migration process has started, ensure the status file contains the current status, including:

## Migration Context
  - **Source AWS Services**: List of AWS services detected in the workload (e.g., EC2, RDS, S3, Lambda, SQS, DynamoDB, etc.)
  - **Target Azure Services**: List of Azure services selected with mapping (e.g., EC2 → App Service, RDS → Azure SQL, S3 → Blob Storage)
  - **Migration Scope**: Service migration / Full workload migration / Infrastructure only
  - **Project type**: .NET or Java (if applicable)
  - **Selected Azure hosting platform**: App Service, Container Apps, AKS, or Functions
  - **Selected Infrastructure as Code type**: Bicep or Terraform

## Migration Progress
  - **Azure Compatibility Score**: Score from Phase 1 assessment (percentage of AWS services with direct Azure equivalents)
  - **SDK Migration Progress**: Per language, per AWS service (e.g., S3 SDK → Azure.Storage.Blobs: 100%, SQS SDK → Azure.Messaging.ServiceBus: 75%)
  - **Infrastructure Conversion Status**: CloudFormation/CDK → Bicep/Terraform conversion progress
  - **Identity Migration Status**: IAM Roles/Policies → Entra ID + Managed Identities + RBAC
  - **Networking Migration Status**: VPC/Subnets/Security Groups → VNet/Subnets/NSGs
  - **Observability Migration Status**: CloudWatch Metrics/Logs/Alarms → Azure Monitor/Application Insights/Log Analytics
  - **CI/CD Migration Status**: CodePipeline/CodeBuild → GitHub Actions or Azure DevOps
  - **Cutover Readiness**: DNS plan ready / Certificates provisioned / Identity cutover tested / Rollback plan documented

## Phase Completion
  Track with checkboxes and timestamps:
  - [ ] Phase 0: Multi-Repo Assessment — `timestamp`
  - [ ] Phase 1: Planning & Assessment — `timestamp`
  - [ ] Phase 2: Code Migration (AWS SDK → Azure SDK) — `timestamp`
  - [ ] Phase 3: Infrastructure Generation (CloudFormation/CDK → Bicep/Terraform) — `timestamp`
  - [ ] Phase 4: Migration Cutover & Deployment — `timestamp`
  - [ ] Phase 5: CI/CD Pipeline Migration — `timestamp`

  Use `[x]` for completed phases with actual timestamps.

  - Current phase in progress
  - Overall completion percentage

## Quality and Risk
  - Quality scores for each completed phase
  - **Blockers and Risks**: Any issues preventing progress, with severity levels
  - **Data Migration Needs**: Document any data migration requirements (out of scope for this tool — refer to Azure Database Migration Service / DMS / Data Migration Assistant / DMA)
  - Security and compliance status
  - Performance metrics and AWS vs Azure baseline comparison
  - Any errors encountered and the last successful step

## Recommendations
  - **Next Recommended Step**: Specific command to run next (e.g., `/AWS2Azure-phase2-migratecode`, `/AWS2Azure-phase3-generateinfra`, etc.)

## Formatting Standards
- Make the status file human-readable and in markdown format, with a structured layout:
  1. Executive Summary section at the top with key metrics and AWS→Azure mapping overview
  2. Progress tracking with checkboxes and completion percentages for each migration dimension
  3. Quality scores and metrics dashboard
  4. Detailed section for each phase with timestamps and outcomes
  5. Blockers, risks, and data migration needs section with severity levels
  6. Performance and security metrics (AWS baseline vs Azure current)
  7. Next steps section with specific commands and recommendations
  8. Resources and documentation links

- Use checkboxes to indicate steps that have been completed:
  - [x] Completed step
  - [ ] Pending step

- Include timestamps for each completed phase to help track the migration timeline.
- Ensure the status report provides a clear view of the overall progress and any blocking issues.
- Format the report to be visually appealing and easy to scan quickly.
