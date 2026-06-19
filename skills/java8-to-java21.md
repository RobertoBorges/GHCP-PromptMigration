# Java 8 to Java 21 + Spring Boot 3

Use this skill when modernizing legacy Java 8 workloads for Azure using Java 21 and Spring Boot 3.x.

## When to use

Apply this skill when the source contains one or more of the following:

- `sourceCompatibility = 1.8` or `<java.version>1.8</java.version>`
- `javax.*` imports
- Spring Boot 1.x or 2.x
- Servlet container WAR packaging with `web.xml`
- XML-heavy Spring configuration, old JUnit 4 tests, or deprecated logging stacks

## Target state

Default to these modernization targets:

- Java 21 LTS
- Spring Boot 3.x with Jakarta namespaces
- Maven or Gradle updated to a version compatible with Java 21
- Executable JAR packaging unless the platform requires a WAR
- Externalized configuration through `application.yml`, environment variables, and Key Vault
- Micrometer / Application Insights friendly observability

## Core migration themes

1. Runtime and build upgrade
2. `javax.*` to `jakarta.*` namespace changes
3. Spring Boot 3 and dependency alignment
4. Security modernization using OAuth2/OIDC and Entra ID
5. Container-friendly packaging for Azure

## Maven baseline example

```xml
<project>
  <modelVersion>4.0.0</modelVersion>
  <parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.3.0</version>
    <relativePath/>
  </parent>

  <properties>
    <java.version>21</java.version>
  </properties>

  <dependencies>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-actuator</artifactId>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-oauth2-resource-server</artifactId>
    </dependency>
    <dependency>
      <groupId>org.springframework.boot</groupId>
      <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-maven-plugin</artifactId>
      </plugin>
    </plugins>
  </build>
</project>
```

## Jakarta namespace migration

The biggest code-level breaking change is usually moving from `javax.*` to `jakarta.*`.

| Legacy | Target |
|---|---|
| `javax.servlet.*` | `jakarta.servlet.*` |
| `javax.persistence.*` | `jakarta.persistence.*` |
| `javax.validation.*` | `jakarta.validation.*` |
| `javax.annotation.*` | Use `jakarta.annotation.*` or modern Spring alternatives |

Example:

```java
import jakarta.persistence.Entity;
import jakarta.persistence.Id;
import jakarta.validation.constraints.NotBlank;
```

## Spring Boot application target

```java
@SpringBootApplication
public class BusReservationApplication {
    public static void main(String[] args) {
        SpringApplication.run(BusReservationApplication.class, args);
    }
}
```

## Configuration pattern

```yaml
server:
  port: ${PORT:8080}

spring:
  application:
    name: bus-reservation-api
  datasource:
    url: ${JDBC_URL}
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
  security:
    oauth2:
      resourceserver:
        jwt:
          issuer-uri: https://login.microsoftonline.com/${AZURE_TENANT_ID}/v2.0

management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus
```

## Azure-friendly packaging

- Prefer executable JARs for App Service or Container Apps.
- Use a Java 21 base image for containers.
- Expose health endpoints through Spring Boot Actuator.
- Avoid filesystem assumptions and local machine-specific configuration.

Example container base:

```dockerfile
FROM eclipse-temurin:21-jre
WORKDIR /app
COPY target/app.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java","-jar","/app/app.jar"]
```

## Security modernization

- Replace container-managed or custom auth with Spring Security OIDC / OAuth2.
- Use Entra ID for web app sign-in or resource server JWT validation.
- Store secrets outside the repo and inject through deployment configuration.

## Validation commands

```bash
mvn clean test
mvn -DskipTests package
```

Also validate:

- No remaining `javax.*` imports that are incompatible with Boot 3.
- All libraries are compatible with Java 21.
- Health endpoints, configuration loading, and auth flows still work.
- Packaging matches the intended Azure host.

## Output expectations for the migration prompt

- Produce updated build files.
- List namespace and dependency breaking changes explicitly.
- Modernize configuration and security in the same pass.
- Flag libraries that block Java 21 or Spring Boot 3 adoption.
