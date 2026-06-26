# =============================================================================
# Java 21 Multi-Stage Dockerfile for Azure Container Apps / AKS
# =============================================================================
# Optimized for Spring Boot with layered JARs
# =============================================================================

# Build stage
FROM eclipse-temurin:21-jdk-alpine AS build
WORKDIR /app

# Copy Maven wrapper and pom.xml for dependency caching
COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .

# Make Maven wrapper executable and download dependencies
RUN chmod +x mvnw && \
    ./mvnw dependency:go-offline -B

# Copy source code
COPY src src

# Build the application (skip tests for faster builds)
RUN ./mvnw package -DskipTests -B

# =============================================================================
# Extract layers for better Docker caching
# =============================================================================
FROM eclipse-temurin:21-jdk-alpine AS extract
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
RUN java -Djarmode=layertools -jar app.jar extract

# =============================================================================
# Runtime stage - JRE only for smaller image
# =============================================================================
FROM eclipse-temurin:21-jre-alpine AS final
WORKDIR /app

# Install curl for health checks
RUN apk add --no-cache curl tzdata

# Create non-root user for security
RUN addgroup -g 1000 appgroup && \
    adduser -u 1000 -G appgroup -D -s /bin/sh appuser

# Copy layers in order of change frequency (least → most)
COPY --from=extract /app/dependencies/ ./
COPY --from=extract /app/spring-boot-loader/ ./
COPY --from=extract /app/snapshot-dependencies/ ./
COPY --from=extract /app/application/ ./

# Change ownership to non-root user
RUN chown -R appuser:appgroup /app

# Switch to non-root user
USER appuser

# JVM configuration optimized for containers
ENV JAVA_OPTS="-XX:+UseContainerSupport \
    -XX:MaxRAMPercentage=75.0 \
    -XX:+UseG1GC \
    -XX:+ExitOnOutOfMemoryError \
    -Djava.security.egd=file:/dev/./urandom"

ENV SERVER_PORT=8080
ENV SPRING_PROFILES_ACTIVE=prod

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl --fail http://localhost:8080/actuator/health/liveness || exit 1

# Entry point using Spring Boot layered launcher
ENTRYPOINT ["java", "org.springframework.boot.loader.launch.JarLauncher"]
