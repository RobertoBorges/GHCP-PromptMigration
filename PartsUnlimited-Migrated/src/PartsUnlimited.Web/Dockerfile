# syntax=docker/dockerfile:1
FROM mcr.microsoft.com/dotnet/sdk:10.0 AS build
WORKDIR /src
COPY ["PartsUnlimited.Web.csproj", "./"]
RUN dotnet restore "PartsUnlimited.Web.csproj"
COPY . .
RUN dotnet publish "PartsUnlimited.Web.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/aspnet:10.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish .

# Run as non-root
RUN useradd -m -u 1001 appuser && chown -R appuser:appuser /app
USER appuser

ENV ASPNETCORE_URLS=http://+:8080
ENV ASPNETCORE_ENVIRONMENT=Production
EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
    CMD wget -q --spider http://localhost:8080/ || exit 1

ENTRYPOINT ["dotnet", "PartsUnlimited.Web.dll"]
