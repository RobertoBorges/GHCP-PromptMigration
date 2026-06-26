using Microsoft.AspNetCore.Mvc.Testing;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;

namespace MyApp.Tests;

/// <summary>
/// Base class for integration tests
/// Provides WebApplicationFactory configuration and test utilities
/// </summary>
public abstract class IntegrationTestBase : IClassFixture<WebApplicationFactory<Program>>, IAsyncLifetime
{
    protected readonly WebApplicationFactory<Program> Factory;
    protected readonly HttpClient Client;
    protected IServiceScope Scope = null!;

    protected IntegrationTestBase(WebApplicationFactory<Program> factory)
    {
        Factory = factory.WithWebHostBuilder(builder =>
        {
            builder.ConfigureServices(services =>
            {
                // Remove existing DbContext registration
                var descriptor = services.SingleOrDefault(
                    d => d.ServiceType == typeof(DbContextOptions<ApplicationDbContext>));
                if (descriptor != null)
                {
                    services.Remove(descriptor);
                }

                // Add in-memory database for testing
                services.AddDbContext<ApplicationDbContext>(options =>
                {
                    options.UseInMemoryDatabase($"TestDb_{Guid.NewGuid()}");
                });

                // Configure additional test services
                ConfigureTestServices(services);
            });
        });

        Client = Factory.CreateClient(new WebApplicationFactoryClientOptions
        {
            AllowAutoRedirect = false
        });
    }

    /// <summary>
    /// Override to configure additional test services
    /// </summary>
    protected virtual void ConfigureTestServices(IServiceCollection services)
    {
        // Override in derived classes to add mock services
    }

    public async Task InitializeAsync()
    {
        Scope = Factory.Services.CreateScope();
        var context = Scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
        await context.Database.EnsureCreatedAsync();
        await SeedTestDataAsync(context);
    }

    /// <summary>
    /// Override to seed test data
    /// </summary>
    protected virtual Task SeedTestDataAsync(ApplicationDbContext context)
    {
        return Task.CompletedTask;
    }

    public async Task DisposeAsync()
    {
        Scope.Dispose();
        await Task.CompletedTask;
    }

    /// <summary>
    /// Get a service from the test DI container
    /// </summary>
    protected T GetService<T>() where T : notnull
    {
        return Scope.ServiceProvider.GetRequiredService<T>();
    }
}
