# Azure Entra ID Integration

Use this skill when migrating authentication and authorization to Microsoft Entra ID for .NET, Java, and Azure-hosted workloads.

## Use Cases

Apply this skill when the solution needs:

- interactive user sign-in
- bearer token validation for APIs
- app roles or delegated scopes
- service-to-service access via managed identity
- replacement for Windows Authentication, Forms Authentication, or custom token plumbing

## App Registration Checklist

Create or verify:

1. application registration for web app or API
2. redirect URIs for local, staging, and production hosts
3. exposed API scopes or app roles
4. API permissions for downstream resources
5. optional client secret or certificate only when managed identity cannot be used

## .NET Web App with `Microsoft.Identity.Web`

### `appsettings.json`

```json
{
  "AzureAd": {
    "Instance": "https://login.microsoftonline.com/",
    "TenantId": "<tenant-id>",
    "ClientId": "<web-app-client-id>",
    "CallbackPath": "/signin-oidc"
  }
}
```

### `Program.cs`

```csharp
using Microsoft.AspNetCore.Authentication.OpenIdConnect;
using Microsoft.Identity.Web;

builder.Services
    .AddAuthentication(OpenIdConnectDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApp(builder.Configuration.GetSection("AzureAd"));

builder.Services.AddAuthorization();
```

## .NET Web API Token Validation

```csharp
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.Identity.Web;

builder.Services
    .AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApi(builder.Configuration.GetSection("AzureAd"));

builder.Services.AddAuthorization(options =>
{
    options.AddPolicy("Api.Read", policy => policy.RequireClaim("scp", "Api.Read"));
});
```

## Spring Security OAuth2 Resource Server

### `application.yml`

```yaml
spring:
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://login.microsoftonline.com/${AZURE_TENANT_ID}/v2.0
```

### `SecurityConfig`

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

## API Permissions and Authorization

Prefer this order:

1. app roles for coarse-grained application roles
2. delegated scopes for API permissions
3. managed identity for Azure-to-Azure access
4. group claims only when governance already depends on them

Do not hardcode tenant IDs, role IDs, or email allowlists in application code.

## MSAL Configuration

Use MSAL for desktop, SPA, or confidential-client flows when the app must acquire tokens explicitly.

### JavaScript example

```javascript
const msalConfig = {
  auth: {
    clientId: "<client-id>",
    authority: "https://login.microsoftonline.com/<tenant-id>",
    redirectUri: window.location.origin
  }
};
```

### .NET confidential client example

```csharp
var app = ConfidentialClientApplicationBuilder
    .Create(clientId)
    .WithAuthority($"https://login.microsoftonline.com/{tenantId}")
    .WithClientSecret(clientSecret)
    .Build();
```

Use certificates or managed identity where possible instead of long-lived client secrets.

## Managed Identity vs App Registration

| Scenario | Preferred Pattern |
|---|---|
| User sign-in to app | App registration + `Microsoft.Identity.Web` / MSAL |
| API protection | App registration + JWT validation |
| Azure resource access from Azure-hosted app | Managed identity |
| Service-to-service outside Azure | App registration or workload identity federation |

## Validation Checklist

- sign-in or token validation works in each environment
- redirect URIs match actual deployed hosts
- scopes/app roles match authorization policies in code
- managed identity is used for Azure resources wherever possible
- no secrets are committed to source control

## Output Expectations for Prompts

When this skill is applied, the prompt should:

- list required app registrations, scopes, roles, and redirect URIs
- generate auth wiring for the target stack (`.NET`, `Java`, `Python`, `Node.js`, `PHP`, `Ruby`, `Go`, etc.) — see the SDK reference table below
- distinguish user identity from workload identity
- call out remaining legacy auth dependencies explicitly
