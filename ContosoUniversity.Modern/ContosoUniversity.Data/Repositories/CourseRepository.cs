using ContosoUniversity.Data.Models;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace ContosoUniversity.Data.Repositories
{
    public class CourseRepository : Repository<Course>, ICourseRepository
    {
        public CourseRepository(ContosoUniversityDbContext context) : base(context)
        {
        }

        public async Task<IEnumerable<Course>> GetCoursesWithDepartmentAsync()
        {
            return await _context.Courses
                .Include(c => c.Department)
                .ToListAsync();
        }

        public async Task<Course> GetCourseWithDetailsAsync(Guid id)
        {
            return await _context.Courses
                .Include(c => c.Department)
                .Include(c => c.Enrollments)
                    .ThenInclude(e => e.Student)
                .Include(c => c.CourseAssignments)
                    .ThenInclude(ca => ca.Instructor)
                .FirstOrDefaultAsync(c => c.Id == id);
        }

        public async Task<IEnumerable<Course>> GetCoursesByDepartmentAsync(Guid departmentId)
        {
            return await _context.Courses
                .Where(c => c.DepartmentId == departmentId)
                .Include(c => c.Department)
                .ToListAsync();
        }
    }
}
