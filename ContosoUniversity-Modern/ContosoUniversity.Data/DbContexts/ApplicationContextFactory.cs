using ContosoUniversity.Data.DbContexts;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Design;
using Microsoft.Extensions.Configuration;
using System;
using System.IO;

namespace ContosoUniversity.Data.DbContexts
{
    public class ApplicationContextFactory : IDesignTimeDbContextFactory<ApplicationContext>
    {
        public ApplicationContext CreateDbContext(string[] args)
        {
            var config = new ConfigurationBuilder()
                .SetBasePath(Directory.GetCurrentDirectory())
                .AddJsonFile("appsettings.json", optional: false, reloadOnChange: true)
                .AddJsonFile($"appsettings.{Environment.GetEnvironmentVariable("ASPNETCORE_ENVIRONMENT") ?? "Production"}.json", optional: true, reloadOnChange: true)
                .AddEnvironmentVariables()
                .Build();

            var builder = new DbContextOptionsBuilder<ApplicationContext>();
            if (OperatingSystem.IsMacOs() || OperatingSystem.IsLinux())
            {
                builder.UseSqlite("Data Source=ContosoUniversity.sqlite");
            }
            else
            {
                builder.UseSqlServer(
                    config.GetConnectionString("DefaultConnection") 
                    ?? throw new InvalidOperationException("Connection string 'DefaultConnection' not found."), 
                    x => x.MigrationsHistoryTable("Migration", "Contoso"));
            }
            return new ApplicationContext(builder.Options);
        }
    }
}
