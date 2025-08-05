using ContosoUniversity.Data.Models;
using Microsoft.EntityFrameworkCore;
using System;

namespace ContosoUniversity.Data
{
    public class ContosoUniversityDbContext : DbContext
    {
        public ContosoUniversityDbContext(DbContextOptions<ContosoUniversityDbContext> options)
            : base(options)
        {
        }

        public DbSet<Course> Courses { get; set; }
        public DbSet<Enrollment> Enrollments { get; set; }
        public DbSet<Student> Students { get; set; }
        public DbSet<Department> Departments { get; set; }
        public DbSet<Instructor> Instructors { get; set; }
        public DbSet<OfficeAssignment> OfficeAssignments { get; set; }
        public DbSet<CourseAssignment> CourseAssignments { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Configure discriminator for Person class hierarchy
            modelBuilder.Entity<Person>()
                .HasDiscriminator<string>("Discriminator")
                .HasValue<Student>("Student")
                .HasValue<Instructor>("Instructor");

            // Configure Course to Department relationship
            modelBuilder.Entity<Course>()
                .HasOne(c => c.Department)
                .WithMany(d => d.Courses)
                .HasForeignKey(c => c.DepartmentId);

            // Configure Department to Instructor relationship
            modelBuilder.Entity<Department>()
                .HasOne(d => d.Administrator)
                .WithMany(i => i.Departments)
                .HasForeignKey(d => d.InstructorId)
                .IsRequired(false);

            // Configure CourseAssignment relationships
            modelBuilder.Entity<CourseAssignment>()
                .HasOne(ca => ca.Instructor)
                .WithMany(i => i.CourseAssignments)
                .HasForeignKey(ca => ca.InstructorId);

            modelBuilder.Entity<CourseAssignment>()
                .HasOne(ca => ca.Course)
                .WithMany(c => c.CourseAssignments)
                .HasForeignKey(ca => ca.CourseId);

            // Configure OfficeAssignment relationship
            modelBuilder.Entity<OfficeAssignment>()
                .HasOne(o => o.Instructor)
                .WithOne(i => i.OfficeAssignment)
                .HasForeignKey<OfficeAssignment>(o => o.InstructorId);

            // Configure Enrollment relationships
            modelBuilder.Entity<Enrollment>()
                .HasOne(e => e.Student)
                .WithMany(s => s.Enrollments)
                .HasForeignKey(e => e.StudentId);

            modelBuilder.Entity<Enrollment>()
                .HasOne(e => e.Course)
                .WithMany(c => c.Enrollments)
                .HasForeignKey(e => e.CourseId);
        }
    }
}
