using ContosoUniversity.Data.Models;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace ContosoUniversity.Data
{
    public static class DbInitializer
    {
        public static async Task InitializeAsync(IServiceProvider serviceProvider)
        {
            using var scope = serviceProvider.CreateScope();
            var context = scope.ServiceProvider.GetRequiredService<ContosoUniversityDbContext>();
            
            // Apply migrations
            await context.Database.MigrateAsync();
            
            // Look for any students
            if (context.Students.Any())
            {
                return; // DB has been seeded
            }

            // Create students
            var students = new[]
            {
                new Student { Id = Guid.NewGuid(), FirstName = "Carson", LastName = "Alexander", EnrollmentDate = DateTime.Parse("2019-09-01") },
                new Student { Id = Guid.NewGuid(), FirstName = "Meredith", LastName = "Alonso", EnrollmentDate = DateTime.Parse("2017-09-01") },
                new Student { Id = Guid.NewGuid(), FirstName = "Arturo", LastName = "Anand", EnrollmentDate = DateTime.Parse("2018-09-01") },
                new Student { Id = Guid.NewGuid(), FirstName = "Gytis", LastName = "Barzdukas", EnrollmentDate = DateTime.Parse("2017-09-01") },
                new Student { Id = Guid.NewGuid(), FirstName = "Yan", LastName = "Li", EnrollmentDate = DateTime.Parse("2017-09-01") },
                new Student { Id = Guid.NewGuid(), FirstName = "Peggy", LastName = "Justice", EnrollmentDate = DateTime.Parse("2016-09-01") },
                new Student { Id = Guid.NewGuid(), FirstName = "Laura", LastName = "Norman", EnrollmentDate = DateTime.Parse("2018-09-01") },
                new Student { Id = Guid.NewGuid(), FirstName = "Nino", LastName = "Olivetto", EnrollmentDate = DateTime.Parse("2019-09-01") }
            };

            await context.Students.AddRangeAsync(students);
            
            // Create instructors
            var instructors = new[]
            {
                new Instructor { Id = Guid.NewGuid(), FirstName = "Kim", LastName = "Abercrombie", HireDate = DateTime.Parse("1995-03-11") },
                new Instructor { Id = Guid.NewGuid(), FirstName = "Fadi", LastName = "Fakhouri", HireDate = DateTime.Parse("2002-07-06") },
                new Instructor { Id = Guid.NewGuid(), FirstName = "Roger", LastName = "Harui", HireDate = DateTime.Parse("1998-07-01") },
                new Instructor { Id = Guid.NewGuid(), FirstName = "Candace", LastName = "Kapoor", HireDate = DateTime.Parse("2001-01-15") },
                new Instructor { Id = Guid.NewGuid(), FirstName = "Roger", LastName = "Zheng", HireDate = DateTime.Parse("2004-02-12") }
            };

            await context.Instructors.AddRangeAsync(instructors);
            
            // Create departments
            var departments = new[]
            {
                new Department { Id = Guid.NewGuid(), Name = "English", Budget = 350000, StartDate = DateTime.Parse("2007-09-01"), InstructorId = instructors[0].Id },
                new Department { Id = Guid.NewGuid(), Name = "Mathematics", Budget = 100000, StartDate = DateTime.Parse("2007-09-01"), InstructorId = instructors[1].Id },
                new Department { Id = Guid.NewGuid(), Name = "Engineering", Budget = 350000, StartDate = DateTime.Parse("2007-09-01"), InstructorId = instructors[2].Id },
                new Department { Id = Guid.NewGuid(), Name = "Economics", Budget = 100000, StartDate = DateTime.Parse("2007-09-01"), InstructorId = instructors[3].Id }
            };

            await context.Departments.AddRangeAsync(departments);
            
            // Create courses
            var courses = new[]
            {
                new Course { Id = Guid.NewGuid(), Title = "Chemistry", Credits = 3, DepartmentId = departments[2].Id },
                new Course { Id = Guid.NewGuid(), Title = "Microeconomics", Credits = 3, DepartmentId = departments[3].Id },
                new Course { Id = Guid.NewGuid(), Title = "Macroeconomics", Credits = 3, DepartmentId = departments[3].Id },
                new Course { Id = Guid.NewGuid(), Title = "Calculus", Credits = 4, DepartmentId = departments[1].Id },
                new Course { Id = Guid.NewGuid(), Title = "Trigonometry", Credits = 4, DepartmentId = departments[1].Id },
                new Course { Id = Guid.NewGuid(), Title = "Composition", Credits = 3, DepartmentId = departments[0].Id },
                new Course { Id = Guid.NewGuid(), Title = "Literature", Credits = 4, DepartmentId = departments[0].Id }
            };

            await context.Courses.AddRangeAsync(courses);
            
            // Create course assignments
            var courseAssignments = new[]
            {
                new CourseAssignment { Id = Guid.NewGuid(), CourseId = courses[0].Id, InstructorId = instructors[0].Id },
                new CourseAssignment { Id = Guid.NewGuid(), CourseId = courses[0].Id, InstructorId = instructors[1].Id },
                new CourseAssignment { Id = Guid.NewGuid(), CourseId = courses[1].Id, InstructorId = instructors[1].Id },
                new CourseAssignment { Id = Guid.NewGuid(), CourseId = courses[2].Id, InstructorId = instructors[2].Id },
                new CourseAssignment { Id = Guid.NewGuid(), CourseId = courses[3].Id, InstructorId = instructors[2].Id }
            };

            await context.CourseAssignments.AddRangeAsync(courseAssignments);
            
            // Create enrollments
            var enrollments = new[]
            {
                new Enrollment { Id = Guid.NewGuid(), StudentId = students[0].Id, CourseId = courses[0].Id, Grade = Grade.A },
                new Enrollment { Id = Guid.NewGuid(), StudentId = students[0].Id, CourseId = courses[1].Id, Grade = Grade.C },
                new Enrollment { Id = Guid.NewGuid(), StudentId = students[0].Id, CourseId = courses[2].Id, Grade = Grade.B },
                new Enrollment { Id = Guid.NewGuid(), StudentId = students[1].Id, CourseId = courses[0].Id, Grade = Grade.B },
                new Enrollment { Id = Guid.NewGuid(), StudentId = students[1].Id, CourseId = courses[1].Id, Grade = Grade.F },
                new Enrollment { Id = Guid.NewGuid(), StudentId = students[2].Id, CourseId = courses[0].Id },
                new Enrollment { Id = Guid.NewGuid(), StudentId = students[3].Id, CourseId = courses[0].Id }
            };

            await context.Enrollments.AddRangeAsync(enrollments);
            
            // Create office assignments
            var officeAssignments = new[]
            {
                new OfficeAssignment { Id = Guid.NewGuid(), InstructorId = instructors[0].Id, Location = "Smith 17" },
                new OfficeAssignment { Id = Guid.NewGuid(), InstructorId = instructors[1].Id, Location = "Gowan 27" },
                new OfficeAssignment { Id = Guid.NewGuid(), InstructorId = instructors[2].Id, Location = "Thompson 304" }
            };

            await context.OfficeAssignments.AddRangeAsync(officeAssignments);
            
            await context.SaveChangesAsync();
        }
    }
}
