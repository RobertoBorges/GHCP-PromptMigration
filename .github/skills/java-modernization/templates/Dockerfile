# Build stage
FROM eclipse-temurin:21-jdk-alpine AS build
WORKDIR /app

# Copy Maven wrapper and pom
COPY mvnw .
COPY .mvn .mvn
COPY pom.xml .

# Make wrapper executable and download dependencies
RUN chmod +x mvnw && ./mvnw dependency:go-offline -B

# Copy source and build
COPY src src
RUN ./mvnw package -DskipTests -B

# Extract layers for better caching
FROM eclipse-temurin:21-jdk-alpine AS extract
WORKDIR /app
COPY --from=build /app/target/*.jar app.jar
RUN java -Djarmode=layertools -jar app.jar extract

# Runtime stage
FROM eclipse-temurin:21-jre-alpine AS final
WORKDIR /app

# Install curl for health checks
RUN apk add --no-cache curl

# Create non-root user for security
RUN addgroup -g 1000 appgroup && adduser -u 1000 -G appgroup -D appuser
USER appuser

# Copy layers in order of change frequency (least → most)
COPY --from=extract /app/dependencies/ ./
COPY --from=extract /app/spring-boot-loader/ ./
COPY --from=extract /app/snapshot-dependencies/ ./
COPY --from=extract /app/application/ ./

# JVM configuration for containers
ENV JAVA_OPTS="-XX:+UseContainerSupport -XX:MaxRAMPercentage=75.0 -XX:+UseG1GC"
ENV SERVER_PORT=8080
ENV SPRING_PROFILES_ACTIVE=prod

EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl --fail http://localhost:8080/actuator/health/liveness || exit 1

ENTRYPOINT ["java", "org.springframework.boot.loader.launch.JarLauncher"]
