using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using PartsUnlimited.Models;
using PartsUnlimited.ProductSearch;
using PartsUnlimited.Recommendations;
using PartsUnlimited.Utils;

var builder = WebApplication.CreateBuilder(args);

var connectionString = builder.Configuration.GetConnectionString("DefaultConnectionString")
    ?? throw new InvalidOperationException("Connection string 'DefaultConnectionString' not found.");

builder.Services.AddDbContext<PartsUnlimitedContext>(options => options.UseSqlServer(connectionString));
builder.Services.AddScoped<IPartsUnlimitedContext>(sp => sp.GetRequiredService<PartsUnlimitedContext>());
builder.Services.AddDatabaseDeveloperPageExceptionFilter();

builder.Services
    .AddIdentity<ApplicationUser, IdentityRole>(options =>
    {
        options.SignIn.RequireConfirmedAccount = false;
        options.Password.RequireNonAlphanumeric = false;
        options.Password.RequireUppercase = false;
    })
    .AddEntityFrameworkStores<PartsUnlimitedContext>()
    .AddDefaultTokenProviders()
    .AddDefaultUI();

builder.Services.ConfigureApplicationCookie(options =>
{
    options.LoginPath = "/Identity/Account/Login";
    options.LogoutPath = "/Identity/Account/Logout";
    options.AccessDeniedPath = "/Identity/Account/AccessDenied";
});

builder.Services.AddHttpContextAccessor();
builder.Services.AddDistributedMemoryCache();
builder.Services.AddSession();
builder.Services.AddMemoryCache();
builder.Services.AddApplicationInsightsTelemetry();

builder.Services.AddScoped<IShippingTaxCalculator, DefaultShippingTaxCalculator>();
builder.Services.AddScoped<IOrdersQuery, OrdersQuery>();
builder.Services.AddScoped<IRaincheckQuery, RaincheckQuery>();
builder.Services.AddScoped<IProductSearch, StringContainsProductSearch>();
builder.Services.AddScoped<IRecommendationEngine, NaiveRecommendationEngine>();
builder.Services.AddSingleton<ITelemetryProvider, TelemetryProvider>();

builder.Services.AddControllersWithViews(options =>
{
    options.Filters.Add<LayoutDataFilter>();
});
builder.Services.AddRazorPages();

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseMigrationsEndPoint();
    app.UseDeveloperExceptionPage();
}
else
{
    app.UseExceptionHandler("/Home/Error");
    app.UseHsts();
}

app.UseHttpsRedirection();
app.UseStaticFiles();
app.UseRouting();

app.UseSession();
app.UseAuthentication();
app.UseAuthorization();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");
app.MapRazorPages();

using (var scope = app.Services.CreateScope())
{
    var db = scope.ServiceProvider.GetRequiredService<PartsUnlimitedContext>();
    db.Database.EnsureCreated();
    PartsUnlimitedDbInitializer.Seed(db);
}

app.Run();
