---
name: config-transformation
description: |
  Configuration file transformation patterns for .NET and Java modernization.
  **Use when:** Converting legacy config files to modern cloud-native formats.
  **Triggers on:** web.config, app.config, applicationContext.xml, persistence.xml files.
  **Covers:** web.config to appsettings.json, XML to YAML/properties, connection string externalization.
---

# Configuration Transformation Skill

Use this skill when transforming legacy configuration files to modern formats for cloud-native applications.

## When to Use This Skill

- Converting web.config to appsettings.json
- Converting app.config to JSON configuration
- Migrating Java XML configs to YAML/properties
- Externalizing configuration for Azure
- Setting up environment-specific configuration
- Integrating with Azure App Configuration or Key Vault

## .NET Configuration Transformation

### web.config to appsettings.json Mapping

| web.config Element | appsettings.json Equivalent |
|--------------------|----------------------------|
| `<connectionStrings>` | `"ConnectionStrings": { }` |
| `<appSettings>` | Root level or custom section |
| `<system.web>` | Middleware in Program.cs |
| `<system.webServer>` | Kestrel configuration |
| `<customErrors>` | Exception handling middleware |
| `<authorization>` | Authorization policies |
| `<authentication>` | Authentication configuration |
| `<sessionState>` | Session middleware options |
| `<httpRuntime>` | Kestrel limits |
| `<compilation debug="true">` | `ASPNETCORE_ENVIRONMENT=Development` |

### Complete Transformation Example

#### Legacy web.config

```xml
<?xml version="1.0" encoding="utf-8"?>
<configuration>
  <connectionStrings>
    <add name="DefaultConnection" 
         connectionString="Server=localhost;Database=MyApp;Trusted_Connection=True;" 
         providerName="System.Data.SqlClient" />
    <add name="RedisCache" 
         connectionString="localhost:6379" />
  </connectionStrings>
  
  <appSettings>
    <add key="ApiBaseUrl" value="https://api.example.com" />
    <add key="MaxPageSize" value="100" />
    <add key="EnableFeatureX" value="true" />
    <add key="SmtpServer" value="smtp.example.com" />
    <add key="SmtpPort" value="587" />
  </appSettings>
  
  <system.web>
    <authentication mode="Forms">
      <forms loginUrl="~/Account/Login" timeout="30" />
    </authentication>
    <authorization>
      <deny users="?" />
    </authorization>
    <sessionState timeout="20" mode="InProc" />
    <customErrors mode="RemoteOnly" defaultRedirect="~/Error">
      <error statusCode="404" redirect="~/Error/NotFound" />
    </customErrors>
  </system.web>
  
  <system.webServer>
    <httpProtocol>
      <customHeaders>
        <add name="X-Frame-Options" value="DENY" />
      </customHeaders>
    </httpProtocol>
  </system.webServer>
</configuration>
```

#### Modern appsettings.json

```jsonc
{
  "ConnectionStrings": {
    "DefaultConnection": "Server=localhost;Database=MyApp;Trusted_Connection=True;TrustServerCertificate=true",
    "RedisCache": "localhost:6379"
  },
  
  "ApiSettings": {
    "BaseUrl": "https://api.example.com",
    "MaxPageSize": 100
  },
  
  "FeatureFlags": {
    "EnableFeatureX": true
  },
  
  "Email": {
    "SmtpServer": "smtp.example.com",
    "SmtpPort": 587,
    "UseSsl": true
  },
  
  "Authentication": {
    "CookieName": ".MyApp.Auth",
    "LoginPath": "/Account/Login",
    "AccessDeniedPath": "/Account/AccessDenied",
    "ExpireTimeSpan": "00:30:00"
  },
  
  "Session": {
    "IdleTimeout": "00:20:00"
  },
  
  "Logging": {
    "LogLevel": {
      "Default": "Information",
      "Microsoft.AspNetCore": "Warning"
    }
  }
}
```

#### Modern Program.cs (Configuration Usage)

```csharp
var builder = WebApplication.CreateBuilder(args);

// Bind configuration sections to strongly-typed options
builder.Services.Configure<ApiSettings>(
    builder.Configuration.GetSection("ApiSettings"));
builder.Services.Configure<EmailSettings>(
    builder.Configuration.GetSection("Email"));

// Database
builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Redis cache
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = builder.Configuration.GetConnectionString("RedisCache");
});

// Authentication (replaces Forms auth)
builder.Services.AddAuthentication(CookieAuthenticationDefaults.AuthenticationScheme)
    .AddCookie(options =>
    {
        var authConfig = builder.Configuration.GetSection("Authentication");
        options.LoginPath = authConfig["LoginPath"];
        options.AccessDeniedPath = authConfig["AccessDeniedPath"];
        options.ExpireTimeSpan = TimeSpan.Parse(authConfig["ExpireTimeSpan"]!);
    });

// Session
builder.Services.AddSession(options =>
{
    options.IdleTimeout = TimeSpan.Parse(
        builder.Configuration["Session:IdleTimeout"]!);
    options.Cookie.HttpOnly = true;
    options.Cookie.IsEssential = true;
});

var app = builder.Build();

// Error handling (replaces customErrors)
if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    app.UseStatusCodePagesWithReExecute("/Error/{0}");
}

// Security headers (replaces system.webServer)
app.Use(async (context, next) =>
{
    context.Response.Headers.Append("X-Frame-Options", "DENY");
    await next();
});

app.UseAuthentication();
app.UseAuthorization();
app.UseSession();
```

## Environment-Specific Configuration

### File Structure

```
appsettings.json                    # Base configuration
appsettings.Development.json        # Development overrides
appsettings.Staging.json            # Staging overrides
appsettings.Production.json         # Production overrides
```

### Production Configuration with Azure References

```jsonc
// appsettings.Production.json
{
  "ConnectionStrings": {
    // Use Azure SQL with managed identity
    "DefaultConnection": "Server=tcp:myserver.database.windows.net,1433;Database=MyApp;Authentication=Active Directory Default;"
  },
  
  "KeyVault": {
    "VaultUri": "https://myapp-kv.vault.azure.net/"
  },
  
  "ApplicationInsights": {
    "ConnectionString": "${APP_INSIGHTS_CONNECTION_STRING}"
  },
  
  "Logging": {
    "LogLevel": {
      "Default": "Warning",
      "Microsoft.AspNetCore": "Error"
    }
  }
}
```

## Java Configuration Transformation

### XML to YAML Mapping

| XML Element | YAML Equivalent |
|-------------|-----------------|
| `<bean>` | Component scanning or `@Bean` |
| `<property>` | Application properties |
| `<context:property-placeholder>` | `@Value` or `@ConfigurationProperties` |
| `<jdbc:embedded-database>` | `spring.datasource.*` |
| `<security:http>` | `spring.security.*` |

### Legacy applicationContext.xml → application.yml

#### Legacy XML

```xml
<beans>
  <context:property-placeholder location="classpath:database.properties"/>
  
  <bean id="dataSource" class="org.apache.commons.dbcp.BasicDataSource">
    <property name="driverClassName" value="${db.driver}"/>
    <property name="url" value="${db.url}"/>
    <property name="username" value="${db.username}"/>
    <property name="password" value="${db.password}"/>
  </bean>
  
  <bean id="sessionFactory" class="org.springframework.orm.hibernate5.LocalSessionFactoryBean">
    <property name="dataSource" ref="dataSource"/>
    <property name="hibernateProperties">
      <props>
        <prop key="hibernate.dialect">org.hibernate.dialect.SQLServerDialect</prop>
        <prop key="hibernate.show_sql">true</prop>
      </props>
    </property>
  </bean>
</beans>
```

#### Modern application.yml

```yaml
spring:
  datasource:
    url: jdbc:sqlserver://${DB_HOST:localhost}:1433;database=${DB_NAME:myapp};encrypt=true;trustServerCertificate=false
    username: ${DB_USER}
    password: ${DB_PASSWORD}
    driver-class-name: com.microsoft.sqlserver.jdbc.SQLServerDriver
    hikari:
      maximum-pool-size: 10
      minimum-idle: 5
  
  jpa:
    hibernate:
      ddl-auto: validate
    show-sql: ${SHOW_SQL:false}
    properties:
      hibernate:
        dialect: org.hibernate.dialect.SQLServerDialect
        format_sql: true

  profiles:
    active: ${SPRING_PROFILES_ACTIVE:dev}

---
spring:
  config:
    activate:
      on-profile: dev
  datasource:
    url: jdbc:sqlserver://localhost:1433;database=myapp_dev;trustServerCertificate=true

---
spring:
  config:
    activate:
      on-profile: prod
  datasource:
    url: jdbc:sqlserver://${DB_HOST}.database.windows.net:1433;database=${DB_NAME};encrypt=true;authentication=ActiveDirectoryDefault
```

## Azure Integration Patterns

### Azure App Configuration

```csharp
// Program.cs
builder.Configuration.AddAzureAppConfiguration(options =>
{
    options.Connect(new Uri("https://myconfig.azconfig.io"), new DefaultAzureCredential())
        .Select(KeyFilter.Any, LabelFilter.Null)
        .Select(KeyFilter.Any, builder.Environment.EnvironmentName)
        .ConfigureKeyVault(kv => kv.SetCredential(new DefaultAzureCredential()));
});
```

### Azure Key Vault References

```jsonc
// appsettings.json with Key Vault reference
{
  "ConnectionStrings": {
    "DefaultConnection": "@Microsoft.KeyVault(SecretUri=https://myvault.vault.azure.net/secrets/db-connection/)"
  }
}
```

## Template Files

- [appsettings.template.jsonc](./templates/appsettings.template.jsonc) - Complete .NET config template
- [application.template.yml](./templates/application.template.yml) - Spring Boot config template

## Migration Checklist

- [ ] Extract all connection strings
- [ ] Convert appSettings to typed configuration
- [ ] Replace ConfigurationManager calls with IConfiguration
- [ ] Set up environment-specific overrides
- [ ] Externalize secrets to Key Vault
- [ ] Configure logging providers
- [ ] Test configuration loading in all environments
- [ ] Document all configuration values
