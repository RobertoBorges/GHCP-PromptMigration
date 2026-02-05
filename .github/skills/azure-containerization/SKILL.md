---
name: azure-containerization
description: |
  Docker containerization patterns for .NET and Java applications targeting Azure.
  **Use when:** Creating Dockerfiles or deploying to Container Apps, App Service containers, or AKS.
  **Triggers on:** Container Apps or AKS selected as hosting platform, Docker-related requests.
  **Covers:** Multi-stage Dockerfiles, docker-compose, Container Apps configuration, health checks, resource limits.
---

# Azure Containerization Skill

Use this skill when containerizing .NET or Java applications for Azure deployment.

## When to Use This Skill

- Creating Dockerfiles for .NET 8+ or Java 21+ applications
- Setting up docker-compose for local development
- Deploying to Azure Container Apps
- Deploying to Azure App Service (container mode)
- Deploying to Azure Kubernetes Service (AKS)
- Configuring container health checks

## .NET Container Best Practices

### Multi-Stage Dockerfile for .NET 8

```dockerfile
# Build stage
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

# Copy csproj and restore dependencies
COPY ["src/MyApp/MyApp.csproj", "MyApp/"]
RUN dotnet restore "MyApp/MyApp.csproj"

# Copy source and build
COPY src/MyApp/ MyApp/
WORKDIR /src/MyApp
RUN dotnet build -c Release -o /app/build

# Publish stage
FROM build AS publish
RUN dotnet publish -c Release -o /app/publish /p:UseAppHost=false

# Runtime stage
FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine AS final
WORKDIR /app

# Create non-root user
RUN addgroup -g 1000 appgroup && adduser -u 1000 -G appgroup -D appuser
USER appuser

COPY --from=publish /app/publish .

# Configure for Azure
ENV ASPNETCORE_URLS=http://+:8080
ENV ASPNETCORE_ENVIRONMENT=Production
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/health || exit 1

ENTRYPOINT ["dotnet", "MyApp.dll"]
```

### .NET .dockerignore

```
**/.dockerignore
**/.git
**/.gitignore
**/.vs
**/.vscode
**/bin
**/obj
**/Dockerfile*
**/docker-compose*
**/*.md
**/node_modules
**/.env
**/appsettings.Development.json
```

## Java Container Best Practices

### Multi-Stage Dockerfile for Spring Boot (Java 21)

```dockerfile
# Build stage
FROM eclipse-temurin:21-jdk-alpine AS build
WORKDIR /app

# Copy Maven wrapper and pom
COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .

# Download dependencies
RUN chmod +x mvnw && ./mvnw dependency:go-offline -B

# Copy source and build
COPY src src
RUN ./mvnw package -DskipTests -B

# Extract layers for better caching
FROM eclipse-temurin:21-jdk-alpine AS extract
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
RUN java -Djarmode=layertools -jar app.jar extract

# Runtime stage
FROM eclipse-temurin:21-jre-alpine AS final
WORKDIR /app

# Create non-root user
RUN addgroup -g 1000 appgroup && adduser -u 1000 -G appgroup -D appuser
USER appuser

# Copy layers in order of change frequency
COPY --from=extract /app/dependencies/ ./
COPY --from=extract /app/spring-boot-loader/ ./
COPY --from=extract /app/snapshot-dependencies/ ./
COPY --from=extract /app/application/ ./

# Configure for Azure
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0"
ENV SERVER_PORT=8080
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:8080/actuator/health || exit 1

ENTRYPOINT ["java", "org.springframework.boot.loader.launch.JarLauncher"]
```

### Java .dockerignore

```
**/.dockerignore
**/.git
**/.gitignore
**/.idea
**/.mvn/wrapper/maven-wrapper.jar
**/target
**/Dockerfile*
**/docker-compose*
**/*.md
**/.env
**/application-local.yml
```

## Docker Compose for Local Development

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      - ASPNETCORE_ENVIRONMENT=Development  # or SPRING_PROFILES_ACTIVE=dev
      - ConnectionStrings__DefaultConnection=Server=db;Database=myapp;User=sa;Password=Your_password123;TrustServerCertificate=true
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "wget", "--spider", "-q", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  db:
    image: mcr.microsoft.com/mssql/server:2022-latest
    environment:
      - ACCEPT_EULA=Y
      - SA_PASSWORD=Your_password123
    ports:
      - "1433:1433"
    volumes:
      - sqldata:/var/opt/mssql
    healthcheck:
      test: /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P "Your_password123" -Q "SELECT 1"
      interval: 10s
      timeout: 5s
      retries: 5

volumes:
  sqldata:
```

## Azure Container Apps Configuration

### Container App YAML

```yaml
properties:
  configuration:
    activeRevisionsMode: Single
    ingress:
      external: true
      targetPort: 8080
      transport: http
      allowInsecure: false
    secrets:
      - name: connection-string
        keyVaultUrl: https://myvault.vault.azure.net/secrets/db-connection
        identity: system
    registries:
      - server: myregistry.azurecr.io
        identity: system
  template:
    containers:
      - image: myregistry.azurecr.io/myapp:latest
        name: myapp
        resources:
          cpu: 0.5
          memory: 1Gi
        env:
          - name: ConnectionStrings__DefaultConnection
            secretRef: connection-string
        probes:
          - type: liveness
            httpGet:
              path: /health/live
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 30
          - type: readiness
            httpGet:
              path: /health/ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
    scale:
      minReplicas: 1
      maxReplicas: 10
      rules:
        - name: http-rule
          http:
            metadata:
              concurrentRequests: '100'
```

## Health Check Endpoints

### .NET Health Checks

```csharp
// Program.cs
builder.Services.AddHealthChecks()
    .AddSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")!)
    .AddAzureBlobStorage(builder.Configuration["AzureStorage:ConnectionString"]!);

app.MapHealthChecks("/health/live", new HealthCheckOptions
{
    Predicate = _ => false  // Just check if app is running
});

app.MapHealthChecks("/health/ready", new HealthCheckOptions
{
    Predicate = check => check.Tags.Contains("ready")
});
```

### Java Health Checks (Spring Boot Actuator)

```yaml
# application.yml
management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics
  endpoint:
    health:
      show-details: when_authorized
      probes:
        enabled: true
  health:
    livenessstate:
      enabled: true
    readinessstate:
      enabled: true
```

## Container Security Best Practices

1. **Use specific image tags** - Never use `latest` in production
2. **Run as non-root** - Create and use a dedicated user
3. **Use minimal base images** - Alpine or distroless
4. **Scan for vulnerabilities** - Use Trivy, Snyk, or Azure Defender
5. **Don't store secrets in images** - Use Key Vault references
6. **Use multi-stage builds** - Smaller final images
7. **Set resource limits** - CPU and memory constraints
8. **Enable health checks** - Liveness and readiness probes

## Template Files

- [Dockerfile.dotnet](./templates/Dockerfile.dotnet) - .NET 8 multi-stage Dockerfile
- [Dockerfile.java](./templates/Dockerfile.java) - Java 21 multi-stage Dockerfile
- [docker-compose.yml](./templates/docker-compose.yml) - Local development compose
- [.dockerignore](./templates/.dockerignore) - Files to exclude
