# Java 8 to Java 21 Migration

Use this skill when modernizing Java 8 applications for Azure using Java 21 and Spring Boot 3.

## When to Use

Apply this skill when the source contains one or more of the following:

- `<java.version>1.8</java.version>` or `sourceCompatibility = 1.8`
- Spring Boot 1.x or 2.x
- `javax.*` imports
- WAR packaging, `web.xml`, old servlet containers, or XML-heavy Spring configuration

## Target State

Default to these targets unless the assessment report says otherwise:

- Java 21 LTS
- Spring Boot 3.x
- `jakarta.*` namespaces
- Maven/Gradle versions compatible with Java 21
- executable JAR packaging unless WAR is mandatory
- externalized configuration through `application.yml`, environment variables, and Azure config providers

## Language and Runtime Upgrade Themes

- Prefer records for immutable DTOs when appropriate.
- Use switch expressions, text blocks, pattern matching, and `var` where clarity improves.
- Replace legacy date/time APIs with `java.time` if they still remain.
- Remove Java EE-era assumptions that depend on app servers.

## Java 8 to 21 Examples

### Before - Java 8 style DTO

```java
public class TicketDto {
    private final String number;
    private final int seats;

    public TicketDto(String number, int seats) {
        this.number = number;
        this.seats = seats;
    }

    public String getNumber() { return number; }
    public int getSeats() { return seats; }
}
```

### After - Java 21 record

```java
public record TicketDto(String number, int seats) { }
```

### Before - verbose switch

```java
String status;
switch (state) {
    case 0:
        status = "Draft";
        break;
    case 1:
        status = "Confirmed";
        break;
    default:
        status = "Unknown";
}
```

### After - switch expression

```java
String status = switch (state) {
    case 0 -> "Draft";
    case 1 -> "Confirmed";
    default -> "Unknown";
};
```

## Spring Boot 2 to 3 Migration

### Maven baseline

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
      <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>
  </dependencies>
</project>
```

### Gradle baseline

```groovy
plugins {
    id 'java'
    id 'org.springframework.boot' version '3.3.0'
    id 'io.spring.dependency-management' version '1.1.5'
}

group = 'com.contoso'
version = '1.0.0'

java {
    toolchain {
        languageVersion = JavaLanguageVersion.of(21)
    }
}
```

## Jakarta EE Namespace Changes

| Legacy Namespace | Target Namespace |
|---|---|
| `javax.servlet.*` | `jakarta.servlet.*` |
| `javax.persistence.*` | `jakarta.persistence.*` |
| `javax.validation.*` | `jakarta.validation.*` |
| `javax.annotation.*` | `jakarta.annotation.*` or modern Spring alternatives |

### Before

```java
import javax.persistence.Entity;
import javax.validation.constraints.NotBlank;
```

### After

```java
import jakarta.persistence.Entity;
import jakarta.validation.constraints.NotBlank;
```

## Application Bootstrapping

### Before - traditional servlet init

```java
public class LegacyApplication extends SpringBootServletInitializer {
    @Override
    protected SpringApplicationBuilder configure(SpringApplicationBuilder application) {
        return application.sources(LegacyApplication.class);
    }
}
```

### After - executable app

```java
@SpringBootApplication
public class BusReservationApplication {
    public static void main(String[] args) {
        SpringApplication.run(BusReservationApplication.class, args);
    }
}
```

## Application Properties Modernization

### Before - flat `application.properties`

```properties
server.port=8080
database.url=jdbc:sqlserver://localhost:1433;database=mydb
database.username=user
database.password=pass
```

### After - `application.yml`

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
  jpa:
    open-in-view: false

management:
  endpoints:
    web:
      exposure:
        include: health,info,prometheus
```

## Dependency and Build Notes

- Upgrade Surefire/Failsafe, compiler plugins, and any BOMs that pin old Java versions.
- Replace libraries incompatible with Spring Framework 6 / Boot 3.
- Review logging, validation, persistence, and security dependencies together to avoid version skew.
- Prefer JUnit 5 and Testcontainers-compatible test stacks.

## Azure-Ready Defaults

- Expose Actuator health endpoints.
- Externalize secrets; do not commit them in properties files.
- Prefer container-friendly executable JARs for App Service or Container Apps.
- Use OAuth2/OIDC and Entra ID for authentication.

## Validation Commands

```bash
mvn clean test
mvn -DskipTests package
```

or

```bash
gradle test
gradle bootJar
```

## Output Expectations for Prompts

When this skill is applied, the prompt should:

- Produce upgraded Maven/Gradle files
- List all `javax.*` to `jakarta.*` changes explicitly
- Modernize configuration and security in the same pass
- Flag libraries that block Java 21 or Spring Boot 3 adoption
