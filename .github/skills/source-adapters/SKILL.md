---
name: source-adapters
description: |
  Routes discovery to source-environment guidance for Azure migrations. Use when input evidence identifies where the application currently lives: GitHub repository, ZIP or filesystem snapshot, on-premises server, AWS, GCP, Kubernetes cluster, container registry image, VMware RVTools export, Oracle Database estate, or unsupported specialist sources. Redirect mainframe, midrange, SaaS-embedded, proprietary, and uninspectable sources to unsupported escalation; do not claim code-level migration for them.
user-invocable: false
---

# Source Adapters Router

## When to use this skill

Use this router during intake and discovery when the user provides, describes, or points to the source environment for an application or portfolio. Source adapters determine what evidence can be collected, which probes are safe, what constraints apply, and which workload or stack adapters should run next.

This project does not perform first-class code migration for mainframe or midrange systems such as z/OS, IBM i / AS-400, COBOL, RPG, Natural, PL/I, CICS, IMS, or VSAM. Route those cases to unsupported escalation.

## Selection table

| Detected signal or evidence | Read this reference |
|---|---|
| Cloned repository, Git URL, GitHub project, local repo, mono-repo, multi-repo solution, source control history | [GitHub Repository](./references/source-github-repo.md) |
| ZIP, 7z, tar.gz, uploaded source bundle, local directory snapshot, extracted filesystem, quick source assessment | [ZIP / Filesystem Upload](./references/source-zip-filesystem.md) |
| Data-centre server, IIS, Windows Service, systemd, cron, scheduled task, packaged install, no public cloud source | [On-Premise Windows / Linux](./references/source-on-premise.md) |
| AWS account or inventory, EC2, ECS, EKS, Lambda, RDS, DynamoDB, SQS/SNS/EventBridge/Kinesis, VPC, IAM, CloudWatch, CloudFormation/CDK/Terraform | [Amazon Web Services](./references/source-aws.md) |
| GCP project or inventory, Compute Engine, Cloud Run, GKE, Cloud Functions, Cloud SQL, Pub/Sub, Cloud Storage, IAM | [Google Cloud Platform](./references/source-gcp.md) |
| Kubernetes cluster, namespace inventory, Deployments, StatefulSets, DaemonSets, Services, Ingress, ConfigMaps, Secrets, PVCs, Helm, GitOps | [Kubernetes Cluster](./references/source-kubernetes-cluster.md) |
| Registry path or image-only source from Docker Hub, ACR, ECR, GCR, GHCR, Harbor, Quay, JFrog; source code unavailable | [Container Registry](./references/source-container-registry.md) |
| RVTools XLSX, vCenter estate, VMware VM portfolio, bulk infrastructure assessment, app grouping from VM inventory | [VMware RVTools Export](./references/source-vmware-rvtools.md) |
| Oracle Database as primary/secondary datastore, Oracle Forms/Reports/APEX/EBS backing database, schemas, PL/SQL packages | [Oracle Database](./references/source-oracle-db.md) |
| SaaS-embedded customisation, Salesforce Apex, ServiceNow, SharePoint customisations, Power Platform, Dynamics plugins, SAP ABAP, Workday Studio, Lotus Notes, mainframe/midrange, COBOL, RPG, Natural, PL/I, proprietary archive, no inspectable artifact | [Unsupported / Specialist Escalation](./references/source-unsupported-escalation.md) |

## How to use

1. Select the source adapter from the strongest source-environment evidence. If multiple sources apply, read each relevant reference and record how the evidence relates.
2. Run only read-only probes described by the selected reference unless the user explicitly authorises more.
3. Feed discovered manifests, files, runtime details, and inventory to stack and workload routers.
4. Capture source constraints, confidence, risks, and target-Azure signals in the Discovery Dossier and Capability Matrix.
5. For unsupported sources, produce an escalation path and do not promise automated code migration.
