# Application-Pillar Slide Specifications — Reference

Slide specs and field references that apply ONLY when the Application pillar is detected. Loaded by the `migration-strategy-report` skill conditionally.

---

## Application Input Fields

The report adapts based on which fields are present. Not all fields are needed — the report uses whatever is available.

**Application Fields:**
Application Name, Business Capability, Criticality Rating, Architecture Tier, Tech Stack/Framework, Database Platform, Operating System, Obsolescence Scores (Tech/DBMS/OS), Migration Complexity, Integration Count, Server Count, Containerized, Regulatory Requirements, RPO/RTO, Application Owner/BU, Vendor/Internal, Migration Phase, Pilot Flag.

---

## Slide 3: Technology Stack Landscape

- Application Frameworks: horizontal bars per technology
- Database Platforms: horizontal bars
- Operating Systems: horizontal bars with EOL markers

---

## Slide 4: Technical Obsolescence Assessment

- Callout: count of "Very High" (5) apps across multiple dimensions
- Three-column tables: Tech Stack, DBMS, OS score distributions
- Critical Technology Debt table: EOL tech → affected count → risk badge → target state

---

## Slide 5: Migration Strategy — 6 Rs (Application Portfolio)

**Include when:** Applications pillar is detected. The 6 Rs framework applies to application-level migration decisions.
**Skip when:** Pure infrastructure-only or database-only scenarios — the Factory/ISD / Partner split (Slide 5b) and DB target selection matrix (Slide 4e) serve as the equivalent strategy distribution.

- Six strategy cards with app counts (Rehost, Replatform, Refactor, Replace, Retire, Retain)
- **REQUIRED:** Use the CAF-aligned classification algorithm defined in `classification-algorithm.md`. Do NOT use LLM judgment — apply the CAF business-driver indicators mechanically.
- **REQUIRED:** Default to 6 Rs (Rehost, Replatform, Refactor, Replace, Retire, Retain). Expand to 8 Rs only if the customer explicitly requests it.
- **REQUIRED:** verification line showing math: all strategy counts must sum to the In-Scope total
- **REQUIRED:** At the end of the slide, include a **Methodology** footnote/callout that reads: *"Classification methodology: Each application was assigned a migration strategy by evaluating its business driver — the gap between current state and desired future state — against the [Microsoft Cloud Adoption Framework (CAF) migration strategy guidance](https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/plan/select-cloud-migration-strategy). Indicators used include application criticality, complexity, integration count, tech stack, architecture type, OS/DB end-of-support status, and containerization readiness. The priority evaluation order follows CAF recommendations: Retire → Retain → Replace → Refactor → Replatform → Rehost (default)."*

---

## Slide 7: Application Grouping by Business Capability

- Top 20 capabilities ranked by app count with primary technologies
- Key Insight callout

---

## Slide 8: Phase 1 Pilot — Application Detail

- Selection criteria callout
- Detailed table: 10–15 apps with full tech details

---

## Slide 9: Technology Modernization Tracks

- Parallel workstreams table: track, scope, current state, target state, key apps
- Priority and dependency callout
