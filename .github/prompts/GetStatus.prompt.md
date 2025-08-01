---
mode: agent
---
Retrieve status of the modernization process

# Rules for Status Tracking
- When this prompt is called, call out the current status of the migration/modernization process, and direct the user to the status file for more details. The status file is located in the 'reports' folder and is named 'modernization_status.md'.
- If this prompt is called at the start of the modernization process, create the status file in the 'reports' folder with content that says the modernization has not started yet.
- If the modernization process has started, ensure the status file contains the current status, including:
  - Project type (.NET or Java)
  - Current framework version
  - Target framework version
  - Selected Azure hosting platform (App Service, AKS, or Container Apps)
  - Completed phases
  - Current phase
  - Any errors encountered and the last successful step
  - Next recommended step
  
- Make the status file human-readable and in markdown format, with a structured layout:
  1. Summary section at the top
  2. Progress tracking with checkboxes
  3. Details section for each phase
  4. Issues section if applicable
  5. Next steps section
  
- Use checkboxes in the status file to indicate steps that have been completed:
  - [x] Completed step
  - [ ] Pending step
  
- Include timestamps for each completed phase to help track the modernization timeline.
- Ensure the status report provides a clear view of the overall progress and any blocking issues.
- Format the report to be visually appealing and easy to scan quickly.
