using ContosoUniversity.Data.Repositories;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using System;

namespace ContosoUniversity.Data
{
    public static class ServiceExtensions
    {
        public static IServiceCollection AddDataServices(this IServiceCollection services, string connectionString)
        {
            // Register DbContext
            services.AddDbContext<ContosoUniversityDbContext>(options =>
                options.UseSqlServer(connectionString));
            
            // Register repositories
            services.AddScoped(typeof(IRepository<>), typeof(Repository<>));
            services.AddScoped<IStudentRepository, StudentRepository>();
            services.AddScoped<ICourseRepository, CourseRepository>();
            services.AddScoped<IInstructorRepository, InstructorRepository>();
            services.AddScoped<IDepartmentRepository, DepartmentRepository>();
            
            return services;
        }
    }
}
