# AWS Dependency Map

> **Generated:** `<YYYY-MM-DD HH:mm UTC>`
> **Accounts:** `<list>` · **Edges:** `<n>` (`<n>` HIGH, `<n>` MEDIUM, `<n>` LOW)
> Machine-readable edge list: `reports/raw/<account-id>/_edges.json`

**Legend**

| Rendering | Meaning |
|-----------|---------|
| Solid arrow `-->` | HIGH confidence — explicit identifier in the API response |
| Dotted arrow `-.->` | MEDIUM confidence — inferred, evidence stated in the edge table |
| Node labeled `EXTERNAL` | Account outside the organization |
| Red-labeled edge | Internet-exposed path |

---

## 1. Account Hierarchy

```mermaid
graph TD
    ROOT["AWS Organization"]
```

---

## 2. Region Distribution

```mermaid
graph LR
    subgraph R1["region - n resources"]
        X["services"]
    end
```

---

## 3. Application Maps

Repeat one diagram per identified application.

### 3.1 `<application-name>`

**Account:** `<id>` · **Environment:** `<env>` · **Owner:** `<owner>` · **Est. cost:** `$<amount>`/month

```mermaid
graph LR
    A["entry point"]
    B["compute"]
    C["data"]
    A --> B
    B --> C
```

| Resource | Type | Role in the application | Owner |
|----------|------|------------------------|-------|
| | | | |

**Inferred edges in this map**

| Source | Target | Evidence | Confidence |
|--------|--------|----------|-----------|
| | | | |

---

## 4. Data Flow

```mermaid
graph LR
    SRC["source"]
    STORE["store"]
    SRC --> STORE
```

| Flow | From | To | Data | Cross-region | Cross-account | Encrypted in transit |
|------|------|----|------|--------------|---------------|----------------------|
| | | | | | | |

---

## 5. Cross-Account & Cross-Region Edges

```mermaid
graph LR
    A1["account A"]
    A2["account B"]
    A1 --> A2
```

| Source Account | Target Account | Mechanism | Detail | External? | Risk |
|----------------|----------------|-----------|--------|-----------|------|
| | | IAM trust / peering / TGW / S3 policy / KMS grant / RAM | | | |

---

## 6. Internet Exposure Paths

```mermaid
graph LR
    NET["Internet 0.0.0.0/0"]
    T["target"]
    NET --> T
```

| # | Entry | Path | Terminal resource | Auth | Severity |
|---|-------|------|-------------------|------|----------|
| | | | | | |

---

## 7. Full Edge Table

| Source | Target | Edge Type | Evidence | Confidence | Cross-Acct | Cross-Region | Application |
|--------|--------|-----------|----------|-----------|-----------|--------------|-------------|
| | | | | | | | |

---

## 8. Orphaned Resources

Resources with **zero HIGH-confidence inbound and outbound edges** — decommissioning candidates.

| Resource | Type | Account | Region | Created | Created By | Owner | Est. monthly cost | Orphan signal |
|----------|------|---------|--------|---------|-----------|-------|-------------------|---------------|
| | | | | | | | | |

**Total reclaimable:** `$<amount>`/month

---

## 9. Unclassified Resources

Resources that could not be assigned to an application.

| Count | Est. monthly cost | Share of estate |
|-------|-------------------|-----------------|
| | | |

| Resource | Type | Account | Region | Created | Owner | Why unclassified |
|----------|------|---------|--------|---------|-------|------------------|
| | | | | | | No tag, no stack, no edges |
