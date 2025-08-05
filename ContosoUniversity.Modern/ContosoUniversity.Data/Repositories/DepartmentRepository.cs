using ContosoUniversity.Data.Models;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace ContosoUniversity.Data.Repositories
{
    public class DepartmentRepository : Repository<Department>, IDepartmentRepository
    {
        public DepartmentRepository(ContosoUniversityDbContext context) : base(context)
        {
        }

        public async Task<IEnumerable<Department>> GetDepartmentsWithAdministratorAsync()
        {
            return await _context.Departments
                .Include(d => d.Administrator)
                .ToListAsync();
        }

        public async Task<Department> GetDepartmentWithDetailsAsync(Guid id)
        {
            return await _context.Departments
                .Include(d => d.Administrator)
                .Include(d => d.Courses)
                .FirstOrDefaultAsync(d => d.Id == id);
        }
    }
}
