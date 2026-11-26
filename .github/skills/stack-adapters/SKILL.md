---
name: stack-adapters
description: |
  Routes migration discovery and planning to stack-specific guidance for universal Azure application migrations. Use when evidence includes language/runtime manifests, source files, build files, framework markers, or Capability Matrix stack fields for .NET, Java, Node.js, Python, PHP, Ruby, Go, Rust, Perl, Scala/Kotlin, C++ Windows, Delphi/VB6, PowerBuilder, or Oracle Forms. Start with stack detection when the stack is unknown or confidence is low.
user-invocable: false
---

# Stack Adapters Router

## When to use this skill

Use this router during discovery, planning, and code migration whenever repository, archive, or inventory evidence indicates an application stack, runtime, framework, or build system. This skill is universal: it routes to the matching stack adapter rather than assuming a .NET or Java-only path.

Start with [Stack Detection](./references/stack-detection.md) when the stack is unknown, conflicting, polyglot, or low confidence. That reference explains manifest-first detection, extension-share fallback, framework detection, build-system detection, runtime detection, polyglot handling, and confidence calibration.

## Selection table

| Detected signal or evidence | Read this reference |
|---|---|
| Unknown, missing, conflicting, or low-confidence stack evidence | [Stack Detection](./references/stack-detection.md) |
| `*.sln`, `*.csproj`, `*.vbproj`, `web.config`, `app.config`, `global.asax`, `*.aspx`, `*.svc`, Razor/Blazor files, `System.Web`, WCF, ASP.NET Core | [.NET](./references/stack-dotnet.md) |
| `pom.xml`, `build.gradle`, `*.java`, `*.jsp`, `WEB-INF/`, `META-INF/`, `*.war`, `*.ear`, Spring, Java EE, Jakarta EE, servlet, EJB, JSF | [Java](./references/stack-java.md) |
| `package.json`, `*.js`, `*.mjs`, `*.cjs`, `*.ts`, `*.tsx`, `node_modules/`, npm/yarn/pnpm lockfiles, Express, NestJS, Next.js, Lambda handlers | [Node.js](./references/stack-nodejs.md) |
| `*.py`, `requirements.txt`, `pyproject.toml`, `setup.py`, `Pipfile`, `poetry.lock`, Django, Flask, FastAPI, Celery, Airflow, notebooks | [Python](./references/stack-python.md) |
| `*.php`, `composer.json`, `composer.lock`, `index.php`, Laravel, Symfony, WordPress, Magento, Drupal, Joomla, LAMP | [PHP](./references/stack-php.md) |
| `*.fmb`, `*.fmx`, `*.rdf`, `*.rep`, `*.mmb`, `*.pll`, Oracle Forms Builder, Oracle Reports, Forms Services, APEX | [Oracle Forms / Reports](./references/stack-oracle-forms.md) |
| `*.go`, `go.mod`, `go.sum`, Gin, Echo, Fiber, Chi, `net/http`, Go CLI, Go gRPC | [Go](./references/stack-go.md) |
| `*.rb`, `Gemfile`, `Gemfile.lock`, `Rakefile`, `config.ru`, Rails, Sinatra, Hanami, Sidekiq, Rack | [Ruby](./references/stack-ruby.md) |
| `*.rs`, `Cargo.toml`, `Cargo.lock`, Actix-web, Axum, Rocket, Tonic, Rust CLI, WASM target | [Rust](./references/stack-rust.md) |
| `*.pl`, `*.pm`, `*.t`, `*.psgi`, `cpanfile`, `Makefile.PL`, Mojolicious, Dancer, Catalyst, Plack, CGI | [Perl](./references/stack-perl.md) |
| `*.scala`, `*.kt`, `*.kts`, `build.sbt`, `build.gradle.kts`, Akka/Pekko, Play, Spark, Spring Boot Kotlin, Ktor | [Scala / Kotlin](./references/stack-scala-kotlin.md) |
| `*.cpp`, `*.h`, `*.hpp`, `*.vcxproj`, Windows-specific CMake, MFC, ATL/COM, native Windows services, C++/CLI | [C++ on Windows](./references/stack-cpp-windows.md) |
| `*.dpr`, `*.pas`, `*.dpk`, `*.dfm`, `*.vbp`, `*.frm`, `*.bas`, `*.cls`, Delphi VCL/FMX, VB6, COM components | [Delphi / Visual Basic 6](./references/stack-delphi-vb6.md) |
| `*.pbl`, `*.pbt`, `*.pbw`, `*.sru`, PowerBuilder DataWindow, PowerServer, Appeon | [PowerBuilder](./references/stack-powerbuilder.md) |

## How to use

1. Inspect the available evidence and select the best-matching row.
2. If stack evidence is uncertain, read [Stack Detection](./references/stack-detection.md) first and record confidence before choosing a stack adapter.
3. Read the selected reference file before producing the Capability Matrix, migration plan, code changes, risks, or Azure target options.
4. For polyglot systems, read one reference per significant stack and capture primary/secondary stack roles instead of collapsing everything into one language.
