# Azure Entra ID

Use this skill when migrating authentication and authorization to Microsoft Entra ID for web apps, APIs, background services, or multi-tier Azure solutions.

## Use cases

Apply this skill when the application must support one or more of the following:

- Interactive sign-in for users
- Bearer token validation for APIs
- App roles or scope-based authorization
- Service-to-service access using managed identity
- Replacing Windows Authentication, Forms Authentication, custom auth, or shared secrets

## Decision model

| App type | Recommended pattern |
|---|---|
| ASP.NET Core MVC / Razor Pages / Blazor Server | `AddMicrosoftIdentityWebApp` |
| ASP.NET Core Web API | `AddMicrosoftIdentityWebApi` |
| Spring Boot API | OAuth2 resource server with JWT validation |
| Background worker on Azure | Managed identity first; app registration only if required |
| SPA + API | SPA uses MSAL, API validates Entra tokens |

## .NET Web API baseline

```json
{
  "AzureAd": {
    "Instance": "https://login.microsoftonline.com/",
    "TenantId": "<tenant-id>",
    "ClientId": "<api-app-registration-client-id>",
    "Audience": "api://<api-app-registration-client-id>"
  }
}
```

```csharp
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.Identity.Web;

builder.Services
    .AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApi(builder.Configuration.GetSection("AzureAd"));

builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("Api.Read", policy =>
        policy.RequireClaim("scp", "Api.Read"));
});

var app = builder.Build();
app.UseAuthentication();
app.UseAuthorization();
```

## Spring Boot API baseline

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://login.microsoftonline.com/${AZURE_TENANT_ID}/v2.0
```

```java
@Bean
SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
    return http
        .authorizeHttpRequests(auth -> auth
            .requestMatchers("/actuator/health").permitAll()
            .anyRequest().authenticated())
        .oauth2ResourceServer(oauth -> oauth.jwt())
        .build();
}
```

## Authorization guidance

Prefer these authorization mechanisms in order:

1. App roles for coarse-grained application roles
2. Scopes for delegated API permissions
3. Group claims only when group-based governance already exists
4. Resource-level authorization in the application for domain-specific rules

Do not hardcode user emails, tenant-specific IDs, or magic role names without central configuration.

## Managed identity vs app registration

- Use managed identity for Azure resource access from Azure-hosted workloads.
- Use app registrations for user-facing login and public API authorization.
- Do not use client secrets for Azure-to-Azure calls when managed identity is available.

## Configuration and secret handling

- Tenant IDs, client IDs, and audiences are configuration, not secrets.
- Client secrets and certificates belong in Key Vault, not source control.
- Production callback URLs, redirect URIs, and audiences must match deployed hostnames.

## Validation checklist

Validate that:

- Sign-in or token validation works in the deployed environment.
- Authorization policies match business roles and API scopes.
- Managed identity is used for downstream Azure resources where possible.
- Local development guidance exists for developers without production secrets.

## Output expectations for migration prompts

- Generate auth wiring in code and configuration.
- State the required Entra objects: app registrations, scopes, app roles, redirect URIs.
- Distinguish user auth from workload identity.
- Call out any remaining legacy auth dependencies or on-prem assumptions.
