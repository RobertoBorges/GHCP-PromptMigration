# Docker Containerization

> **REFERENCE ONLY** — This root `skills/` copy is for reference and onboarding. Prompts must reference the authoritative prompt-local copy at `#file:.github/skills/docker-containerize.md`.

Use this skill when the migrated application must run as a container on Azure Container Apps, AKS, or App Service for Containers.

## Core rules

- Use multi-stage builds.
- Run as a non-root user when practical.
- Keep images small and deterministic.
- Expose the application port explicitly.
- Add a `.dockerignore` file.

## .NET pattern

```dockerfile
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY . .
RUN dotnet publish -c Release -o /out

FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /out .
ENTRYPOINT ["dotnet", "Contoso.Web.dll"]
```

## Java pattern

```dockerfile
FROM maven:3.9-eclipse-temurin-21 AS build
WORKDIR /src
COPY . .
RUN mvn -DskipTests package

FROM eclipse-temurin:21-jre
WORKDIR /app
COPY --from=build /src/target/app.jar app.jar
ENTRYPOINT ["java", "-jar", "/app/app.jar"]
```

## Validation checklist

- Image builds locally and in CI.
- Runtime config comes from env vars or secrets.
- Health endpoint and startup command are documented.
- Base images are supported and patched.
