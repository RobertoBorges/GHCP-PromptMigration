// =============================================================================
// .NET 8 Program.cs Template
// =============================================================================
// Modern entry point for ASP.NET Core applications
// Replaces Global.asax, Startup.cs, and web.config configuration
// =============================================================================

using Microsoft.EntityFrameworkCore;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.Identity.Web;

var builder = WebApplication.CreateBuilder(args);

// =============================================================================
// Service Registration
// =============================================================================

// Add MVC with Razor Views (for web apps)
builder.Services.AddControllersWithViews();

// OR for API only:
// builder.Services.AddControllers();
// builder.Services.AddEndpointsApiExplorer();
// builder.Services.AddSwaggerGen();

// Database Context
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(
        builder.Configuration.GetConnectionString("DefaultConnection")));

// Caching
builder.Services.AddMemoryCache();
// OR for distributed cache with Redis:
// builder.Services.AddStackExchangeRedisCache(options =>
// {
//     options.Configuration = builder.Configuration.GetConnectionString("Redis");
// });

// Session (if needed)
builder.Services.AddSession(options =>
{
    options.IdleTimeout = TimeSpan.FromMinutes(30);
    options.Cookie.HttpOnly = true;
    options.Cookie.IsEssential = true;
});

// Authentication with Entra ID
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddMicrosoftIdentityWebApi(builder.Configuration.GetSection("AzureAd"));

// OR for cookie-based authentication:
// builder.Services.AddAuthentication(CookieAuthenticationDefaults.AuthenticationScheme)
//     .AddCookie(options =>
//     {
//         options.LoginPath = "/Account/Login";
//         options.LogoutPath = "/Account/Logout";
//     });

builder.Services.AddAuthorization();

// Application Services (register your services here)
// builder.Services.AddScoped<IUserService, UserService>();
// builder.Services.AddScoped<IProductService, ProductService>();

// Health Checks
builder.Services.AddHealthChecks()
    .AddDbContextCheck<ApplicationDbContext>();

// Application Insights
builder.Services.AddApplicationInsightsTelemetry();

// =============================================================================
// Build the Application
// =============================================================================

var app = builder.Build();

// =============================================================================
// Middleware Pipeline
// =============================================================================

if (app.Environment.IsDevelopment())
{
    app.UseDeveloperExceptionPage();
    // app.UseSwagger();
    // app.UseSwaggerUI();
}
else
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

// Authentication & Authorization
app.UseAuthentication();
app.UseAuthorization();

// Session
app.UseSession();

// Health check endpoints
app.MapHealthChecks("/health");
app.MapHealthChecks("/health/ready");
app.MapHealthChecks("/health/live");

// Default route
app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");

// OR for API:
// app.MapControllers();

app.Run();

// Make Program class accessible for integration tests
public partial class Program { }
