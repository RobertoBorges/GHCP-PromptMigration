using ContosoUniversity.Data.Models;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace ContosoUniversity.Data.Repositories
{
    public interface IInstructorRepository : IRepository<Instructor>
    {
        Task<IEnumerable<Instructor>> GetInstructorsWithCoursesAndDepartmentsAsync();
        Task<Instructor> GetInstructorWithCoursesAndDepartmentsAsync(Guid id);
    }
}
