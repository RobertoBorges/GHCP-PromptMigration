using ContosoUniversity.Data;
using ContosoUniversity.Web.Mapping;
using Microsoft.AspNetCore.Authentication.OpenIdConnect;
using Microsoft.Identity.Web;
using Microsoft.Identity.Web.UI;

var builder = WebApplication.CreateBuilder(args);

// Add Application Insights
builder.Services.AddApplicationInsightsTelemetry();

// Add Authentication services
builder.Services.AddAuthentication(OpenIdConnectDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApp(builder.Configuration.GetSection("AzureAd"));

// Add services to the container
builder.Services.AddControllersWithViews()
    .AddMicrosoftIdentityUI();

// Add SignalR
builder.Services.AddSignalR();

// Add AutoMapper
builder.Services.AddAutoMapper(typeof(MappingProfile));

// Add Data services
var connectionString = builder.Configuration.GetConnectionString("DefaultConnection");
builder.Services.AddDataServices(connectionString);

var app = builder.Build();

// Configure the HTTP request pipeline
if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
}
else
{
    app.UseExceptionHandler("/Home/Error");
    // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

app.UseAuthentication();
app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

// Map SignalR hub
app.MapHub<ContosoUniversity.Web.Hubs.UniversityHub>("/universityhub");

// Initialize the database
try
{
    using (var scope = app.Services.CreateScope())
    {
        var serviceProvider = scope.ServiceProvider;
        var logger = serviceProvider.GetRequiredService<ILogger<Program>>();
        
        logger.LogInformation("Initializing database...");
        await DbInitializer.InitializeAsync(serviceProvider);
        logger.LogInformation("Database initialized successfully.");
    }
}
catch (Exception ex)
{
    var logger = app.Services.GetRequiredService<ILogger<Program>>();
    logger.LogError(ex, "An error occurred while initializing the database.");
}

app.Run();
