# Skill: Source Adapter — ZIP / Filesystem Upload

> Characterizes an application whose source comes to us as a ZIP archive, tarball, or a directory the user pasted on the filesystem. No version control, no live system.

## When to Use

- User attaches a ZIP / 7z / tar.gz of source
- User points at a local directory ("here's a snapshot")
- Application is from a system we cannot access (and the user did the extraction for us)
- Quick assessments where the user just wants a look

## Inputs

- Path to the archive (`*.zip`, `*.tar.gz`, `*.tar.bz2`, `*.7z`, `*.rar`), OR
- Path to an already-extracted directory
- Optional: a `README` or note from the user about origin and what's missing

## Probes

### 1. Extract (if archive)

- `Expand-Archive -Path <zip> -DestinationPath <dest>` (PowerShell ZIP)
- `tar -xzf <tgz> -C <dest>` (tarball)
- `7z x <archive> -o<dest>` (7z / RAR)
- Preserve original timestamps where possible

### 2. Top-level shape

- `Get-ChildItem -Path <dest> -Depth 2` (PowerShell) or `find <dest> -maxdepth 2 -type d` (Unix)
- Look for canonical roots: `src/`, `app/`, `web/`, `WebContent/`, `WEB-INF/`, `wwwroot/`, `htdocs/`
- Read top-level `README*`, `CHANGELOG*`, `LICENSE`, `*.txt`

### 3. Manifest census (feed `stack-detection`)

Same as `source-github-repo` — find all build manifests across the tree:

- `*.sln`, `*.csproj`, `*.vbproj`, `pom.xml`, `build.gradle*`, `package.json`, `requirements.txt`, `pyproject.toml`, `composer.json`, `Gemfile`, `go.mod`, `Cargo.toml`, `Makefile`, `CMakeLists.txt`, `mix.exs`, `*.pbproj`, `*.dpr`, `*.vbp`, `*.cbl`

### 4. Detect missing pieces

- Are there `*.suo`, `*.user`, `.idea/`, `.vs/`, `.gradle/` files? → user accidentally included IDE state; safe to ignore
- Are there compiled artifacts (`*.dll`, `*.jar`, `*.war`, `*.class`, `*.exe`, `*.pyc`, `node_modules/`, `vendor/`)? → user shipped binaries; source may also be present (check `*.cs`, `*.java`, etc.) or this may be a binary-only drop
- Is there a `.git/`? → user shipped a Git clone; treat as `source-github-repo` instead and re-run

### 5. Configuration files

- `appsettings*.json`, `application*.yml`, `web.config`, `app.config`, `.env*`, `config/`
- Grep for secrets — same list as `source-github-repo` (passwords, tokens, AWS keys, etc.)

### 6. Database scripts

- `*.sql`, `migrations/`, `db/`, `database/`
- May be the only data-side evidence available

### 7. Documentation / artifacts

- `architecture/`, `docs/`, `*.drawio`, `*.png` (diagrams)
- Original-system clues: filenames mentioning hostnames, internal URLs, account IDs

## Output Evidence

```yaml
source:
  primary_adapter: source-zip-filesystem
  access_method: filesystem-path
  evidence_confidence: <high if source is complete; medium if partial; low if binaries-only>
  evidence_paths:
    - <archive path>
    - <extracted root>
    - <key manifest paths>
  notes: |
    - Archive type: <zip | tgz | 7z | rar | unzipped directory>
    - Extracted size: <MB>
    - Manifests found: <count and list>
    - Tests included: <yes/no>
    - Config files: <count>
    - Database scripts: <count>
    - Compiled artifacts present: <yes/no>
    - .git directory present: <yes/no — if yes, switch adapter>
    - Documentation: <yes/no>
    - Apparent original system: <hostname/url hints from configs>
```

## Migration Constraints / Risks

- **Snapshot is point-in-time.** Whatever the user gave us is what we have — no incremental fetch later without going back to the source system.
- **Provenance is weak.** No commit history, no author trail. For audit-sensitive engagements, flag for Security Auditor.
- **Binary-only drops.** If `*.cs` / `*.java` / source equivalents are missing, treat as `risk_flags: [no-source-code-available]` and route through Branch 2 of `migration-strategy-decision-tree`.
- **Hostnames + IPs in configs.** Same risk as on-premise: grep configs for the source system's own hostname/IPs/drive letters.
- **Secrets in configs.** Identical risk as `source-github-repo`. Grep and flag.
- **Missing build context.** No CI history, no shared registry — Phase 5 may need to rebuild the pipeline assumption from scratch.
- **Dependencies vendored vs declared.** Some snapshots include `vendor/` or `node_modules/` checked in; others rely on package managers. Check whether dependencies can actually be restored from the manifest alone.

## Workload Pattern Inference

Same as `source-github-repo`. Use entry points + scheduler signals.

## Target Azure Mapping

This adapter is target-agnostic. The mapping comes from the detected stack and workload pattern, not from the fact that source arrived as a ZIP.

## Anti-Patterns

- Don't ignore the README. Snapshots often come with a hand-written context note.
- Don't classify the project by the largest folder — `node_modules/` and `vendor/` can dwarf real source.
- Don't proceed if a `.git/` is present. Switch to `source-github-repo` — it's a strictly better adapter (history + branches + commits + provenance).
- Don't assume the ZIP is the whole app. Ask: "Is there a database / config server / external dependency that wasn't included?"

## Output Checklist

- [ ] Archive extracted to a clean directory
- [ ] Top-level shape captured
- [ ] All build manifests inventoried (feed `stack-detection`)
- [ ] Config files identified
- [ ] Secrets-in-source grep performed
- [ ] Compiled-artifacts vs source ratio captured
- [ ] Database scripts noted
- [ ] Documentation noted
- [ ] User context note read and respected
- [ ] Snapshot-only nature flagged (no incremental sync possible)
- [ ] Source-completeness assessment captured (`high` / `medium` / `low`)
