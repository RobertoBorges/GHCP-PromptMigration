---
name: java-modernization
description: |
  Java EE and legacy Java to modern Spring Boot migration patterns.
  **Use when:** User has a Java EE, J2EE, or legacy Java 8/11 application and needs to upgrade to Spring Boot 3.x with Java 21.
  **Triggers on:** pom.xml with javax.* dependencies, web.xml files, EJB annotations, JAAS configuration.
  **Covers:** EJB to Spring beans, XML to Java/YAML config, JAAS to Spring Security OAuth2, JPA/Hibernate updates.
---

# Java Modernization Skill

Use this skill when modernizing legacy Java applications to Spring Boot 3.x for Azure compatibility.

## When to Use This Skill

- Migrating Java EE (J2EE) to Spring Boot
- Upgrading Java 8/11 to Java 17/21
- Converting XML configuration to Java config or YAML
- Migrating EJB to Spring components
- Modernizing JAAS/container security to Spring Security
- Moving from application servers (WebLogic, WebSphere, JBoss) to embedded servers

## Framework Version Mapping

| Legacy Version | Target Version | Notes |
|----------------|----------------|-------|
| Java 8 | Java 21 LTS | Long-term support |
| Java 11 | Java 21 LTS | Recommended upgrade path |
| Spring 4.x/5.x | Spring Boot 3.x | Requires Java 17+ |
| Java EE 7/8 | Jakarta EE 10 or Spring Boot 3.x | Namespace changes |

## Java EE to Spring Boot Mapping

| Java EE Component | Spring Boot Equivalent |
|-------------------|------------------------|
| EJB `@Stateless` | `@Service` or `@Component` |
| EJB `@Stateful` | `@Scope("session")` bean |
| EJB `@Singleton` | `@Component` (default singleton) |
| `@PersistenceContext` | `@Autowired EntityManager` or Spring Data |
| `@Resource` | `@Autowired` or `@Value` |
| `@EJB` | `@Autowired` |
| JSF Managed Bean | `@Controller` + Thymeleaf |
| CDI `@Inject` | `@Autowired` |
| JMS `@MessageDriven` | `@JmsListener` |
| JAX-RS `@Path` | `@RestController` + `@RequestMapping` |
| JNDI lookup | Spring dependency injection |

## Configuration Transformation

### XML to Java Config

```java
// Legacy XML (applicationContext.xml)
// <bean id="userService" class="com.example.UserServiceImpl">
//     <property name="userRepository" ref="userRepository"/>
// </bean>

// Modern Java Config
@Configuration
public class AppConfig {
    @Bean
    public UserService userService(UserRepository userRepository) {
        return new UserServiceImpl(userRepository);
    }
}

// Or simply use component scanning
@Service
public class UserServiceImpl implements UserService {
    private final UserRepository userRepository;
    
    public UserServiceImpl(UserRepository userRepository) {
        this.userRepository = userRepository;
    }
}
```

### XML to YAML Configuration

```yaml
# Legacy properties file
# database.url=jdbc:sqlserver://localhost:1433;database=mydb
# database.username=user
# database.password=pass

# Modern application.yml
spring:
  datasource:
    url: jdbc:sqlserver://${DB_HOST:localhost}:1433;database=${DB_NAME:mydb}
    username: ${DB_USER}
    password: ${DB_PASSWORD}
  jpa:
    hibernate:
      ddl-auto: validate
    properties:
      hibernate:
        dialect: org.hibernate.dialect.SQLServerDialect
```

## Authentication Migration

### JAAS → Spring Security + OAuth2

```java
// Legacy JAAS configuration in web.xml
// <login-config>
//     <auth-method>FORM</auth-method>
// </login-config>

// Modern Spring Security with Entra ID
@Configuration
@EnableWebSecurity
public class SecurityConfig {
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/public/**").permitAll()
                .anyRequest().authenticated()
            )
            .oauth2Login(Customizer.withDefaults())
            .oauth2ResourceServer(oauth2 -> oauth2.jwt(Customizer.withDefaults()));
        return http.build();
    }
}
```

### application.yml for Entra ID

```yaml
spring:
  security:
    oauth2:
      client:
        registration:
          azure:
            client-id: ${AZURE_CLIENT_ID}
            client-secret: ${AZURE_CLIENT_SECRET}
            scope: openid, profile, email
        provider:
          azure:
            issuer-uri: https://login.microsoftonline.com/${AZURE_TENANT_ID}/v2.0
```

## Data Access Migration

### JDBC → Spring Data JPA

```java
// Legacy JDBC
public class UserDaoImpl implements UserDao {
    public User findById(Long id) {
        Connection conn = dataSource.getConnection();
        PreparedStatement ps = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
        ps.setLong(1, id);
        ResultSet rs = ps.executeQuery();
        // Manual mapping...
    }
}

// Modern Spring Data JPA
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    List<User> findByActiveTrue();
}

// Usage
@Service
public class UserService {
    private final UserRepository userRepository;
    
    public User findById(Long id) {
        return userRepository.findById(id)
            .orElseThrow(() -> new UserNotFoundException(id));
    }
}
```

## SOAP to REST Migration

| SOAP Element | REST Equivalent |
|--------------|-----------------|
| WSDL | OpenAPI/Swagger specification |
| `@WebService` | `@RestController` |
| `@WebMethod` | `@GetMapping`, `@PostMapping`, etc. |
| Complex types | DTOs with Jackson annotations |
| SOAP Fault | `@ExceptionHandler` + RFC 7807 Problem Details |

See the [wcf-to-rest-migration](../wcf-to-rest-migration/SKILL.md) skill for detailed patterns.

## Package/Dependency Mapping

| Legacy Dependency | Modern Replacement |
|-------------------|-------------------|
| `javax.*` packages | `jakarta.*` packages |
| Apache Commons | Java 8+ Stream API or existing |
| Log4j 1.x | SLF4J + Logback |
| Apache HttpClient 4.x | Java 11 HttpClient or RestClient |
| Hibernate 4/5 | Hibernate 6 (via Spring Boot 3) |
| Jackson 2.x | Keep (Spring Boot manages version) |

## Maven POM Modernization

```xml
<!-- Legacy parent -->
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.2.0</version>
</parent>

<properties>
    <java.version>21</java.version>
</properties>

<dependencies>
    <!-- Web -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    
    <!-- Data -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    
    <!-- Azure SQL -->
    <dependency>
        <groupId>com.microsoft.sqlserver</groupId>
        <artifactId>mssql-jdbc</artifactId>
        <scope>runtime</scope>
    </dependency>
    
    <!-- Security -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-oauth2-client</artifactId>
    </dependency>
    
    <!-- Azure Identity -->
    <dependency>
        <groupId>com.azure.spring</groupId>
        <artifactId>spring-cloud-azure-starter-active-directory</artifactId>
    </dependency>
</dependencies>
```

## Template Files

- [Application.java](./templates/Application.java) - Spring Boot entry point
- [application.yml](./templates/application.yml) - Configuration template
- [Dockerfile](./templates/Dockerfile) - Container template for Java 21

## Best Practices

1. **Use constructor injection** - Prefer over field injection
2. **Externalize configuration** - Use environment variables for secrets
3. **Use Spring Data repositories** - Reduce boilerplate
4. **Enable virtual threads** - For high-concurrency apps (Java 21)
5. **Use records for DTOs** - Immutable data carriers
6. **Configure health endpoints** - For Azure monitoring
7. **Use SLF4J** - Consistent logging abstraction
