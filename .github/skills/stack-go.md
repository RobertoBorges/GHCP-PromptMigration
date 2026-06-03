# Skill: Stack Adapter — Go (Golang) (Stub)

> **Stub adapter.** Provides classification + Azure target tendencies. Phase 2 effort for these stacks is typically **L or XL** with frequent **rebuild** recommendations. Pair with the Architect early.

## File Evidence

`*.go`, `go.mod`, `go.sum`

## Version Targets

Go 1.22+ (target). Pre-1.18 lacks generics; lacks workspaces.

## Sub-Stack Detection

| Sub-stack | Signal | Azure target |
|-----------|--------|--------------|
| Gin | `github.com/gin-gonic/gin` | App Service / Container Apps |
| Echo | `github.com/labstack/echo` | App Service / Container Apps |
| Fiber | `github.com/gofiber/fiber` | App Service / Container Apps |
| Chi | `github.com/go-chi/chi` | App Service / Container Apps |
| net/http only | stdlib HTTP only | App Service / Container Apps |
| CLI / one-shot | `main.go` exits | Container Apps Jobs / Functions |
| gRPC server | `google.golang.org/grpc` | Container Apps (HTTP/2) |

## Risks / Migration Constraints

- Go binaries are statically linked but CGO toggles + `libc` choices matter (alpine vs distroless vs ubuntu).
- Build cache size; multi-stage Dockerfile is mandatory.
- Module proxy (`GOPROXY`) needs network access in CI.
- Vendoring strategy (`go mod vendor` vs not) affects build reproducibility.
- `cgo` dependencies require build deps in container.

## Phase 2 Effort

Default: **L** (medium-to-large). Often **XL** when source predates current supported versions.

## Identity Modernization

Default: replace any custom auth with **Entra ID OIDC** at the app boundary. Map current users to Entra ID groups.

## Output Checklist

- [ ] Sub-stack identified
- [ ] Runtime version captured (and flagged if EOL)
- [ ] Top dependencies / vendor libs captured
- [ ] Native dependencies / Windows-only / hardware deps flagged
- [ ] Approach decided: `replatform` / `refactor` / `rebuild`
- [ ] Architect + (often) Cost Engineer flagged as required specialists
- [ ] Target Azure compute candidate noted (often **AKS**, **Container Apps**, or **VM**)