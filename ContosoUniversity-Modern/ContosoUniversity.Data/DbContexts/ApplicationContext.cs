using ContosoUniversity.Data.Entities;
using Microsoft.EntityFrameworkCore;

namespace ContosoUniversity.Data.DbContexts
{
    public class ApplicationContext : DbContext
    {
        public ApplicationContext(DbContextOptions<ApplicationContext> options) : base(options)
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
            string? schema = "Contoso";
            if (OperatingSystem.IsMacOs() || OperatingSystem.IsLinux())
            {
                schema = null;
            }

            var config = new DbContextConfig();
            config.ApplicationContextConfig(modelBuilder, schema);
        }
    }
}
