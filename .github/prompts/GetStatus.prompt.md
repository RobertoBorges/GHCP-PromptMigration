---
mode: agent
---
Retrieve status of the modernization process

# Rules for Status Tracking
- When this prompt is called, summarize the current migration status and direct the user to the status file for details. The status file is located at 'reports/Report-Status.md'.
- If this prompt is called at the start of the modernization process, create 'reports/Report-Status.md' with content indicating the modernization has not started yet.
- If the modernization process has started, ensure the status file contains the current status, including:
  - Project type (.NET or Java)
  - Current framework version
  - Target framework version
  - Selected Azure hosting platform (App Service, AKS, or Container Apps)
  - Selected Infrastructure as Code type (Bicep or Terraform)
  - Completed phases with timestamps:
    * Phase 1: Planning
    * Phase 2: Assessment
    * Phase 3: Code Migration
    * Phase 4: Infrastructure Generation
    * Phase 5: Deployment to Azure
    * Phase 6: CI/CD Pipeline Setup
  - Current phase in progress
  - Overall completion percentage
  - Quality scores for each completed phase
  - Any errors encountered and the last successful step
  - Security and compliance status
  - Performance metrics and baseline
  - Next recommended step with specific command
  
- Make the status file human-readable and in markdown format, with a structured layout:
  1. Executive Summary section at the top with key metrics
  2. Progress tracking with checkboxes and completion percentages
  3. Quality scores and metrics dashboard
  4. Detailed section for each phase with timestamps and outcomes
  5. Issues and risk section with severity levels if applicable
  6. Performance and security metrics
  7. Next steps section with specific commands and recommendations
  8. Resources and documentation links
  
- Use checkboxes in the status file to indicate steps that have been completed:
  - [x] Completed step
  - [ ] Pending step
  
- Include timestamps for each completed phase to help track the modernization timeline.
- Ensure the status report provides a clear view of the overall progress and any blocking issues.
- Format the report to be visually appealing and easy to scan quickly.
