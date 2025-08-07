using ContosoUniversity.Common.Repositories;
using ContosoUniversity.Data.DbContexts;
using System;

namespace ContosoUniversity.Common
{
    public interface IUnitOfWork : IDisposable
    {
        IDepartmentRepository Department { get; }
        ICourseRepository Course { get; }
        IStudentRepository Student { get; }
        IInstructorRepository Instructor { get; }
        IEnrollmentRepository Enrollment { get; }
        int Complete();
        ApplicationContext GetContext();
    }
}
