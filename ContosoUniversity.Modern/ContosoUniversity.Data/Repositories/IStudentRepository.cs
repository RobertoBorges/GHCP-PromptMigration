using ContosoUniversity.Data.Models;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace ContosoUniversity.Data.Repositories
{
    public interface IStudentRepository : IRepository<Student>
    {
        Task<IEnumerable<Student>> GetStudentsWithEnrollmentsAsync();
        Task<Student> GetStudentWithEnrollmentsAsync(Guid id);
    }
}
