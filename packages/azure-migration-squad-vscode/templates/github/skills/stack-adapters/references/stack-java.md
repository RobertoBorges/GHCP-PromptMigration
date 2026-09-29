# Skill: Stack Adapter — Java (Java SE + EE + Spring + modern JVM apps)

> Stack adapter for any Java application: Java 8 / 11 / 17 / 21, Java EE / Jakarta EE, Spring 4.x / 5.x / Spring Boot 2.x / 3.x, Quarkus, Micronaut, Tomcat / JBoss / WebLogic / WebSphere-hosted apps, Servlet / JSP / JSF, Batch jobs.

> This adapter consolidates the content from the legacy `Assess-Java-Upgrade` prompt.

## When to Use

- `stack.primary_stack: java` in the Capability Matrix
- File evidence: `pom.xml`, `build.gradle`, `*.java`, `*.jsp`, `WEB-INF/`, `META-INF/`, `*.war`, `*.ear`, `*.jar`

## Sub-Stack Detection

| Sub-stack | Detection signal | Typical migration target |
|-----------|------------------|--------------------------|
| **Spring Boot 3.x (Java 17+)** | `spring-boot-starter-parent:3.x` in pom; `jakarta.*` imports | Current; redeploy on Container Apps / App Service / Spring Apps |
| **Spring Boot 2.x (Java 8/11)** | `spring-boot-starter-parent:2.x`; `javax.*` imports | Upgrade to 3.x + Java 21 (mandatory `javax → jakarta`) |
| **Spring 4.x / 5.x classic** | `org.springframework:spring-context:4.x|5.x`, XML config, `web.xml` | Migrate to Spring Boot 3.x |
| **Java EE 7 / 8 (javax)** | EJB (`@Stateless`, `@Singleton`, `@MessageDriven`); `@WebServlet`; `persistence.xml` | Modernize to Spring Boot 3.x or Jakarta EE 10 |
| **Jakarta EE 9+ (jakarta)** | `jakarta.servlet`, `jakarta.persistence` | Already on modern API; redeploy |
| **Quarkus** | `io.quarkus.platform:quarkus-bom` | Already cloud-native; redeploy |
| **Micronaut** | `io.micronaut:micronaut-bom` | Already cloud-native; redeploy |
| **Plain Servlet / JSP (no framework)** | `web.xml` + servlets + JSPs only | Modernize to Spring Boot or rewrite |
| **JSF** | `javax.faces.*` / `jakarta.faces.*`, `*.xhtml` | Rewrite UI to modern framework; or containerize as-is |
| **Spring Batch** | `spring-boot-starter-batch`, `Job`, `Step` beans | Container Apps Jobs or Spring Apps Enterprise |
| **Apache Camel / Mule / Boomi** | `org.apache.camel:camel-*` | Modernize routes; consider Logic Apps for some |

## App Server Detection

Hosting matters as much as the framework:

| Server signal | Implication |
|---------------|-------------|
| Embedded Tomcat (Spring Boot default) | Easy → any Azure compute |
| Standalone Tomcat 9/10 (`*.war` only) | Container Apps / App Service Linux Tomcat |
| JBoss / WildFly | Container Apps with custom image, or AKS |
| WebLogic | Azure Marketplace WebLogic on VM, or refactor to Spring Boot |
| WebSphere (traditional) | Azure VMs (WebSphere ND offered), or refactor to Open Liberty + AKS |
| Open Liberty / WebSphere Liberty | Container Apps / AKS |
| GlassFish / Payara | Container Apps with custom image |
| Jetty embedded | Easy → any Azure compute |

Look at: `Dockerfile FROM` line, `pom.xml` `<packaging>` (war vs jar), `web.xml` presence, server-specific deployment descriptors (`jboss-web.xml`, `weblogic.xml`, `ibm-web-bnd.xml`).

## Probes

### Build manifest inspection

For `pom.xml`:

1. `<java.version>` / `<maven.compiler.source>` / `<maven.compiler.target>` → Java version
2. `<packaging>` → `jar` (Spring Boot fat jar) / `war` (servlet container) / `ear` (full JEE)
3. `<parent>` → Spring Boot parent version (signals overall stack)
4. `<dependencies>` → top dependencies (`spring-boot-starter-*`, `javax.*`, `jakarta.*`, `hibernate`, `log4j`, etc.)
5. `<plugins>` → `spring-boot-maven-plugin`, `jib-maven-plugin`, `dockerfile-maven-plugin` (container build path)

For `build.gradle` / `build.gradle.kts`:

1. `sourceCompatibility` / `targetCompatibility` / `JavaLanguageVersion.of()`
2. `plugins { id 'org.springframework.boot' version 'X' }`
3. `dependencies { implementation '...' }`

### Code/import inspection

Critical migration signal: **`javax.*` vs `jakarta.*`**

- `javax.servlet.*` / `javax.persistence.*` / `javax.ejb.*` → JEE 8 or earlier → mandatory rename to `jakarta.*` when upgrading to Spring Boot 3 / Jakarta EE 10+
- `jakarta.servlet.*` → already on the modern API
- Mixed usage → in-progress migration

Other patterns:

- `log4j 1.x` / `log4j 2.x < 2.17.1` → CVE; mandatory upgrade
- `Jackson 2.x` → check `<jackson.version>` against Spring Boot version
- `Hibernate 5.x` → must upgrade to 6.x with Spring Boot 3
- `JUnit 4` → JUnit 5 with vintage engine, or upgrade
- `System.out.println` everywhere → suggest SLF4J migration

### Configuration inspection

- `application.properties` / `application.yml` → Spring config
- `web.xml` → presence implies servlet container or legacy Spring
- `persistence.xml` → JPA provider + DataSource JNDI name → DB engine signal
- `ejb-jar.xml` → EJB declarations
- `applicationContext.xml` / `spring-context.xml` → legacy Spring XML config (modernize to annotations)

### Data access

- JPA (Hibernate / EclipseLink) → standard
- jOOQ → fine
- MyBatis → fine
- Plain JDBC → fine but old
- Spring Data JPA → idiomatic Spring Boot

### Tests

- JUnit 4 / JUnit 5
- TestNG
- Mockito
- Testcontainers
- Spring Boot Test
- Maven Surefire / Failsafe; Gradle Test

## Phase 2 Effort Mapping

| Sub-stack | Phase 2 effort | Notes |
|-----------|----------------|-------|
| Spring Boot 3.x already | S | Minor library bumps only |
| Spring Boot 2.x → 3.x | M | Mandatory `javax→jakarta` + Spring Security overhaul |
| Spring 4/5 → Spring Boot 3 | L | Heavy refactor; XML → annotations |
| Java EE 7/8 → Spring Boot 3 | L | EJB → Spring beans; JNDI DS → Spring DS |
| Java 8 → Java 21 | M | Module system; sealed classes; preview features off |
| Plain Servlet/JSP → Spring Boot | XL | Rewrite to MVC/REST |
| WebLogic → Spring Boot on AKS | XL | Server-specific APIs (`weblogic.*`) replacement |
| WebSphere → Open Liberty on AKS | L | Often easier than going to Spring Boot |

## Identity Modernization

| Today | Target |
|-------|--------|
| Container-managed auth (`<security-constraint>` in web.xml) | Spring Security + Entra ID OIDC |
| Custom realm | Spring Security custom + Entra ID |
| OpenAM / Keycloak | Keep Keycloak on AKS, or migrate IDP to Entra ID |
| LDAP / AD | Entra ID Connect or federation |
| Hardcoded users | Entra ID + roles |

## Target Azure Mapping

| Sub-stack | Primary Azure target | Secondary |
|-----------|----------------------|-----------|
| Spring Boot 3 (fat jar) | App Service Linux (Java SE) | Container Apps; Azure Spring Apps Enterprise |
| Spring Boot war | App Service Linux (Tomcat) | Container Apps |
| JEE app (WildFly / Open Liberty container) | Container Apps with custom image | AKS |
| WebSphere traditional | Azure VM (WebSphere ND) | Refactor to Liberty + Container Apps |
| WebLogic | Azure Marketplace WebLogic VM | Refactor to Spring Boot |
| Spring Batch | Container Apps Jobs | Azure Spring Apps Enterprise |
| Quarkus / Micronaut | Container Apps (native image) | AKS |

## Anti-Patterns

- Don't upgrade Spring Boot 2 → 3 without doing the `javax→jakarta` rename across the codebase. Use `openrewrite` or IDE structural search.
- Don't host JEE container apps on App Service expecting them to work as-is — App Service Linux Tomcat hosts WARs, not EAR full-JEE deployments.
- Don't auto-port WebLogic-specific APIs (`weblogic.jms.*`, `weblogic.security.*`) to Spring — design replacements explicitly.
- Don't drop Hibernate 5 without checking custom dialects/converters.
- Don't preserve `log4j 1.x` in any migration — replace with Logback or Log4j 2.

## Output Checklist

- [ ] Sub-stack identified (one of the 11 above)
- [ ] Java version captured
- [ ] App server identified
- [ ] `javax` vs `jakarta` usage characterized
- [ ] Top dependencies inventoried
- [ ] Spring / JEE / framework version captured
- [ ] Web descriptors captured (web.xml, persistence.xml, ejb-jar.xml, server-specific files)
- [ ] Data access pattern captured
- [ ] Tests inventory captured
- [ ] log4j 1.x / CVE-bearing dependencies flagged
- [ ] Phase 2 effort label assigned (S/M/L/XL)
- [ ] Target Azure compute candidate noted
