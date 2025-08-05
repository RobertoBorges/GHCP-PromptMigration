using ContosoUniversity.Data.Models;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace ContosoUniversity.Data.Repositories
{
    public class StudentRepository : Repository<Student>, IStudentRepository
    {
        public StudentRepository(ContosoUniversityDbContext context) : base(context)
        {
        }

        public async Task<IEnumerable<Student>> GetStudentsWithEnrollmentsAsync()
        {
            return await _context.Students
                .Include(s => s.Enrollments)
                    .ThenInclude(e => e.Course)
                .ToListAsync();
        }

        public async Task<Student> GetStudentWithEnrollmentsAsync(Guid id)
        {
            return await _context.Students
                .Include(s => s.Enrollments)
                    .ThenInclude(e => e.Course)
                .FirstOrDefaultAsync(s => s.Id == id);
        }
    }
}
