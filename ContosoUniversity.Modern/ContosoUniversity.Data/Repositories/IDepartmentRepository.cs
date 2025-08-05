using ContosoUniversity.Data.Models;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace ContosoUniversity.Data.Repositories
{
    public interface IDepartmentRepository : IRepository<Department>
    {
        Task<IEnumerable<Department>> GetDepartmentsWithAdministratorAsync();
        Task<Department> GetDepartmentWithDetailsAsync(Guid id);
    }
}
