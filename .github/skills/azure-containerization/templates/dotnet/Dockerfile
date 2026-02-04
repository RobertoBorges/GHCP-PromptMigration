# =============================================================================
# .NET 8 Multi-Stage Dockerfile for Azure Container Apps / AKS
# =============================================================================
# Optimized for production with security best practices
# =============================================================================

# Build stage
FROM mcr.microsoft.com/dotnet/sdk:8.0-alpine AS build
WORKDIR /src

# Copy csproj files first for layer caching
COPY ["*.sln", "./"]
COPY ["src/*/*.csproj", "./"]

# Restore dependencies (cached if csproj unchanged)
RUN dotnet restore

# Copy full source code
COPY . .

# Build and publish
RUN dotnet publish -c Release -o /app/publish \
    --no-restore \
    /p:UseAppHost=false \
    /p:PublishTrimmed=false

# =============================================================================
# Runtime stage - Alpine for smaller image size
# =============================================================================
FROM mcr.microsoft.com/dotnet/aspnet:8.0-alpine AS final
WORKDIR /app

# Install curl for health checks (Alpine)
RUN apk add --no-cache curl tzdata

# Create non-root user for security (Azure Container Apps requirement)
RUN addgroup -g 1000 appgroup && \
    adduser -u 1000 -G appgroup -D -s /bin/sh appuser

# Copy published application
COPY --from=build /app/publish .

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# Configure ASP.NET Core
ENV ASPNETCORE_URLS=http://+:8080
ENV ASPNETCORE_ENVIRONMENT=Production
ENV DOTNET_RUNNING_IN_CONTAINER=true
ENV DOTNET_EnableDiagnostics=0

# Expose port (Azure Container Apps uses 8080 by default)
EXPOSE 8080

# Health check for orchestrators
HEALTHCHECK --interval=30s --timeout=10s --start-period=10s --retries=3 \
    CMD curl --fail http://localhost:8080/health || exit 1

# Entry point
ENTRYPOINT ["dotnet", "MyApp.dll"]
