using ContosoUniversity.Data.Models;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace ContosoUniversity.Data.Repositories
{
    public class InstructorRepository : Repository<Instructor>, IInstructorRepository
    {
        public InstructorRepository(ContosoUniversityDbContext context) : base(context)
        {
        }

        public async Task<IEnumerable<Instructor>> GetInstructorsWithCoursesAndDepartmentsAsync()
        {
            return await _context.Instructors
                .Include(i => i.OfficeAssignment)
                .Include(i => i.CourseAssignments)
                    .ThenInclude(ca => ca.Course)
                        .ThenInclude(c => c.Department)
                .Include(i => i.Departments)
                .ToListAsync();
        }

        public async Task<Instructor> GetInstructorWithCoursesAndDepartmentsAsync(Guid id)
        {
            return await _context.Instructors
                .Include(i => i.OfficeAssignment)
                .Include(i => i.CourseAssignments)
                    .ThenInclude(ca => ca.Course)
                        .ThenInclude(c => c.Department)
                .Include(i => i.Departments)
                .FirstOrDefaultAsync(i => i.Id == id);
        }
    }
}
