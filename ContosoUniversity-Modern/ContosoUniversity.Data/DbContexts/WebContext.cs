using ContosoUniversity.Data.DbContexts;
using ContosoUniversity.Data.Entities;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore;

namespace ContosoUniversity.Data.DbContexts
{
    public class WebContext : IdentityDbContext<ApplicationUser>
    {
        public WebContext(DbContextOptions<WebContext> options) : base(options)
        {
        }

        public DbSet<Course> Courses { get; set; } = default!;
        public DbSet<Enrollment> Enrollments { get; set; } = default!;
        public DbSet<Student> Students { get; set; } = default!;
        public DbSet<Department> Departments { get; set; } = default!;
        public DbSet<Instructor> Instructors { get; set; } = default!;
        public DbSet<OfficeAssignment> OfficeAssignments { get; set; } = default!;  
        public DbSet<CourseAssignment> CourseAssignments { get; set; } = default!;
        public DbSet<Person> People { get; set; } = default!;

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);
            string? schema = "Contoso";
            if (OperatingSystem.IsMacOs() || OperatingSystem.IsLinux())
            {
                schema = null;
            }

            var config = new DbContextConfig();
            config.SecureApplicationContextConfig(modelBuilder, schema);
            config.ApplicationContextConfig(modelBuilder, schema);
        }
    }
}
