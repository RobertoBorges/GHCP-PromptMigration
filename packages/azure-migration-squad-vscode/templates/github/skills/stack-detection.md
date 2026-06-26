# Skill: Stack Detection

> Generic, language-agnostic fingerprinting of any application's primary language(s), framework(s), build system, and runtime version.

## When to Use

- During discovery, when the user says "I don't know — probe it"
- Whenever stack hints are missing or low-confidence
- After loading a source adapter that exposes file contents
- To validate user-stated stack against actual evidence

## Inputs

- A file system path, repository root, or container image manifest
- Optional: a stack hint to validate

## Output

```yaml
stack:
  primary: <language>
  primary_framework: <framework or null>
  primary_evidence:
    - <file path or count>
  primary_confidence: <high | medium | low>
  secondary: [<language>...]
  build_system: <msbuild | maven | gradle | npm | pnpm | yarn | pip | poetry | composer | cargo | go-modules | bundler | make | cmake | sbt | mix | ...>
  runtime_version_detected: <e.g., dotnet8.0, java-17, python-3.11, node-20>
  package_manifests_found:
    - <path>
```

## Detection Order

Apply in this order to maximize signal:

### 1. Manifest-first detection (fastest, highest confidence)

| Manifest file | Implies |
|---------------|---------|
| `*.csproj`, `*.sln`, `*.vbproj`, `*.fsproj` | `.NET` (read `TargetFramework` for version) |
| `global.json`, `nuget.config` | `.NET` ecosystem |
| `pom.xml` | Java / Maven (read `<java.version>` or `<maven.compiler.source>`) |
| `build.gradle`, `build.gradle.kts`, `settings.gradle` | Java/Kotlin / Gradle |
| `package.json` + `node_modules` lockfile | Node.js (read `engines.node`) |
| `pnpm-lock.yaml`, `yarn.lock` | Node.js with that package manager |
| `requirements.txt`, `pyproject.toml`, `Pipfile`, `setup.py`, `setup.cfg` | Python |
| `composer.json`, `composer.lock` | PHP (read `require.php`) |
| `Gemfile`, `Gemfile.lock`, `.ruby-version` | Ruby |
| `go.mod`, `go.sum` | Go (read `go` directive for version) |
| `Cargo.toml`, `Cargo.lock` | Rust (read `rust-version`) |
| `mix.exs` | Elixir |
| `build.sbt` | Scala |
| `*.cabal`, `stack.yaml` | Haskell |
| `cpanfile`, `Makefile.PL` | Perl |
| `CMakeLists.txt`, `Makefile` (with `.c`/`.cpp`) | C/C++ |
| `*.pbproj`, `*.pbl` | PowerBuilder |
| `*.dpr`, `*.dpk` | Delphi |
| `*.vbp` | VB6 |
| `*.cbl`, `*.cob`, `JCL` files | COBOL / mainframe |
| `*.fmb`, `*.fmx`, `*.mmb` | Oracle Forms |

If a manifest is found and parsed, `primary_confidence: high`.

### 2. File-extension share fallback

If no manifest, or for secondary language detection, count source files by extension:

| Extension | Language |
|-----------|----------|
| `.cs`, `.vb`, `.fs`, `.cshtml`, `.razor`, `.aspx`, `.ascx`, `.asax`, `.asmx` | .NET (with sub-flavor) |
| `.java`, `.jsp`, `.jspx`, `.kt`, `.kts`, `.scala`, `.groovy` | JVM family |
| `.py`, `.pyx`, `.ipynb` | Python |
| `.js`, `.mjs`, `.cjs`, `.ts`, `.tsx`, `.jsx`, `.vue`, `.svelte` | Node.js / browser |
| `.php`, `.phtml`, `.phar` | PHP |
| `.rb`, `.erb`, `.rake` | Ruby |
| `.go` | Go |
| `.rs` | Rust |
| `.pl`, `.pm`, `.t`, `.psgi` | Perl |
| `.c`, `.h`, `.cpp`, `.hpp`, `.cc`, `.cxx` | C / C++ |
| `.cbl`, `.cob`, `.cpy` | COBOL |
| `.fmb`, `.fmx`, `.mmb`, `.olb`, `.pll` | Oracle Forms |
| `.pbl`, `.pbt`, `.pbw` | PowerBuilder |
| `.dpr`, `.pas`, `.dpk`, `.dfm` | Delphi |
| `.vbp`, `.frm`, `.bas`, `.cls` | VB6 |
| `.asp`, `.asa` | Classic ASP |
| `.svc`, `.xamlx` | WCF / WF |

Compute share: `language_share = file_count(language) / total_source_files`.

- Primary = highest share above 30%
- Secondary = any language above 5%
- If no language dominates, `primary_confidence: low`

### 3. Framework detection (within a language)

| Language | Framework signals |
|----------|-------------------|
| .NET | `TargetFramework` value in csproj; `Microsoft.AspNetCore.*` (ASP.NET Core); `System.Web` (ASP.NET classic); `Microsoft.EntityFrameworkCore` (EF Core); `EntityFramework` (EF6); `System.ServiceModel.*` (WCF); `WebForms` if `.aspx` present |
| Java | `spring-boot-starter-*` (Spring Boot); `spring-context` (Spring); `javax.ejb` (EJB); `javax.servlet` (Servlet); `jakarta.*` (Jakarta EE); `org.hibernate.*` (Hibernate); `play.api.*` (Play); `io.quarkus.*` (Quarkus); `io.micronaut.*` (Micronaut) |
| Python | `django` in requirements (Django); `flask` (Flask); `fastapi` (FastAPI); `tornado`; `airflow` (data pipeline); `streamlit` (data app); `numpy/pandas/scikit/torch` (data/ML); `celery` (event-driven) |
| Node.js | `express` (Express); `next` (Next.js); `nuxt` (Nuxt); `nestjs` (NestJS); `koa`; `fastify`; `react`/`vue`/`angular`/`svelte` (UI frameworks); `socket.io` (real-time) |
| PHP | `laravel/framework` (Laravel); `symfony/*` (Symfony); `cakephp/*` (CakePHP); `codeigniter4/*` (CodeIgniter); `magento/*` (Magento); `wordpress` markers (WordPress) |
| Ruby | `rails` in Gemfile (Rails); `sinatra` (Sinatra); `hanami` (Hanami); `padrino` |
| Go | `github.com/gin-gonic/gin` (Gin); `github.com/labstack/echo` (Echo); `github.com/gofiber/fiber` (Fiber); `net/http` only (stdlib server) |

### 4. Build system detection

Already implied by manifest, but for hybrid repos look for:

- `*.sln` + `Directory.Build.props` → MSBuild
- `mvnw`, `mvnw.cmd` → Maven wrapper
- `gradlew`, `gradlew.bat` → Gradle wrapper
- `Makefile` with `.PHONY` and language source → make
- `Dockerfile` only → containerized build (capture base image as runtime fingerprint)

### 5. Runtime version detection

- .NET: read `TargetFramework` (`net48`, `netcoreapp3.1`, `net8.0`, `net10.0`)
- Java: read `<java.version>`, `<maven.compiler.source>`, `sourceCompatibility`, or `JAVA_VERSION` in CI
- Python: read `python_requires` in `setup.py`, `requires-python` in `pyproject.toml`, or `.python-version`
- Node.js: read `engines.node` in `package.json`, or `.nvmrc`
- PHP: read `require.php` in `composer.json`
- Ruby: read `.ruby-version` or `ruby` directive in `Gemfile`
- Go: read `go` directive in `go.mod`
- Rust: read `rust-version` in `Cargo.toml`

If no version found, capture `runtime_version_detected: unknown` and add to `unresolved_questions`.

## Polyglot Handling

Many apps are polyglot. Capture all stacks above 5% share. The matrix supports `stack.primary_stack` (one) and `stack.secondary_stacks` (array).

For polyglot apps, the **primary** is the stack used for the main entrypoint (web server, API, scheduler). The **secondary** stacks are infrastructure (e.g., a Python script for build, a Bash deploy script, an SQL migration file).

Heuristic for primary:

1. Stack referenced by the build entrypoint (Dockerfile `CMD`, `package.json` start, `pom.xml` main class)
2. Stack with most lines of code in core source dirs (not `tests/`, `scripts/`, `docs/`)
3. Largest file count among non-trivial extensions

## Confidence Calibration

| Evidence | Confidence |
|----------|-----------|
| Manifest found + parsed + version extracted | **high** |
| Manifest found but version missing | **medium** |
| No manifest; clear file-extension dominance (>60%) + framework signal | **medium** |
| Multiple competing languages, no manifest | **low** |
| User statement only, no source access | **low** |

## Edge Cases

- **Mainframe / IBM i** — file extensions are weak signals. Use presence of JCL, copybooks, CICS maps, RACF files. Default to `low` confidence and recommend specialist probe.
- **SaaS-embedded** — when the only artifacts are XML metadata (Salesforce Force.com IDE, ServiceNow update sets, SharePoint solution packages), classify as `source-unsupported-escalation`, not as a normal stack.
- **Vendor binaries only** — no manifests, no source. Detect from EXE/DLL strings, container base image, installation scripts. `primary_confidence: low`, flag as `no-source-code-available`.
- **Notebooks** — `.ipynb` files imply data-science workload pattern more than a "stack"; capture as primary stack `python` with `workload-data-pipeline`.

## Anti-Patterns

- Don't confuse generated files for source. Skip `node_modules/`, `bin/`, `obj/`, `target/`, `dist/`, `build/`, `vendor/`, `.git/`, `__pycache__/`.
- Don't classify based on test files alone. `*.test.js` does not make the app primarily Node.js if the production code is Java.
- Don't infer framework version from documentation. Read manifests.
- Don't skip secondary stacks — they often carry the build/deploy logic that matters for Phase 5.

## Output Quality Checklist

- [ ] Primary stack identified with evidence path
- [ ] Confidence label set
- [ ] Build system identified
- [ ] Runtime version captured (or marked `unknown` with question)
- [ ] Secondary stacks listed if >5% share
- [ ] Framework signals captured
- [ ] Anti-pattern files excluded from counts
