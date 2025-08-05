using ContosoUniversity.Data.Models;
using System;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace ContosoUniversity.Data.Repositories
{
    public interface ICourseRepository : IRepository<Course>
    {
        Task<IEnumerable<Course>> GetCoursesWithDepartmentAsync();
        Task<Course> GetCourseWithDetailsAsync(Guid id);
        Task<IEnumerable<Course>> GetCoursesByDepartmentAsync(Guid departmentId);
    }
}
