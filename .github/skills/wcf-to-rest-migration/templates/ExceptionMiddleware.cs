// =============================================================================
// Global Exception Handler Middleware
// =============================================================================
// Replaces WCF [FaultContract] pattern with ProblemDetails
// =============================================================================

using Microsoft.AspNetCore.Diagnostics;
using Microsoft.AspNetCore.Mvc;
using System.Diagnostics;
using System.Net;
using System.Text.Json;

namespace MyApp.Api.Middleware;

/// <summary>
/// Global exception handler replacing WCF FaultContract pattern
/// 
/// WCF Migration Notes:
/// - [FaultContract(typeof(ServiceFault))] → ProblemDetails response
/// - throw new FaultException<T>() → throw custom exception
/// - Middleware catches all unhandled exceptions
/// </summary>
public class GlobalExceptionHandler : IExceptionHandler
{
    private readonly ILogger<GlobalExceptionHandler> _logger;
    private readonly IHostEnvironment _environment;

    public GlobalExceptionHandler(
        ILogger<GlobalExceptionHandler> logger,
        IHostEnvironment environment)
    {
        _logger = logger;
        _environment = environment;
    }

    public async ValueTask<bool> TryHandleAsync(
        HttpContext httpContext,
        Exception exception,
        CancellationToken cancellationToken)
    {
        _logger.LogError(exception, "Unhandled exception occurred: {Message}", exception.Message);

        var problemDetails = CreateProblemDetails(exception);

        httpContext.Response.StatusCode = problemDetails.Status ?? 500;
        httpContext.Response.ContentType = "application/problem+json";

        await httpContext.Response.WriteAsJsonAsync(problemDetails, cancellationToken);

        return true;
    }

    private ProblemDetails CreateProblemDetails(Exception exception)
    {
        var (statusCode, title) = exception switch
        {
            // Custom business exceptions (replace WCF FaultException types)
            ValidationException => (StatusCodes.Status400BadRequest, "Validation Error"),
            NotFoundException => (StatusCodes.Status404NotFound, "Resource Not Found"),
            UnauthorizedAccessException => (StatusCodes.Status401Unauthorized, "Unauthorized"),
            ForbiddenException => (StatusCodes.Status403Forbidden, "Forbidden"),
            ConflictException => (StatusCodes.Status409Conflict, "Conflict"),
            
            // Infrastructure exceptions
            TimeoutException => (StatusCodes.Status504GatewayTimeout, "Request Timeout"),
            OperationCanceledException => (StatusCodes.Status499ClientClosedRequest, "Request Cancelled"),
            
            // Default to 500
            _ => (StatusCodes.Status500InternalServerError, "Internal Server Error")
        };

        var problemDetails = new ProblemDetails
        {
            Status = statusCode,
            Title = title,
            Detail = _environment.IsDevelopment() ? exception.Message : "An error occurred processing your request.",
            Instance = $"urn:error:{Guid.NewGuid()}"
        };

        // Add stack trace in development
        if (_environment.IsDevelopment())
        {
            problemDetails.Extensions["stackTrace"] = exception.StackTrace;
            problemDetails.Extensions["exceptionType"] = exception.GetType().Name;
        }

        // Add correlation ID if available
        problemDetails.Extensions["traceId"] = Activity.Current?.Id ?? Guid.NewGuid().ToString();

        return problemDetails;
    }
}

// =============================================================================
// Custom Exception Types (Replace WCF FaultException<T>)
// =============================================================================

/// <summary>
/// Base exception for business logic errors
/// Replaces: FaultException&lt;ServiceFault&gt;
/// </summary>
public abstract class BusinessException : Exception
{
    public string ErrorCode { get; }

    protected BusinessException(string message, string errorCode = "BUSINESS_ERROR")
        : base(message)
    {
        ErrorCode = errorCode;
    }
}

/// <summary>
/// Validation error exception
/// Replaces: FaultException&lt;ValidationFault&gt;
/// </summary>
public class ValidationException : BusinessException
{
    public IDictionary<string, string[]> Errors { get; }

    public ValidationException(string message, IDictionary<string, string[]>? errors = null)
        : base(message, "VALIDATION_ERROR")
    {
        Errors = errors ?? new Dictionary<string, string[]>();
    }
}

/// <summary>
/// Resource not found exception
/// Replaces: FaultException&lt;NotFoundFault&gt;
/// </summary>
public class NotFoundException : BusinessException
{
    public string ResourceType { get; }
    public string ResourceId { get; }

    public NotFoundException(string resourceType, string resourceId)
        : base($"{resourceType} with ID '{resourceId}' was not found", "NOT_FOUND")
    {
        ResourceType = resourceType;
        ResourceId = resourceId;
    }

    public NotFoundException(string message)
        : base(message, "NOT_FOUND")
    {
        ResourceType = "Unknown";
        ResourceId = "Unknown";
    }
}

/// <summary>
/// Forbidden access exception
/// </summary>
public class ForbiddenException : BusinessException
{
    public ForbiddenException(string message = "You do not have permission to perform this action")
        : base(message, "FORBIDDEN")
    {
    }
}

/// <summary>
/// Resource conflict exception
/// Replaces: FaultException&lt;ConcurrencyFault&gt;
/// </summary>
public class ConflictException : BusinessException
{
    public ConflictException(string message)
        : base(message, "CONFLICT")
    {
    }
}

// =============================================================================
// Extension Method for Registration
// =============================================================================

public static class ExceptionHandlerExtensions
{
    /// <summary>
    /// Register global exception handler in Program.cs
    /// </summary>
    public static IServiceCollection AddGlobalExceptionHandler(this IServiceCollection services)
    {
        services.AddExceptionHandler<GlobalExceptionHandler>();
        services.AddProblemDetails();
        return services;
    }

    /// <summary>
    /// Use global exception handler in middleware pipeline
    /// </summary>
    public static IApplicationBuilder UseGlobalExceptionHandler(this IApplicationBuilder app)
    {
        app.UseExceptionHandler();
        return app;
    }
}
